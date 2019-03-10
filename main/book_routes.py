from main import app, r
from flask import request, jsonify, make_response
from main.schemas import AdSchema
import json


ad_schema = AdSchema()
ads_schema = AdSchema(many=True)

# return new ads by book title
@app.route('/ad/new', methods=['GET'])
def get_ads_by_book_name():
    data = request.get_json()
    name = data['title'].lower()
    result = []

    for key in r.scan_iter('*'+name+'*'):
        title = key
        for ad in r.lrange(title, 0, -1):
            result.append(json.loads(ad.decode('utf-8')))

    return make_response(jsonify({'ads': result}))
