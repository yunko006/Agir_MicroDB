import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'mongodb'

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for the flask app")


class DevelopmentConfig(Config):
    BEBUG = True
    TESTING = True
