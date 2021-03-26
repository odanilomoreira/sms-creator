from sql_alchemy import db
from flask import request, url_for
from requests import post
from send_email import confrm_email

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)
    restaurant_id = db.Column(db.String(80), db.ForeignKey('restaurants.restaurant_id'))

    def __init__(self, username, password, email, restaurant_id, activated):
        self.username = username
        self.password = password
        self.email = email
        self.activated = activated
        self.restaurant_id = restaurant_id

    def send_confirmation_email(self):
        # http://127.0.0.1:5000/confirm/{user_id}
        confirmation_link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        confrm_email(self.email,confirmation_link)

    def json(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'restaurant_id': self.restaurant_id,
            'activated': self.activated
            }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user:
            return user
        return None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
