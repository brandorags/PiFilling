import os
import logging

from flask_testing import TestCase
from flask_uploads import UploadSet, ALL, configure_uploads, patch_request_class
from app import app, db


class PiFillingTest(TestCase):

    def create_app(self):
        # override default Flask configuration
        app.config['TESTING'] = True
        app.config['BASE_DIR'] = os.path.abspath(os.path.dirname(__file__))
        app.config['UPLOADED_FILES_DEST'] = app.config['BASE_DIR'] + '/files'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

        # override Flask-Uploads configuration
        files_upload_set = UploadSet('files', ALL)
        configure_uploads(app, files_upload_set)
        patch_request_class(app, size=5000000000)

        # disable logging
        logger = logging.getLogger()
        logger.disabled = True

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
