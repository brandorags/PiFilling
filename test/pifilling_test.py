# Copyright Brandon Ragsdale
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


import os
import logging

from flask_testing import TestCase
from app import app, db


class PiFillingTest(TestCase):

    def create_app(self):
        # override default Flask configuration
        app.config['TESTING'] = True
        app.config['BASE_DIR'] = os.path.abspath(os.path.dirname(__file__))
        app.config['UPLOAD_FOLDER'] = app.config['BASE_DIR'] + '/files'
        app.config['LOG_FILE_LOC'] = os.path.join(app.config['BASE_DIR'], 'info.log')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

        # disable logging
        logger = logging.getLogger()
        logger.disabled = True

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
