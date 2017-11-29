# models.py


import datetime
from app import db


class Chat(db.Model):

    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id):
        self.id = id


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)

    def __init__(self, text):
        self.text = text
