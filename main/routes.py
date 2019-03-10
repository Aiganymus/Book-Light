from main import app, bcrypt
from main.models import *
from flask import request, jsonify, make_response
import jwt
from functools import wraps
import datetime
from main.schemas import UserSchema


user_schema = UserSchema()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.get(data['id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    auth = request.get_json()
    print(auth)
    if not auth or not auth['email'] or not auth['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth['email']).first()

    if not user:
        return make_response('Such user doesn\'t exist', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if bcrypt.check_password_hash(user.password, auth['password']):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        result = user_schema.dump(user)
        return jsonify({'token': token.decode('UTF-8'), 'userId': result['id']})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})