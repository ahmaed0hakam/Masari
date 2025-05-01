from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_core.output_parsers import StrOutputParser
from config.config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
cors = CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# Configure login manager
login_manager.login_view = 'login'
login_manager.init_app(app)

# Initialize Ollama
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = Ollama(model="llama3", callbacks=callback_manager, verbose=True)
output_parser = StrOutputParser()

# Import routes after app initialization to avoid circular imports
from app.routes import auth, main, api
from app.models import models

@login_manager.user_loader
def load_user(user_id):
    return models.Users.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login')) 