from main import app
from main.models import User, db
from flask import request, jsonify, make_response
from main import bcrypt
from main.schemas import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return make_response(jsonify({'users': result}))


@app.route('/user/<int:pk>', methods=['GET'])
def get_one_user(pk):
    # print(request.args['foo'])
    user = User.query.get_or_404(pk)
    user_result = user_schema.dump(user)
    return make_response(jsonify({'user': user_result}))


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'No input data provided'})), 400
    if User.query.filter_by(email=data['email']):
        return make_response(jsonify({'message': 'User with such email already exists!'})), 400
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('UTF-8')
    new_user = User(
        contactName=data['contactName'],
        password=hashed_password,
        email=data['email'],
        phoneNumber=data['phoneNumber']
    )
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({'message': 'New user created!'})), 201


@app.route('/user/<int:pk>', methods=['DELETE'])
def delete_user(pk):
    user = User.query.get_or_404(pk)

    db.session.delete(user)
    db.session.commit()

    return make_response(jsonify({'message': 'The user has been deleted!'}))