from . import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True)
  password = db.Column(db.String(20))

  def __repr__(self) -> str:
      return  '<User {}>'.format(self.username)