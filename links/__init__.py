from links.config import Config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    bcrypt.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    from links.main.handlers import main
    from links.users.handlers import users
    from links.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app


def init_database(app):
    from links.models import User, Links, Reviews, Roles
    with app.app_context():
        db.create_all()