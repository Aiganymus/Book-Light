from main import app, allowed_file, secure_filename, bcrypt
from main.models import User, db
from flask import request, jsonify, make_response, redirect
from main.schemas import UserSchema
import os
from main.routes import token_required

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return make_response(jsonify({'users': result}))


@app.route('/user/<int:pk>', methods=['GET'])
def get_one_user(pk):
    user = User.query.get_or_404(pk)
    user_result = user_schema.dump(user)
    return make_response(jsonify({'user': user_result}))


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = user_schema.dump(User.query.filter_by(email=data['email']).first())
    if not data:
        return make_response(jsonify({'message': 'No input data provided'})), 400
    if user:
        return make_response(jsonify({'message': 'User with such email already exists!'})), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('UTF-8')

    new_user = User(
        contactName=data['contactName'],
        password=hashed_password,
        email=data['email'],
        phoneNumber=data['phoneNumber']
    )

    if 'imageFile' in request.files:
        file = request.files['imageFile']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_PROFPIC_FOLDER'], filename))
            new_user.imageFile = filename

    db.session.add(new_user)
    db.session.commit()
    result = user_schema.dump(new_user)
    return make_response(jsonify({'message': 'New user created!', 'user': result})), 201


@app.route('/user', methods=['DELETE'])
@token_required
def delete_user(current_user):
    user = User.query.get_or_404(current_user.id)

    db.session.delete(user)
    db.session.commit()

    return make_response(jsonify({'message': 'The user has been deleted!'}))