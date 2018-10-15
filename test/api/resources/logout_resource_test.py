import unittest

from werkzeug.security import generate_password_hash
from api import db
from api.database.models import PiFillingUser
from test.pifilling_test import PiFillingTest


class LogoutResourceTest(PiFillingTest):

    def setUp(self):
        super().setUp()

        username = 'test_user'
        password = 'password'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:200000', salt_length=32)
        user = PiFillingUser(username=username, password_hash=hashed_password)

        db.session.add(user)
        db.session.commit()

        self._log_in_user()

    def tearDown(self):
        super().tearDown()

    def test_logout_success(self):
        data = self.client.post('/api/logout')

        self.assert200(data)

    def _log_in_user(self):
        self.client.post('/api/login', json={
            'username': 'test_user', 'password': 'password'
        })


if __name__ == '__main__':
    unittest.main()