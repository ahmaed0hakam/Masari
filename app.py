import os
import pdfplumber

import re
from flask import Flask, flash, render_template, redirect, url_for, request, jsonify
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, FileField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_cors import CORS


#############################################
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_core.output_parsers import StrOutputParser
#############################################

from flask import request
from werkzeug.utils import secure_filename

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'My|!w>YD/IT[&iE}?yV#>;}Xf]^7YgLV'
app.config['UPLOAD_FOLDER'] = 'CVs'

# Define the Ollama model and callback manager
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = Ollama(model="llama3", callbacks=callback_manager, verbose=True)
output_parser = StrOutputParser()


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.init_app(app)
login_manager.login_view = 'login'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx'}


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
    pdf_path = db.Column(db.String(150))  # Path to the CV file


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
    completed = db.Column(db.Boolean, default=0, nullable=False)


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Name"})
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=6)], render_kw={"placeholder": "Confirm Password"})
    birthdate = DateField('Birth Date', validators=[InputRequired()], render_kw={"placeholder": "Birth Date"})
    cv = FileField('CV Resume', validators=[InputRequired()], render_kw={"placeholder": "Upload CV"})
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
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # cv_file = request.files['cv']
        # if cv_file and allowed_file(cv_file.filename):
        #     filename = secure_filename(cv_file.filename)
        #     cv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #     cv_file.save(cv_path)
        new_user = Users(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data,
            birthdate=form.birthdate.data,
            # pdf_path=cv_path 
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        flash('Invalid file type.')
    return render_template('register.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    learning_paths = current_user.learning_paths
    # courses = current_user.courses
    return render_template('dashboard.html', name=current_user.name, learning_paths=learning_paths)

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
    print(lessons)

    lessons_titles = [{'id':lesson.id, 'title': lesson.title, 'completed': lesson.completed} for lesson in lessons]

    return render_template('course.html', lessons=lessons_titles, course_title=decoded_course_title)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


import re

def parse_prompt(input_text):
    # This pattern matches lines starting with a number, a period, and captures the course title
    pattern = r'^\d+\.\s(.+)$'
    
    # Find all occurrences of the pattern
    courses = re.findall(pattern, input_text, re.MULTILINE)
    return courses




@app.route('/api/generate_learningpath', methods=['POST'])
@login_required
def generate_learning_path():

    try:

        request_data = request.get_json()

        lp_title = request_data.get('text')
        user_id = request_data.get('user_id')

        print("LOGGING...\n\t\tbefore prompt")

        # path_id = generate_path(text, user_id)

        # Define the prompt template with revised instructions
        prompt_template = """
        You are creating a personalized learning path for a user interested in {lp_title}. 
        Please provide the courses names only, ordered based on difficulty and correct ordering in the learning path, no another text in the string, only the courses names:

        ## **Generate Output**:
        Format the output to list only the names of the recommended courses under the header Personalized Learning Path: [Learning Path Name].
        Ensure the output adheres strictly to the format provided, without including any descriptive text, comments, or conversational elements.

        ## **Output Format:**
        ```
        # Personalized Learning Path: [Learning Path Name]
        1. [Course Name 1]
        2. [Course Name 2]
        3. (repeat as necessary for additional courses)
        ```
    """

        # Populate the prompt with the user's topic
        prompt = prompt_template.format(lp_title=lp_title)

        response_llm = llm.invoke(prompt)

        print("LOGGING...\n\t\tafter llm")


        courses_titles = parse_prompt(response_llm)
        new_path = LearningPaths(title=lp_title, user_id=current_user.id)
        db.session.add(new_path)
        db.session.commit()


        for course in courses_titles:
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

        response = {
            'id': course_id,
            'course_title': course_title
        }

        existing_lesson = Lessons.query.filter_by(course_id=course_id).first()

        if existing_lesson:
            return jsonify(response), 201
        learning_paths = current_user.learning_paths
        # Prompt template for course recommendation
        lesson_prompt_template = """
# Generating a Personalized Lessons 
You are creating a course for a user interested in learning about {course_title}, This course from this learning paths {learning_paths}. 
Please provide proper number of lesson titles that would be suitable for this course, and no other text, just lessons tiles, each prefixed with a number, don't write anything else.

## **Generate Output**:
Format the output to list only the names of the recommended lessons title from course {course_title} under the header Personalized Lessons Of Course: {course_title}.
Ensure the output adheres strictly to the format provided, without including any descriptive text, comments, or conversational elements.

## **Output Format:**
```
# Personalized Learning Path: [Course Name]
1. [Lesson Name 1]
2. [Lesson Name 2]
3. (repeat as necessary for additional Lessons)
```

## instructions
        """

        # Populate the prompt with the user's topic
        prompt = lesson_prompt_template.format(course_title=course_title, learning_paths=learning_paths)

        response_llm = llm.invoke(prompt)

        lesson_titles = parse_prompt(response_llm)

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

    existing_content = Lessons.query.filter_by(id=lesson_id).first().content

    if existing_content:
        return jsonify({'content': existing_content}), 200
    learning_paths = current_user.learning_paths

    content_prompt_template = f"""

    Lesson: {lesson_title}"

    Lesson Overview:
    In this lesson, we will delve into the key topics related to "{lesson_title}" in "{course_title}", Please provide detailed content covering the following aspects within the course "{course_title}":

    Key Topics to Cover:
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
    
    **Instructions:**
    - Do not use (Here Markdown) or (Here XYZ) or any form of conversations just give me the content without any additional conversations   
    - Design a Markdown template focusing on individual lessons within a course.

    **Content Details:**
    - _[Provide detailed descriptions of the main topics and any critical content covered in this lesson.]_
"""
    prompt = content_prompt_template.format(lesson_title=lesson_title, course_title=course_title, learning_paths=learning_paths)
    print(prompt)
    response_llm = llm.invoke(prompt)
    response_llm = response_llm.replace("```html", "").replace("```", "").strip()
    current_lesson = Lessons.query.get(lesson_id)

    if current_lesson:
        # Update the null lesson's content with the generated response
        current_lesson.content = response_llm

        db.session.commit()

        return jsonify({'content': response_llm}), 200
    else:
        return jsonify({'message': 'Lesson not found'}), 404
    
@app.route('/api/generate_reply', methods=['POST'])
@login_required
def generate_reply():

    # Retrieve data from incoming JSON request
    request_data = request.get_json()
    user_input = request_data.get('user_input')
    lesson_id = request_data.get('lesson_id')
    print("my lesson id", lesson_id)
    content = Lessons.query.get(lesson_id).content


    context_template = f"""
        You are a learning assistant designed to provide accurate and helpful information. 
        Please use the following details to answer the question provided as short as possible, max to 20 character. 
        If you're unsure about any details, it's important to be honest and precise rather than guessing.

        *Instructions:*
        - Do not use (Here XYZ) or any form of conversations just give me the Answer without any additional conversations  

        
        Depend on this content and your information:
        
        {content}
        

        Answer this question:
        Question: {user_input}

        Helpful Answer:"""


    response_llm = llm.invoke(context_template)

    return jsonify({'reply': response_llm}), 200

@app.route('/api/mark_completed', methods=['POST'])
@login_required
def mark_completed():

    # Retrieve data from incoming JSON request
    request_data = request.get_json()
    lesson_id = request_data.get('lesson_id')

    current_lesson = Lessons.query.get(lesson_id)

    if current_lesson:
        # Update the null lesson's content with the generated response
        current_lesson.completed = 1

        db.session.commit()

        return jsonify({'message': f"lesson {lesson_id} completed"}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)