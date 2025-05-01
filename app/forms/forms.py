from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, FileField
from wtforms.validators import InputRequired, Length, ValidationError
from app.models.models import Users

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