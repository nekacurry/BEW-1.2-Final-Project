# Create your models here.
from sqlalchemy_utils import URLType

from game_app import db
from game_app.utils import FormEnum
from flask_login import UserMixin

class GameGenre(FormEnum):
  """Genres of games."""
  SHOOTER = 'Shooter'
  MMORPG = 'MMORPG'
  RPG = 'RPG'
  PUZZLE = 'Puzzle'
  ADVENTURE = 'Adventure'
  SURVIVAL = 'Survival'
  PARTY = 'Party'
  PLATFORMER = 'Platformer'
  MOBA = 'MOBA'
  OTHER = 'Other'

class System(db.Model):
  """Game System model."""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  games = db.relationship('Game', back_populates='system')
  added_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  added_by = db.relationship('User')

class Game(db.Model):
  """Game model."""
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), nullable=False)
  genre = db.Column(db.Enum(GameGenre), default=GameGenre.OTHER)
  photo_url = db.Column(URLType)
  system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)
  system = db.relationship('System', back_populates='games')
  added_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  added_by = db.relationship('User')

class User(UserMixin, db.Model):
  """User model."""
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(25), nullable=False)
  password = db.Column(db.String(80), nullable=False)
  