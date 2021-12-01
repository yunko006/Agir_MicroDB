from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
import flask_login
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config.from_object(Config)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)

MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')


app.config['MONGODB_SETTINGS'] = {
    'db': 'benevole',
    'alias': 'default',
    'host': f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.07jrf.mongodb.net/agir?retryWrites=true&w=majority'
}

db = MongoEngine(app)

from app import routes, models
