import unittest

from werkzeug.security import generate_password_hash
from api import db
from api.database.models import PiFillingUser
from test.pifilling_test import PiFillingTest


class LoginResourceTest(PiFillingTest):

    def setUp(self):
        super().setUp()

        username = 'test'
        password = 'password'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:200000', salt_length=32)
        user = PiFillingUser(username=username, password_hash=hashed_password)

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        super().tearDown()

    def test_user_added(self):
        user = PiFillingUser.query.filter_by(username='test').first()
        self.assertEqual(user.username, 'test', 'username should be ' + user.username)

    # def test_login(self):
    #     response = self.client.get('/api/login')
    #     self.assertEqual(response.json, dict(success=True))


if __name__ == '__main__':
    unittest.main()
