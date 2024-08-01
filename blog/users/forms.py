from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

from blog.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password',message='Passwords must match') ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user: # if the user already exists in the database then throw error
            raise ValidationError('That username is taken. Please choose a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different email')
        
# class ChangePasswordForm(FlaskForm):
#     current_password = PasswordField('Current Password', validators=[DataRequired()])
#     new_password = PasswordField('New Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo(new_password, message='New password and confirm password must be same.')])
    
#     def validate_new_password(self, new_password):
#         if bcrypt

class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Request password reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')