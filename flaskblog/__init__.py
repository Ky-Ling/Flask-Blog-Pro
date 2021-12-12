# from flask import Flask
# # from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from os import path
# from flask_mail import Mail
# import os


# db = SQLAlchemy()
# DB_NAME = "database.db"

# class Config:
#     # To use these forms, we need to set a secret key for our application. Secret key will protect against modifying cookies and
#     #   cross-site request forgery attacks and things like that.
#     SECRET_KEY = "helloworld"
#     SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     SQLALCHEMY_COMMIT_TEARDOWN = True

#     @staticmethod
#     def init_app(app):
#         pass


# def create_app():
#     app = Flask(__name__)

#     app.config.from_object(Config)
#     Config.init_app(app)

#     mail_configuration(app)

#     db.init_app(app)

#     # from .routes import auth
#     # app.register_blueprint(auth, url_prefix="/")

#     # Before we create our database, we need to import all the models individually that we want to be created in our database.
#     from .models import User, Post
#     create_database(app)

#     login_manager = LoginManager()
#     login_manager.login_view = "login"
#     login_manager.login_message_category = 'info'
#     login_manager.init_app(app)

#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))

#     return app


# def mail_configuration(app):
#     # Create some configurations for the mail server:
#     app.config["MAIL_SERVER"] = "smtp.googlemail.com"
#     app.config["MAIL_PORT"] = 587
#     # Gmail: 587
#     app.config["MAIL_USE_TLS"] = True
#     app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
#     app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")

#     mail = Mail(app)

#     return mail


# def create_database(app):
#     if path.exists("flaskblog/" + DB_NAME):
#         db.create_all(app=app)
#         print("Created database!!")



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from os import path
import os

db = SQLAlchemy()
DB_NAME = "database.db"
mail = Mail()

class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    @staticmethod
    def init_app(app):
        pass


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    db.init_app(app)
    # login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.main.routes import main
    from flaskblog.posts.routes import posts
    from flaskblog.users.routes import users
    from flaskblog.errors.handler import errors

    app.register_blueprint(users, url_prefix="/")
    app.register_blueprint(posts, url_prefix="/")
    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(errors, url_prefix="/")

    from .models import User, Post
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # return User.query.get(int(user_id))

        return User.query.filter_by(alternative_id=user_id).first()
        # The alternative_id is in User class of models.py

    return app


def create_database(app):
    if path.exists("flaskblog/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!!")

