from main import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contactName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    imageFile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    phoneNumber = db.Column(db.String(12), nullable=False, unique=True)
    ads = db.relationship('Ad', backref='author', lazy=True, cascade="delete")

    def __repr__(self):
        return f"User('{self.contactName}', '{self.email}', '{self.phoneNumber}')"


payingTypes = db.Table('adPayingTypes',
    db.Column('adId', db.Integer, db.ForeignKey('ad.id'), primary_key=True),
    db.Column('payingTypeId', db.Integer, db.ForeignKey('paying_types.id'), primary_key=True)
)


class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    images = db.relationship('Image', backref='author', lazy=True, cascade="delete")
    payingTypes = db.relationship('PayingType', secondary=payingTypes, lazy='subquery',
                           backref=db.backref('ads', lazy=True), cascade="delete")
    books = db.relationship('Book', backref='ad', lazy=True, cascade="delete")

    def __repr__(self):
        return f"Post('{self.title}', '{self.datePosted}')"


class PayingType(db.Model):
    __tablename__ = 'paying_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), unique=True, nullable=False)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageFile = db.Column(db.String(20))
    adId = db.Column(db.Integer, db.ForeignKey('ad.id'), nullable=False)


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    adId = db.Column(db.Integer, db.ForeignKey('ad.id'), nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer)
    adId = db.Column(db.Integer, db.ForeignKey('ad.id'), nullable=False)
