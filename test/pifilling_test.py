from flask import Flask
from flask_testing import TestCase
from api import db
from api.resources.login_resource import login_resource
from api.resources.logout_resource import logout_resource
from api.resources.file_resource import file_resource
from api.resources.admin_resource import admin_resource


class PiFillingTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)

        app.register_blueprint(login_resource)
        app.register_blueprint(logout_resource)
        app.register_blueprint(file_resource)
        app.register_blueprint(admin_resource)

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
