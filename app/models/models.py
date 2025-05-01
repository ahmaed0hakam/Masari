from flask_login import UserMixin
from app import db

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date)
    learning_paths = db.relationship('LearningPaths', backref='user', lazy=True)
    pdf_path = db.Column(db.String(150))

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
    learning_path = db.relationship('LearningPaths', backref='courses')

class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    course = db.relationship('Courses', backref=db.backref('lessons', lazy=True))
    completed = db.Column(db.Boolean, default=0, nullable=False) 