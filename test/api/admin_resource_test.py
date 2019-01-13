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


import unittest

from werkzeug.security import generate_password_hash
from app import db
from app.database.entities import PiFillingUser
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
