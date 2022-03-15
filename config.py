import os

MONGODB_URI = os.environ.get('MONGODB_URI')


class Config:
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_SETTINGS = {
        'db': 'benevole',
        'host': MONGODB_URI,
    }

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for the flask app")


class DevelopmentConfig(Config):
    BEBUG = True
    TESTING = True
