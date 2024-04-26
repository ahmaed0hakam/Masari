from flask import Flask, render_template, redirect, url_for, request, jsonify
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime


#############################################
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_core.output_parsers import StrOutputParser
#############################################


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'My|!w>YD/IT[&iE}?yV#>;}Xf]^7YgLV'

# Define the Ollama model and callback manager
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = Ollama(model="llama3", callbacks=callback_manager, verbose=True)
output_parser = StrOutputParser()


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    # Redirect to the login page when unauthorized access is detected
    return redirect(url_for('login'))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date)
    learning_paths = db.relationship('LearningPaths', backref='user', lazy=True)
    courses = db.relationship('Courses', backref='user', lazy=True)


class LearningPaths(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    learning_path_id = db.Column(db.Integer, db.ForeignKey('learning_paths.id'), nullable=True)

    # Define a relationship to LearningPaths
    learning_path = db.relationship('LearningPaths', backref='courses')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Name"})
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=6)], render_kw={"placeholder": "Confirm Password"})
    birthdate = DateField('Birth Date', validators=[InputRequired()], render_kw={"placeholder": "Birth Date"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_password(self, field):
        if self.password.data != self.confirm_password.data:
            raise ValidationError('Passwords must match')
        

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

def login_required_redirect_dashboard(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # Redirect to the dashboard page if user is logged in
            return redirect(url_for('dashboard'))
        else:
            # Allow access to the original view function if user is not logged in
            return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user_id():
    if current_user.is_authenticated:
        return {'userId': current_user.id}
    else:
        return {'userId': None}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
@login_required_redirect_dashboard
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@login_required_redirect_dashboard
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        new_user = Users(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data,
            birthdate=form.birthdate.data  # Use the birthdate string directly
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    learning_paths = current_user.learning_paths
    courses = current_user.courses
    return render_template('dashboard.html', name=current_user.name, learning_paths=learning_paths, courses=courses)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')

@app.route('/liked', methods=['GET', 'POST'])
@login_required
def liked():
    return render_template('liked.html')

@app.route('/learningpath/<int:path_id>', methods=['GET', 'POST'])
@login_required
def learningpath(path_id):
    courses = Courses.query.filter_by(learning_path_id=path_id).all()

    course_titles = [{course.id, course.title} for course in courses]

    return render_template('learningpath.html', courses=course_titles)

@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def course(course_id):
    # Retrieve the learning path based on the course_id
    course = Courses.query.get_or_404(course_id)
    return render_template('course.html', course=course)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/generate_learningpath', methods=['POST'])
@login_required
def generate_learning_path():

    try:
        request_data = request.get_json()

        lp_title = request_data.get('text')
        user_id = request_data.get('user_id')

        # path_id = generate_path(text, user_id)

        # Define the prompt template with revised instructions
        prompt_template = """
        You are creating a personalized learning path for a user interested in {lp_title}. 
        Please provide the courses names only, ordered based on difficulty and correct ordering in the learning path, no another text in the string, only the courses names, the output format should be string separated by commas:
        """


        new_path = LearningPaths(title=lp_title, user_id=current_user.id)
        db.session.add(new_path)
        db.session.commit()
        
        # Populate the prompt with the user's topic
        prompt = prompt_template.format(lp_title=lp_title)  # Provide user_title as a named argument

        # Generate response from the modelp

        response_llm = llm.invoke(prompt)

        lp_courses = response_llm.replace('"', '').split(',')
        for course in lp_courses:
            new_course = Courses(title=course, learning_path_id=new_path.id)
            db.session.add(new_course)
            db.session.commit()

        response = {
            'id': new_path.id
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_courses', methods=['POST'])
@login_required
def generate_courses():
    # Placeholder for actual course generation logic
    new_course = Courses(title="Sample Course", description="Generated Course", user_id=current_user.id)
    db.session.add(new_course)
    db.session.commit()
    return {'id': new_course.id}



if __name__ == '__main__':
    app.run(debug=True)