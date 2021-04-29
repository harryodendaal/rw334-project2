from flask import Blueprint, json, request, jsonify, make_response
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .database.models.user import BlacklistToken, User
from .database.models import db
import jwt
import datetime
from flaskapp import app

auth = Blueprint('auth', __name__)

def token_required(func):
  @wraps(func)
  def decorated(*args,**kwargs):
    token = None
    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']
    if not token:
      return jsonify({"message":"Token is missing!"}), 401
    data = jwt.decode(token,  app.config.get("SECRET_KEY"), algorithms='HS256')
    try:
      current_user = User.query.filter_by(id=data['sub']).first()
    except:
      return jsonify({'message':'Token is invalid!'}), 401
    return func(current_user, *args, **kwargs)
  return decorated


@auth.route('/hello',methods=['POST', 'GET'])
def hello():
  return {"message":"hello"}

@auth.route('/register', methods=['POST'])
def register():
  #get post data
  data = request.get_json()
  #check if user already exists
  user = User.query.filter_by(username=data.get('email')).first()
  if not user:
    try:
      hashed_password = generate_password_hash(data['password'], method='sha256')
      user = User(
        username=data['username'],
        password=hashed_password
      )
      #insert user
      db.session.add(user)
      db.session.commit()
      #generte the auth token
      auth_token = user.encode_auth_token(user.id)
      responseObject = {
        'message':'Registration Completed',
        'access_token':auth_token.decode()
      }
      return make_response(jsonify(responseObject)),201
    except Exception as e:
      print(e)
      message = ""
      if str(e).find('duplicate'):
        message = 'Unique key constraint invalidated'
      else:
        message = "maybe not respecting table rules? working on errors..."
      responseObject = {
        'message':message
      }
      return make_response(jsonify(responseObject)),401
  else:
    responseObject = {
      'message':'Some error occured'
    }
    return make_response(jsonify(responseObject)), 202


@auth.route('/login',methods=['POST'])
def login():
  # auth data
  auth = request.get_json()
  username = auth['username']
  password = auth['password']

  try:

    user:User = User.query.filter_by(
      username=username
    ).first()
    if user and check_password_hash(
      user.password, password=password
    ):
      auth_token = user.encode_auth_token(user.id)
      if auth_token:
        responseObject = {
          'message':'Succesfully logged in.',
          'access_token': auth_token
        }
        return make_response(jsonify(responseObject)),200
    else:
      responseObject = {
        'message':'User does not exist'
      }
      return make_response(jsonify(responseObject)), 404
  except Exception as e:
    print(e)
    responseObject = {
      "message":"Woor just happened"
    }
    return make_response(jsonify(responseObject)), 500


@auth.route('/logout',methods=['POST'])
@token_required
def logout(current_user):
  auth_token =  request.headers['x-access-token']
  if auth_token:
    resp = User.decode_auth_token(auth_token)
    if not isinstance(resp, str):
      print('ye')
      # decode_auth_token returned not string
      # thus not blacklisted yet
      
      # blacklist token
      blacklisted_token = BlacklistToken(token=auth_token)
      try:
        # insert the token
        db.session.add(blacklisted_token)
        db.session.commit()
        responseObject = {
          'message':'Logging out'
        }
        return make_response(jsonify(responseObject)), 200
      except Exception as e:
        responseObject = {
          'message':e
        }
        return make_response(jsonify(responseObject)), 400
    else:
      print('ye2')
      responseObject = {
        'message':resp
      }
      return make_response(jsonify(responseObject)), 200
  else:
    responseObject = {
      'message':'non valid auth token'
    }

    return make_response(jsonify(responseObject)), 403


@auth.route('/secure', methods=['GET'])
@token_required
def secure(current_user):
  return jsonify({"message":"Success"})

# supersecret needs to be enviorment variable