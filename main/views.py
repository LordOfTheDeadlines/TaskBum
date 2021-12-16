import base64
import os

import flask_login
from amqp import loop, rpc_client
from flask import render_template, request, url_for, Blueprint
from flask_login import current_user
from minio_client import ensure_minio_bucket, get_objects_minio, get_minio_client
from models import PhotoTask, Photo
from config import Configuration
from urllib3.exceptions import ResponseError
from werkzeug.utils import redirect

taskbum = Blueprint('taskbum', __name__, template_folder='templates/taskbum')
BUCKET_NAME = Configuration.BUCKET_NAME


@taskbum.route('/profile')
@flask_login.login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@taskbum.route("/tasks")
def user_tasks():
    return render_template('user_tasks.html', tasks=PhotoTask.find_by_creator_id(current_user.id))


@taskbum.route('/tasks/generation', methods=['GET', 'POST'])
def task_generation():
    if request.method == 'POST':
        text = request.form.get('task')
        if text and not text.isspace():
            task = PhotoTask(text, current_user.id)
            PhotoTask.create(task)
        else:
            sendMessageInRabbit(current_user.id)
        return redirect(url_for('taskbum.user_tasks'))
    return render_template('task_generation.html')


@taskbum.route("/tasks/<int:task_id>")
def task_photos(task_id):
    print('[*] populate db')
    task = PhotoTask.query.get(int(task_id))
    return render_template('task_photos.html', task_id=task_id, task=task)


@taskbum.route("/addphoto/<task_id>", methods=['GET', 'POST'])
def add_photo(task_id):
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'images/')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)

        photo_file = request.files['file']
        description = request.form.get('text')
        if not photo_file:
            # flash('Please check your login details and try again.')
            pass
        else:
            photo = Photo(None, None, description, task_id, current_user.id)
            Photo.upload(photo)
            filename = f'{current_user.id}_{task_id}_{photo.id}.jpg'
            destination = "/".join([target, filename])
            photo_file.save(destination)
            ensure_minio_bucket(BUCKET_NAME)
            try:
                minioClient = get_minio_client()
                print('[*] fput')
                print(minioClient.fput_object(BUCKET_NAME, filename, destination))
                add_photo_to_db(photo, filename)
            except ResponseError as err:
                print(err)
            return redirect(url_for('taskbum.task_photos', task_id=task_id))
    return render_template('photo_form.html')


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def add_photo_to_db(photo, filename):
    try:
        # url = minioClient.presigned_get_object(BUCKET_NAME, filename, expires=timedelta(days=2))
        url = ''
        urls = get_objects_minio(BUCKET_NAME, filename)
        for u in urls:
            prefix = base64.b64encode(bytes(u.object_name, encoding='utf-8')).decode('utf-8')
            url = 'http://localhost:40089/api/v1/buckets/photos/objects/download?preview=true&prefix=' \
                  + prefix + '&version_id=null'
        print("[*] url = " + url)
        photo.add_photo_url(url)
    except:
        print("[*] Could not add " + str(photo) + " to db...")


def sendMessageInRabbit(body):
    print(' [x] Send message to SDK')
    loop.run_until_complete(rpc_client(body))
