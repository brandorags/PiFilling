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


class LoginResourceTest(PiFillingTest):

    def setUp(self):
        super().setUp()

        username = 'test_user'
        password = 'password'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:200000', salt_length=32)
        user = PiFillingUser(username=username, password_hash=hashed_password)

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        super().tearDown()

    def test_login_success(self):
        user = PiFillingUser.query.filter_by(username='test_user').first()

        data = self.client.post('/api/login', json={
            'username': 'test_user', 'password': 'password'
        })
        user_json = data.get_json()

        self.assertEqual(user_json, user.to_json())

    def test_login_unauthorized(self):
        data = self.client.post('/api/login', json={
            'username': 'fake_user', 'password': 'password'
        })

        self.assert401(data)

    def test_login_error(self):
        data = self.client.post('/api/login', json={
            'wrongKey': 'fake_user', 'password': 'password'
        })

        self.assert500(data)


if __name__ == '__main__':
    unittest.main()
