from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import app, db, bcrypt
from app.models.models import Users
from app.forms.forms import LoginForm, RegisterForm
from app.utils.helpers import login_required_redirect_dashboard, allowed_file
import os

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
        new_user = Users(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data,
            birthdate=form.birthdate.data,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 