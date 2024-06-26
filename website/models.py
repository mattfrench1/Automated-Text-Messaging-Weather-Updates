from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(150))
    lat = db.Column(db.String(150))
    long = db.Column(db.String(150))
    pollen = db.Column(db.String(150))
    air_quality = db.Column(db.String(150))
    forecast = db.Column(db.String(150))
    solar = db.Column(db.String(150))
    phone_number = db.Column(db.String(150), unique=True)
    phone_provider = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))