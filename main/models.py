import base64

from modules.database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    photos = db.relationship('Photo', backref=db.backref('users'))
    tasks = db.relationship('PhotoTask', backref=db.backref('users'))

    def __init__(self, username, password, email):
        self.name = username
        self.password = password
        self.email = email

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    def find_by_id(user_id):
        return User.query.get(user_id)


class PhotoTask(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), unique=False, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    photos = db.relationship('Photo', backref=db.backref('tasks'))

    def __init__(self, description, user_id):
        self.description = description
        self.owner_id = user_id

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def find_by_creator_id(user_id):
        return PhotoTask.query.filter_by(owner_id=user_id).all()


class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String(1000))
    # encode_photo_url = db.Column(db.String(2000))
    description = db.Column(db.String(1000))

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, photo_url, description, task_id, owner_id):
        self.photo_url = photo_url
        # self.encode_photo_url = encode_photo_url
        self.description = description
        self.task_id = task_id
        self.owner_id = owner_id

    def upload(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def is_empty(self):
        photos = self.query.all()
        return False if len(photos) else True

    def add_photo_url(self, url):
        self.photo_url = url
        # encode_photo_url = base64.b64encode(bytes(url, 'utf-8'))
        # print("[*] encode_photo_url = " + encode_photo_url.__str__())
        # self.encode_photo_url = encode_photo_url
        db.session.commit()
