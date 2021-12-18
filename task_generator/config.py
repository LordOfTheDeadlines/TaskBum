import os


class Configuration:
    DEBUG = True
    RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
    RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT')
    RABBITMQ_LOGIN = os.environ.get('RABBITMQ_LOGIN')
    RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
