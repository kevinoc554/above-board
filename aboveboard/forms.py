from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField,
                     SubmitField, BooleanField,
                     TextAreaField, SelectField)
from wtforms.validators import (
    InputRequired, Length, Email, EqualTo, ValidationError)
from flask_login import current_user
import urllib3
from aboveboard import bcrypt, mongo