from . import db
import jwt
import datetime
from flaskapp import app
class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True)
  password = db.Column(db.String())

  def __repr__(self) -> str:
      return  '<User {}>'.format(self.username)

  def encode_auth_token(self, user_id):
    # generates the Auth Token
    try:
      payload = {
        'exp':datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30, seconds=10),
        'iat': datetime.datetime.utcnow(),
        'sub':user_id
      }
      return jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
      )
    except Exception as e:
      return e
    
  @staticmethod
  def decode_auth_token(auth_token):
    # validate the auth token
    try:
      payload =jwt.decode(auth_token,  app.config.get("SECRET_KEY"), algorithms='HS256')
      print("the payload is : ", payload)
      is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
      if is_blacklisted_token:
        return 'Token blacklist (loggedout). Please login again.'
      else:
        return payload['sub']
    except jwt.ExpiredSignatureError:
      return 'Signature expired'
    except jwt.InvalidTokenError:
      return 'Invalid token'


class BlacklistToken(db.Model):
  """
  Token Model for storing JWT tokens
  """
  __tablename__ = 'blacklist_tokens'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  token = db.Column(db.String(500), unique=True, nullable=False)
  blacklisted_on = db.Column(db.DateTime, nullable=False)

  def __init__(self, token):
    self.token = token
    self.blacklisted_on = datetime.datetime.now()

  def __repr__(self):
    return '<id: token: {}'.format(self.token)

  @staticmethod
  def check_blacklist(auth_token):
    # check whether auth token has been blacklisted
    res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
    if res:
      return True
    else:
      return False