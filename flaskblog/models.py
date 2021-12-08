'''
Date: 2021-11-29 14:51:18
LastEditors: GC
LastEditTime: 2021-12-05 14:15:30
FilePath: \Flask-Blog-Project2\flaskblog\models.py
'''
from flaskblog import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime
from flask import current_app


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
    # What the backref allows us to do is when we have a post, we can simply use this author attribute to get the user who
    #   create the post

    # Create tokens:

    def get_reset_token(self, expires_sec=1800):
        # Create a serializer object and we are simply setting this up with our secret key and an expiration time:
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)

        # Return this token which is created by the dumps method and it also contains the payload of the current user id.
        return s.dumps({"user_id": self.id}).decode("utf-8")

    # Verify the token we created:

    @staticmethod
    def verify_reset_token(token):
        # Create a serializer object
        s = Serializer(current_app.config['SECRET_KEY'])

        # And we could get an exception when we try to load this token. The token could be invalid or the time could be expired.
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{ self.username }', '{ self.email }', '{ self.image_file }')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
