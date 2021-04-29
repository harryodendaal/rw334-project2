from flask import Blueprint, json, request, jsonify, make_response
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .database.models.user import User
from .database.models.queries import get_all, add_instance, edit_instance, delete_instance, commit_changes
import jwt
import datetime


auth = Blueprint('auth', __name__)

def token_required(func):
  @wraps(func)
  def decorated(*args,**kwargs):
    token = None
    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']
    print("the token is: " , token)
    if not token:
      return jsonify({"message":"Token is missing!"}), 401
    data = jwt.decode(token, 'SUPERSECRET', algorithms='HS256')
    try:
      current_user = User.query.filter_by(id=data['id']).first()
    except:
      return jsonify({'message':'Token is invalid!'}), 401
    return func(current_user, *args, **kwargs)
  return decorated


@auth.route('/hello',methods=['POST', 'GET'])
def hello():
  return {"message":"hello"}

@auth.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  hashed_password = generate_password_hash(data['password'], method='sha256')
  add_instance(User, username=data['username'], password=data['password'])
  commit_changes()
  return jsonify({"message":"User Created"})


@auth.route('/login',methods=['POST'])
def login():
  print('hello')
  auth = request.get_json()
  username = auth['username']
  password = auth['password']
  if not auth or not username or not password:
    return jsonify({'message' : 'could not verify'})

  user = User.query.filter_by(username=username).first()
  if not user:
    return jsonify({'message' : 'could not verify'})

  if check_password_hash(user.password, password):
    token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'SUPERSECRET', algorithm='HS256')
    return jsonify({'token' : token})

  return jsonify({'message' : 'could not verify'})

@auth.route('/users', methods=['GET'])
def returnUsers():
  users = get_all(User)
  all_users = []
  for user in users:
    new_user = {
      "username":user.username
    }

    all_users.append(new_user)
  return json.dumps(all_users),200

@auth.route('/secure', methods=['GET'])
@token_required
def secure(current_user):
  return jsonify({"message":"Success"})

# supersecret needs to be enviorment variable