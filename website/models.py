from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(5), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    notes = db.relationship('Note')
    rules = db.relationship('User_rules')


class User_rules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rules = db.Column(db.String(12))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class email_received(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(150))
    receiver = db.Column(db.String(150))
    subject = db.Column(db.String(150))
    text = db.Column(db.String(10000))
    html = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    email = db.relationship('Ticket')


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey('email_received.id'))
    note = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    Owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


