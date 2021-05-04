from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from gampe_app.models import GameGenre, System

class SystemForm(FlaskForm):
    """Form for adding/updating a Game System."""

    name = StringField('Name')
    purchased = DateField('Date Purchased', format = '%m/%d/%Y')
    submit = SubmitField('Submit')

class GameForm(FlaskForm):
    """Form for adding/updating a Game."""

    title = StringField('Title')
    genre = SelectField('Genre', choices=GameGenre.choices())
    photo_url = StringField('Photo URL', validators=[URL()])
    purchased = DateField('Date Purchased', format = '%m/%d/%Y')
    system = QuerySelectField('System', query_factory=lambda: System.query.all())
    submit = SubmitField('Submit')