from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, validators


class RegistrationForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=5, max=20)])
    email = EmailField("Email", [validators.Email()]) 
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=5, message="Too Short, minimum 5 characters"), 
                validators.EqualTo("confirm_password", message="Passwords must match")])
    confirm_password = PasswordField("Repeat Password", [validators.DataRequired(), validators.EqualTo("password", message="Passwords must match")])
    submit = SubmitField("Sign Up")
    
    
class LoginForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
