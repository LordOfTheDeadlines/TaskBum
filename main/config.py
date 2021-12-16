import os

HOST = '0.0.0.0'
PORT = 5000


class Configuration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret-key-goes-here'
    TESTING = False
    MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT')
    MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
    RABBITMQ_LOGIN = os.environ.get('RABBITMQ_LOGIN')
    RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
