from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()

DB_NAME = 'database.db'

def create_app():
  app = Flask(__name__)
  CORS(app, resources={r"/*": {"origins": "*"}})
  secret = app.config['SECRET_KEY'] = 'SUPERSECRET'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/harry/Documents/CompSci_334/Project_2/22794484-rw334-project-2/backend/todo.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)

  from .auth import auth
  app.register_blueprint(auth, url_prefix='/')

  if not path.exists('flaskapp/' + DB_NAME):
    db.create_all(app=app)
    print("Created Database!")

  return app