import os

HOST = '0.0.0.0'
PORT = 5000

class Configuration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret-key-goes-here'
    TESTING = False
    UPLOAD_DIRECTORY = '/tmp'
    MINIO_ENDPOINT = 'compose-minio:9000'
    MINIO_ACCESS_KEY = 'minio'
    MINIO_SECRET_KEY = 'minio123'
    MINIO_STORAGE_URL = 'localhost:9000/minio/'