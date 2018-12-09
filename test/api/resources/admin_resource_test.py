import unittest

from werkzeug.security import generate_password_hash
from app import db
from app.database import PiFillingUser
from test.pifilling_test import PiFillingTest


class AdminResourceTest(PiFillingTest):

    def setUp(self):
        super().setUp()

        username = 'test_user'
        password = 'password'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:200000', salt_length=32)
        user = PiFillingUser(username=username, password_hash=hashed_password, is_admin=True)

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        super().tearDown()

    def test_create_user_success(self):
        self._log_in_user()

        data = self.client.post('/api/admin/create-user', json={
            'username': 'new_test_user', 'password': 'password'
        })
        new_user_json = data.get_json()

        self.assertEqual(new_user_json, {'username': 'new_test_user', 'isAdmin': False})

    def test_create_user_unauthorized_not_logged_in(self):
        data = self.client.post('/api/admin/create-user', json={
            'username': 'new_test_user', 'password': 'password'
        })

        self.assert401(data)

    def test_create_user_unauthorized_not_admin(self):
        admin_user = PiFillingUser.query.filter_by(username='test_user').first()
        admin_user.is_admin = False
        db.session.commit()

        self._log_in_user()

        data = self.client.post('/api/admin/create-user', json={
            'username': 'new_test_user', 'password': 'password'
        })

        self.assert401(data)

    def test_create_user_error(self):
        self._log_in_user()

        data = self.client.post('/api/admin/create-user', json={
            'wrongKey': 'new_test_user', 'password': 'password'
        })

        self.assert500(data)

    def _log_in_user(self):
        self.client.post('/api/login', json={
            'username': 'test_user', 'password': 'password'
        })


if __name__ == '__main__':
    unittest.main()
