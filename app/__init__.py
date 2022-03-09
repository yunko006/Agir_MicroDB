import os
from flask import Flask
from flask_session import Session
from config import DevelopmentConfig
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from app.role_required import not_ROLE


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Check Configuration section for more details
sess = Session()
sess.init_app(app)

# bootstrap
bootstrap = Bootstrap5(app)

# flask login set up
LoginManager.not_ROLE = not_ROLE
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.not_ROLE_view = 'not_ROLE'

# bcrypt setup
bcrypt = Bcrypt(app)


MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGODB_URI = os.environ.get('MONGODB_URI')


app.config['MONGODB_SETTINGS'] = {
    'db': 'benevole',
    'host': MONGODB_URI,
    'port': 27017
}

db = MongoEngine(app)

from app import routes, models

if __name__ == '__main__':
    app.run()
