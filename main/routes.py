from main import app
from main.models import *
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from main import bcrypt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/users', methods=['GET'])
@token_required
def get_all_users():

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['contact_name'] = user.contact_name
        user_data['password'] = user.password
        user_data['email'] = user.email
        user_data['phone_number'] = user.phone_number
        user_data['image_file'] = user.image_file
        user_data['ads'] = user.ads
        output.append(user_data)

    return jsonify(output)


@app.route('/users/<id>', methods=['GET'])
def get_one_user(id):
    print(request.args['foo'])
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['id'] = user.id
    user_data['contactName'] = user.contactName
    user_data['password'] = user.password
    user_data['email'] = user.email
    user_data['phoneNumber'] = user.phoneNumber
    user_data['imageFile'] = user.imageFile

    return jsonify(user_data)


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('UTF-8')

    new_user = User(contactName=data['contactName'], password=hashed_password, email=data['email'], phoneNumber=data['phoneNumber'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(contactName=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

