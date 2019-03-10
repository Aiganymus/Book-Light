from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

app = Flask(__name__)

UPLOAD_PROFPIC_FOLDER = '/media/profile_pics'
UPLOAD_FOLDER = '/media/ads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PROFPIC_FOLDER'] = UPLOAD_PROFPIC_FOLDER

POSTGRES = {
    'user': 'admin',
    'pw': 'password',
    'db': 'bookmarket_db',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.secret_key = 'cc9b142b232623024e898e8ca5aadd9b'

db = SQLAlchemy(app)

# from main.models import *
#
# db.create_all()


bcrypt = Bcrypt(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from main import user_routes
from main import ad_routes
from main import book_routes
from main import routes
from main.schemas import *

