from sql_alchemy import db
from flask import request, url_for
from requests import post
from send_email import confrm_email

MAILGUN_DOMAIN = 'sandbox7405257bdaeb4b0791617210d2eabb5a.mailgun.org'
MAILGUN_API_KEY = 'key-5f9cfb789e009f8a171d01d6195149b0'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@sms-creator.com'

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, email, activated):
        self.username = username
        self.password = password
        self.email = email
        self.activated = activated

    def send_confirmation_email(self):
        # http://127.0.0.1:5000/confirm/{user_id}
        confirmation_link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        confrm_email(self.email,confirmation_link)

    def json(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
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
