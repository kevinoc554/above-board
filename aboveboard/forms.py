from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    InputRequired, Length, Email, EqualTo, ValidationError)
from flask_login import current_user
from aboveboard import bcrypt, mongo


class RegistrationForm(FlaskForm):
    fname = StringField('First Name',
                        validators=[InputRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name',
                        validators=[InputRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[
        InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up!')

    def validate_username(self, username):
        """
        Checks if provided username is already in db.
        Fires as part of wtform's .validate_on_submit()
        """
        exisiting_username = mongo.db.users.find_one(
            {"username": self.username.data})
        if exisiting_username:
            raise ValidationError(
                'That username is already in use. Please choose a new one.')

    def validate_email(self, email):
        """
        Checks if provided email is already in db.
        Fires as part of wtform's .validate_on_submit()
        """
        exisiting_email = mongo.db.users.find_one(
            {"email": self.email.data})
        if exisiting_email:
            raise ValidationError(
                'That email is already in use. Please choose a new one.')

    def make_dict(self):
        """
        Takes response from form, hashes password
        and converts to dict to pass to User class
        """
        info = {
            "fname": self.fname.data,
            "lname": self.lname.data,
            "username": self.username.data,
            "email": self.email.data,
            "password": bcrypt.generate_password_hash(self.password.data)
                              .decode('utf-8')
        }
        return info


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    fname = StringField('First Name',
                        validators=[InputRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name',
                        validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    submit = SubmitField('Update!')

    def validate_email(self, email):
        """
        Checks if provided email is already in db. Will not trigger if email
        is unchanged. Fires as part of wtform's .validate_on_submit()
        """
        if self.email.data != current_user.email:
            exisiting_email = mongo.db.users.find_one(
                {"email": self.email.data})
            if exisiting_email:
                raise ValidationError(
                    'That email is already in use. Please choose a new one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        exisiting_email = mongo.db.users.find_one(
            {"email": self.email.data})
        if not exisiting_email:
            raise ValidationError(
                'Email not found. Please try again.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[
        InputRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
