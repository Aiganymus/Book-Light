from main import app, r
from main.models import *
from flask import request, jsonify, make_response
from main.schemas import AdSchema, UserSchema, BookSchema
from main.routes import token_required
import json

user_schema = UserSchema()
ad_schema = AdSchema()
ads_schema = AdSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route('/ad', methods=['GET'])
def get_all_ads():
    ads = Ad.query.all()
    result = ads_schema.dump(ads)
    return make_response(jsonify({'ads': result}))


@app.route('/ad/<int:pk>', methods=['GET'])
def get_one_ad(pk):
    ad = Ad.query.get_or_404(pk)
    ad_result = ad_schema.dump(ad)
    user_result = user_schema.dump(ad.author)
    return make_response(jsonify({'ad': ad_result, 'user': user_result}))


@app.route('/ad', methods=['POST'])
@token_required
def create_ad(current_user):
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'No input data provided'})), 400
    print(data)
    new_ad = Ad(
        title=data['title'],
        description=data['description'],
        userId=current_user.id
    )

    db.session.add(new_ad)
    db.session.flush()

    new_book = Book(
        title=data['book']['title'],
        price=data['book']['price'],
        adId=new_ad.id
    )

    db.session.add(new_book)
    db.session.flush()

    key = new_book.title.lower()  # key fo redis list
    value = json.dumps(ad_schema.dump(new_ad))  # from json to string
    r.lpush(key, value)  # push to the head of list
    r.ltrim(key, 0, 9)  # leave only 10 ads

    db.session.commit()

    return make_response(jsonify({'message': 'New ad created!'})), 201


@app.route('/user/<int:pk>', methods=['DELETE'])
@token_required
def delete_ad(current_user, pk):
    ad = Ad.query.get_or_404(pk)
    if current_user.id != ad.userId:
        return make_response(jsonify({'message': 'Access denied.'})), 401
    db.session.delete(ad)
    db.session.commit()

    return make_response(jsonify({'message': 'The ad has been deleted!'}))


@app.route('/search', methods=['GET'])
def search():
    data = request.get_json()
    name = data['title']
    books = Book.query.filter(Book.title.ilike('%'+name+'%')).all()
    ads = [book.ad for book in books]
    result = ads_schema.dump(list(set(ads)))
    return make_response(jsonify({'ads': result}))
