from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


#====Registration and login ==#

class RegistationForm(FlaskForm):
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
            Email(),
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

    confirmpassword = PasswordField(
        "Confirm_password",
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
            Email(),
        ]
    )

    password = PasswordField(
        "Password", 
        validators=[
            DataRequired(),
            Email(),
        ]
    )

    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")