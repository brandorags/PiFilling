import logging

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# init Flask
app = Flask(__name__)
app.config.from_pyfile('../app_config.py')


# init logging
logging.basicConfig(filename=app.config['LOG_FILE_LOC'], format='[%(levelname)s] %(asctime)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING)


# init SQLAlchemy
db = SQLAlchemy(app)

from api.database import models

db.create_all()


# register blueprints
from api.resources.login_resource import login_resource
from api.resources.admin_resource import admin_resource

app.register_blueprint(login_resource)
app.register_blueprint(admin_resource)


# init Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)


# implement session callback functions
from api.database.models import PiFillingUser


@login_manager.user_loader
def load_user(user_id: int) -> PiFillingUser:
    """
    Callback function that gets the user object whose ID
    is stored in the session. This function gets called
    every time an endpoint is decorated with the
    @login_required decorator function

    :param user_id: the user's ID
    :return: the PiFillingUser object
    """
    return PiFillingUser.query.get(user_id)


@app.before_request
def set_session_details() -> None:
    """
    Callback function that sets the user's session details
    before every request that is made. This function ensures
    that the user's session will expire in the amount of
    time designated by the configuration variable
    SESSION_DURATION, but it also ensures that when the user
    makes a request, their session will continue to stay
    alive and will reset to the amount of time designated by
    the same configuration variable mentioned above.

    :return:
    """
    session.permanent = True
    session.modified = True
    app.permanent_session_lifetime = app.config['SESSION_DURATION']
