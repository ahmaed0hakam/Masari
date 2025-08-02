import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security configuration
    SECRET_KEY = 'My|!w>YD/IT[&iE}?yV#>;}Xf]^7YgLV'
    
    # File upload configuration
    UPLOAD_FOLDER = 'CVs'
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # LLM Service configuration
    LLM_SERVICE_TYPE = 'huggingface'  # Options: 'huggingface', 'fallback'
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', 'hf_xxx')
    HUGGINGFACE_MODEL = 'microsoft/DialoGPT-medium'
    
    # Application configuration
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000 