import os


class Configuration:
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')
    SQLALCHEMY_DATABASE_URI = 'postgresql://hello_flask:hello_flask@' \
                              + os.environ.get('SQL_HOST') + ':' \
                              + os.environ.get('SQL_PORT') + '/hello_flask_dev'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = bool(os.environ.get('TESTING'))
    MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT')
    MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
    MINIO_SERVER_URL = os.environ.get('MINIO_SERVER_URL')
    MINIO_BROWSER_REDIRECT_URL = os.environ.get('MINIO_BROWSER_REDIRECT_URL')
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
    RABBITMQ_LOGIN = os.environ.get('RABBITMQ_LOGIN')
    RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
    RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT')
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
