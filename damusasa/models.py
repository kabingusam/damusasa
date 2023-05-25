from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from damusasa import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    interests = db.relationship('Interest', backref='user', lazy=True)
    google_id = db.Column(db.String(50), unique=True, nullable=True)