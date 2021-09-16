from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from aboveboard.config import Config


mail = Mail()
mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from aboveboard.users.routes import users
    from aboveboard.games.routes import games
    from aboveboard.main.routes import main
    from aboveboard.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(games)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
