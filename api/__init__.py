# Copyright 2018 Brandon Ragsdale
#
# This file is part of PiFilling.
#
# PiFilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PiFilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PiFilling.  If not, see <https://www.gnu.org/licenses/>.


import logging

from flask import Flask, session
from flask_uploads import UploadSet, ALL, configure_uploads, patch_request_class
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# init Flask
app = Flask(__name__)
app.config.from_pyfile('../app_config.py')


# init Flask-Uploads
files_upload_set = UploadSet('files', ALL)
configure_uploads(app, files_upload_set)
patch_request_class(app, size=5000000000)

# init logging
logging.basicConfig(filename=app.config['LOG_FILE_LOC'], format='[%(levelname)s] %(asctime)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING)


# allow CORS
cors = CORS(app, supports_credentials=True, regex={r'/api/*': {'origins': '*'}})


# init SQLAlchemy
db = SQLAlchemy(app)

from api.database import db_models

db.create_all()


# register blueprints
from api.resources.login_resource import login_resource
from api.resources.logout_resource import logout_resource
from api.resources.file_resource import file_resource
from api.resources.admin_resource import admin_resource

app.register_blueprint(login_resource)
app.register_blueprint(logout_resource)
app.register_blueprint(file_resource)
app.register_blueprint(admin_resource)


# init Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)


# implement session callback functions
from api.database.db_models import PiFillingUser


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
