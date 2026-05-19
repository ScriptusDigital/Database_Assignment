from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


#====Registration and login ==#

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=2, max=150),
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Length(max=150),
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6),
        ]
    )

    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )

    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", 
        validators=[
            DataRequired(),
       
        ]
    )

    password = PasswordField(
        "Password", 
        validators=[
            DataRequired(),
        ]
    )

    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")