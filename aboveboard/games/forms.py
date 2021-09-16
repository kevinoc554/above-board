from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField,
                     TextAreaField, SelectField)
from wtforms.validators import (
    InputRequired, Length, ValidationError)
import urllib3


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
        Convert form response to dict to facilitate creating Game instance.
        Stores rating as an int in a list.
        """
        info = {
            "title": self.title.data,
            "designer": self.designer.data,
            "publisher": self.publisher.data,
            "genre": self.genre.data,
            "mechanics": self.mechanics.data,
            "player_count": self.player_count.data,
            "rating": [int(self.rating.data)],
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
