from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField,
                     SubmitField, BooleanField,
                     TextAreaField, SelectField)
from wtforms.validators import (
    InputRequired, Length, Email, EqualTo, ValidationError)
from flask_login import current_user
import urllib3
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

    def validate_password(self, password):
        """
        Checks if password contains:
        - At least 1 lower case letter
        - At least 1 Uppercase letter
        - At leaset 1 number
        - At least 1 symbol: ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        """
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        if not any(char.islower() for char in self.password.data):
            raise ValidationError(
                'Password should have at least one lowercase letter')

        if not any(char.isupper() for char in self.password.data):
            raise ValidationError(
                'Password should have at least one UPPERCASE letter')

        if not any(char.isdigit() for char in self.password.data):
            raise ValidationError(
                'Password should have at least one number')

        if not any(char in symbols for char in self.password.data):
            raise ValidationError(
                'Password should have at least one of the symbols: !@#$%^&*()')

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


class AddGameForm(FlaskForm):
    title = StringField('Title',
                        validators=[InputRequired()])
    designer = StringField('Designer',
                           validators=[InputRequired()])
    publisher = StringField('Publisher',
                            validators=[InputRequired()])
    genre = SelectField('Genre', validators=[InputRequired()])
    mechanics = SelectField('Game Mechanics', validators=[InputRequired()])
    player_count = StringField('Player Count',
                               validators=[InputRequired()])
    rating = SelectField('Rating', choices=['Rate this game', 1, 2, 3, 4, 5],
                         validators=[InputRequired()])
    weight = SelectField('Weight', choices=[
        'How complex is this game?', 1, 2, 3, 4, 5],
        validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image_link = StringField('Box Art Image URL')
    submit = SubmitField('Add Game!')

    def make_dict(self):
        """
        Convert form response to dict to facilitate creating Game instance
        """
        info = {
            "title": self.title.data,
            "designer": self.designer.data,
            "publisher": self.publisher.data,
            "genre": self.genre.data,
            "mechanics": self.mechanics.data,
            "player_count": self.player_count.data,
            "rating": self.rating.data,
            "weight": self.weight.data,
            "description": self.description.data,
            "image_link": self.image_link.data,
        }
        return info

    def validate_image_link(self, image_link):
        """
        Validate the image link to check that it is a valid URL
        with a content type of JPEG or JPG.

        Does not raise error if field is blank (as placeholder will be
        applied).
        """
        if self.image_link.data:
            content_types = ['image/jpeg', 'image/jpg']
            http = urllib3.PoolManager()
            try:
                r = http.request('GET', self.image_link.data)
            except Exception:
                raise ValidationError(
                    'Text provided is not a URL. Please try again.')
            else:
                response = r.info()
                if response['Content-Type'] not in content_types:
                    raise ValidationError(
                        'Must be a valid URL to an image in JPEG/JPG format')


class EditGameForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    designer = StringField('Designer',
                           validators=[InputRequired()])
    publisher = StringField('Publisher',
                            validators=[InputRequired()])
    weight = SelectField('Weight', choices=[
        'How complex is this game?', 1, 2, 3, 4, 5],
        validators=[InputRequired()])
    player_count = StringField('Player Count',
                               validators=[InputRequired()])
    image_link = StringField('Box Art Image URL')
    description = TextAreaField('Description',
                                validators=[InputRequired()])
    submit = SubmitField('Update Info!')

    def validate_image_link(self, image_link):
        """
        Validate the image link to check that it is a valid URL
        with a content type of JPEG or JPG.

        Does not raise error if field is blank (as placeholder will be
        applied), or if placeholder is already used.
        """
        placeholds = [
            'https://via.placeholder.com/250x200?text=No+Box+Art+Provided',
            ''
        ]
        if self.image_link.data not in placeholds:
            content_types = ['image/jpeg', 'image/jpg']
            http = urllib3.PoolManager()
            try:
                r = http.request('GET', self.image_link.data)
            except Exception:
                raise ValidationError(
                    'Text provided is not a URL. Please try again.')
            else:
                response = r.info()
                if response['Content-Type'] not in content_types:
                    raise ValidationError(
                        'Must be a valid URL to an image in JPEG/JPG format')

    def set_form_data(self, game):
        """
        Collects data from game to populate the form on load
        """
        self.title.data = game['title']
        self.designer.data = game['designer']
        self.publisher.data = game['publisher']
        self.weight.data = game['weight']
        self.player_count.data = game['player_count']
        self.description.data = game['description']
        self.image_link.data = game['image_link']

    def collect_changes(self):
        """
        Collects the responses from the for, and gathers them into a dict
        to be passed to the db.
        If image link is left blank, uses placeholder.
        """
        placehold = 'https://via.placeholder.com/250x200?text=No+Box+Art+Provided'
        if self.image_link.data == '':
            self.image_link.data = placehold
        changes = {
            'title': self.title.data,
            'designer': self.designer.data,
            'publisher': self.publisher.data,
            'weight': self.weight.data,
            'description': self.description.data,
            'image_link': self.image_link.data,
            'player_count': self.player_count.data
        }
        return changes


class SearchForm(FlaskForm):
    query = StringField('Search Games',
                        validators=[InputRequired(), Length(min=2)])
    submit = SubmitField('Search')
