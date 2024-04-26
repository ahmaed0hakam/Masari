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
llm = Ollama(model="phi3", callbacks=callback_manager, verbose=True)
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

class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    course = db.relationship('Courses', backref=db.backref('lessons', lazy=True))

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

    course_titles = [{'id':course.id, 'title': course.title} for course in courses]

    return render_template('learningpath.html', courses=course_titles)

@app.route('/course/<int:course_id>/<path:course_title>', methods=['GET', 'POST'])
@login_required
def course(course_id, course_title):

    decoded_course_title = course_title.replace('-', ' ')

    lessons = Lessons.query.filter_by(course_id=course_id).all()

    lessons_titles = [{'id':lesson.id, 'title': lesson.title} for lesson in lessons]

    return render_template('course.html', lessons=lessons_titles, course_title=decoded_course_title)

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
    
@app.route('/api/generate_lessons', methods=['POST'])
@login_required
def generate_lessons():
    try:
        request_data = request.get_json()

        course_title = request_data.get('course_title')
        course_id = request_data.get('course_id')
        user_id = request_data.get('user_id')

        response = {
            'id': course_id,
            'course_title': course_title
        }

        existing_lesson = Lessons.query.filter_by(course_id=course_id).first()

        if existing_lesson:
            return jsonify(response), 201
        # Define the prompt template with revised instructions
        lesson_prompt_template = """
        You are creating a course for a user interested in learning about {course_title}. 
        Please provide proper number of lesson titles that would be suitable for this course, max to 5, and no other text, just lessons tiles, each prefixed with a number, don't write anything else.
        Example:
        1. Introduction to python
        2. Data types in python
        """
        
        # Populate the prompt with the user's topic
        prompt = lesson_prompt_template.format(course_title=course_title)

        # Generate response from the modelp

        response_llm = llm.invoke(prompt)

        lesson_titles = response_llm.split('\n')  # Split by new lines to get individual lesson titles

        # Create a list to store the lesson titles
        # lessons_list = [f"{title.strip()}." for title in lesson_titles if title.strip()]

        for lesson_title in lesson_titles:
            new_lesson = Lessons(title=lesson_title, course_id=course_id)
            db.session.add(new_lesson)
            db.session.commit()

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_content', methods=['POST'])
@login_required
def generate_content():

    # Retrieve data from incoming JSON request
    request_data = request.get_json()
    lesson_title = request_data.get('lesson_title')  # Get course title from request
    course_title = request_data.get('course_title')
    lesson_id = request_data.get('lesson_id')
    user_id = request_data.get('user_id')  # Get user ID from request (assuming it's passed)
    # Define a prompt template to guide lesson content generation
    #
    #  within the course "{course_title}".

    existing_content = Lessons.query.filter_by(id=lesson_id).first().content

    if existing_content:
        return jsonify({'content': existing_content}), 200

    content_prompt_template = f"""
    Lesson: {lesson_title}"

    **Lesson Overview:**
    In this lesson, we will delve into the key topics related to "{lesson_title}" in "{course_title}", Please provide detailed content covering the following aspects within the course "{course_title}":

    **Key Topics to Cover:**
    1. 
    2. 
    3. 

    **Examples and Explanations:**
    - Please include illustrative examples to clarify the concepts.
    - Provide detailed explanations to ensure comprehension.

    **Exercises:**
    - Develop exercises or problems related to the lesson topics.
    - Include solutions or hints where applicable.

    **Additional Notes:**
    Feel free to add any additional insights or details that would enhance this lesson.

    """

    prompt = content_prompt_template.format(lesson_title=lesson_title, course_title=course_title)

    response_llm = llm.invoke(prompt)

    lesson = Lessons.query.get(lesson_id)

    if lesson:
        # Update the lesson's content with the generated response
        lesson.content = response_llm

        # Commit the changes to the database
        db.session.commit()

        # Return a success response
        return jsonify({'content': response_llm}), 200
    else:
        # If lesson with the given lesson_id is not found
        return jsonify({'message': 'Lesson not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)