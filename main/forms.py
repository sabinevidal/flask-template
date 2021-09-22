from flask_wtf import FlaskForm
from wtforms import Form, Field, BooleanField, StringField, IntegerField, validators
from wtforms.fields.core import FormField
from wtforms.fields.simple import HiddenField
from wtforms.widgets import TextInput
from .models import *
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

class ExampleForm(FlaskForm):
    name = StringField()
    email = StringField()