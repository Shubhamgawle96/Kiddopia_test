from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms.validators import InputRequired,Length,Email

class Form(FlaskForm):
    name = StringField('name', [validators.input_required(message="name field is required")])
    email = EmailField('Email', validators=[InputRequired(message="Email field is required"), Length(4, 128), Email()])


