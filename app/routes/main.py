from flask import render_template
from flask_login import login_required, current_user
from app import app
from app.models.models import LearningPaths, Courses, Lessons

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    learning_paths = current_user.learning_paths
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
    lessons_titles = [{'id':lesson.id, 'title': lesson.title, 'completed': lesson.completed} for lesson in lessons]
    return render_template('course.html', lessons=lessons_titles, course_title=decoded_course_title) 