import os
import redis
from flask import Flask
from flask_session import Session
from config import DevelopmentConfig
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from app.role_required import not_ROLE


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# mongodb
db = MongoEngine(app)
# app.session_interface = MongoEngineSessionInterface(db)

# Configure MongoDB for storing the session data on the server-side
# app.config['SESSION_TYPE'] = 'mongodb'
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_MONGODB'] = os.environ.get('MONGODB_URI')

# Create and initialize the Flask-Session object AFTER `app` has been configured
# server_session = Session(app)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
# Configure Redis for storing the session data on the server-side
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url(
    f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}')

# Create and initialize the Flask-Session object AFTER `app` has been configured
server_session = Session(app)


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


from app import routes, models
