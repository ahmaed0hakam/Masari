from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config.config import Config
import os

# Initialize Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
cors = CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# Configure login manager
login_manager.login_view = 'login'
login_manager.init_app(app)

# Import routes after app initialization to avoid circular imports
from app.routes import auth, main, api
from app.models import models

@login_manager.user_loader
def load_user(user_id):
    return models.Users.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login')) 