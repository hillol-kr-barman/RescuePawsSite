from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    name = StringField("Full Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password",
                             validators=[InputRequired()])
    conf_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password", message="Passwods don't match!")])
    submit = SubmitField("Sign Up")


class ModifyPet(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired()])
    bio = StringField('Bio', validators=[InputRequired()])
    edit_pet = SubmitField("Edit Pet")
    new_pet = SubmitField("Add New Pet")

