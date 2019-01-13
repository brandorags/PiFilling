# Copyright 2018-2019 Brandon Ragsdale
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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

from app.database.entities import *

db.create_all()


# register blueprints
from app.api import login_resource
from app.api import logout_resource
from app.api import file_resource
from app.api import admin_resource

app.register_blueprint(login_resource)
app.register_blueprint(logout_resource)
app.register_blueprint(file_resource)
app.register_blueprint(admin_resource)


# init Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)


# implement session callback functions
from app.database.entities import PiFillingUser


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
