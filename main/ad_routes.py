from main import app
from main.models import Ad, db
from flask import request, jsonify, make_response
from main.schemas import AdSchema

ad_schema = AdSchema()
ads_schema = AdSchema(many=True)


@app.route('/ad', methods=['GET'])
def get_all_ads():
    ads = Ad.query.all()
    result = ads_schema.dump(ads)
    return make_response(jsonify({'ads': result}))


@app.route('/ad/<int:pk>', methods=['GET'])
def get_one_ad(pk):
    ad = Ad.query.get_or_404(pk)
    ad_result = ad_schema.dump(ad)
    return make_response(jsonify({'ad': ad_result}))


# @app.route('/user', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     if not data:
#         return make_response(jsonify({'message': 'No input data provided'})), 400
#     if User.query.filter_by(email=data['email']):
#         return make_response(jsonify({'message': 'User with such email already exists!'})), 400
#     hashed_password = bcrypt.generate_password_hash(data['password']).decode('UTF-8')
#     new_user = User(
#         contactName=data['contactName'],
#         password=hashed_password,
#         email=data['email'],
#         phoneNumber=data['phoneNumber']
#     )
#     db.session.add(new_user)
#     db.session.commit()
#
#     return make_response(jsonify({'message': 'New user created!'})), 201
#
#
# @app.route('/user/<int:pk>', methods=['DELETE'])
# def delete_user(pk):
#     user = User.query.get_or_404(pk)
#
#     db.session.delete(user)
#     db.session.commit()
#
#     return make_response(jsonify({'message': 'The user has been deleted!'}))