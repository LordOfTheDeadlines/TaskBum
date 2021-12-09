import os

import flask_login
import magic
from flask import render_template, request, url_for, Blueprint, current_app
from flask_login import current_user
from sqlalchemy.dialects.postgresql import psycopg2
from werkzeug.utils import redirect

from models import User, PhotoTask, Photo
from amqp import loop, rpc_client

from minio_client import hexdigest, ensure_minio_bucket, upload_minio, get_objects_minio

taskbum = Blueprint('taskbum', __name__, template_folder='templates/taskbum')
BUCKET_NAME = 'photos'


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
    task = PhotoTask.query.get(int(task_id))
    prefix = f'{current_user.id}_{task_id}_'
    print(prefix)
    for obj in get_objects_minio(BUCKET_NAME, prefix):
        print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
              obj.etag, obj.size, obj.content_type)
    return render_template('task_photos.html', task_id=task_id, task=task)


@taskbum.route("/addphoto/<task_id>", methods=['GET', 'POST'])
def add_photo(task_id):
    if request.method == 'POST':
        photo_file = request.files['file']
        description = request.form.get('text')
        if not photo_file:
            # flash('Please check your login details and try again.')
            pass
        else:
            photo = Photo(None, None, description, task_id, current_user.id)
            Photo.upload(photo)
            filename = f'{current_user.id}_{task_id}_{photo.id}.png'
            full_filepath = os.path.join(current_app.config['UPLOAD_DIRECTORY'], filename)
            photo_file.save(full_filepath)

            mime = magic.Magic(mime=True)
            content_type = mime.from_file(full_filepath)
            metadata = {'Content-type': content_type}
            print(metadata)

            ensure_minio_bucket(BUCKET_NAME)
            file_url = upload_minio(BUCKET_NAME, full_filepath, filename, content_type, metadata)
            photo.add_photo_url(file_url)

            os.remove(full_filepath)
            return redirect(url_for('taskbum.task_photos', task_id=task_id))

    return render_template('photo_form.html')


def sendMessageInRabbit(body):
    print(' [x] Send message to SDK')
    loop.run_until_complete(rpc_client(body))
