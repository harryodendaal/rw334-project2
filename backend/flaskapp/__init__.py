from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path
from . import config

from .database.models import db
app = Flask(__name__)

def create_app():
  CORS(app, resources={r"/*": {"origins": "*"}})
  app.config['SECRET_KEY'] = 'SUPERSECRET'
  app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)

  from .auth import auth
  app.register_blueprint(auth, url_prefix='/')

  db.create_all(app=app)

  return app