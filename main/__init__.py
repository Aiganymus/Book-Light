from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)

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


from main import routes