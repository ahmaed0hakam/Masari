import re
from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def parse_prompt(input_text):
    pattern = r'^\d+\.\s(.+)$'
    courses = re.findall(pattern, input_text, re.MULTILINE)
    return courses

def allowed_file(filename):
    from config.config import Config
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def login_required_redirect_dashboard(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        else:
            return f(*args, **kwargs)
    return decorated_function 