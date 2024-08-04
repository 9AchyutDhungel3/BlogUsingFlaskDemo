from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blog.config import Config

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

bcrypt = Bcrypt()

# Mail configuration setup
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    # The app.config dictioanr is a general purpose place to store configuration variables used by Flask
    # flask_wtf expects our application to have a secret key configured
    # this key is part of the mechanism the extension uses to protect from CSRF attacks.
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Our routes use our uses the Flask instace 'app'
    # So to prevent circular import , we first configure the app and then
    # only we import the routes

    # Now we import all the blueprints and register them into our app
    from blog.users.routes import users
    from blog.posts.routes import posts
    from blog.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
