from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def config():
    DB_NAME = "database.db"
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwertzuioeter'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True