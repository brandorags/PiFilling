import unittest
import shutil
import os
import io

from werkzeug.security import generate_password_hash
from api import db
from api.database.models import PiFillingUser
from test.pifilling_test import PiFillingTest


class FileResourceTest(PiFillingTest):

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

        test_file_upload_folder_path = self.app.config['UPLOADED_FILES_DEST'] + '/test_user'
        path_exists = os.path.exists(test_file_upload_folder_path)
        if path_exists:
            shutil.rmtree(test_file_upload_folder_path)

    def test_upload_file_success(self):
        self._log_in_user()
        file = self._get_test_file()

        data = self.client.post('/api/file/upload', data=file, content_type='multipart/form-data')
        file_json = data.get_json()

        self.assertEqual(file_json, [{'filename': 'test.txt', 'path': 'test_user'}])

    def test_upload_file_success_empty_data(self):
        self._log_in_user()

        data = self.client.post('/api/file/upload', content_type='multipart/form-data')
        file_json = data.get_json()

        self.assertEqual(file_json, [])

    def test_upload_file_unauthorized(self):
        file = self._get_test_file()

        data = self.client.post('/api/file/upload', data=file, content_type='multipart/form-data')

        self.assert401(data)

    def test_create_new_file_success(self):
        self._log_in_user()

        data = self.client.post('/api/file/new-folder', json={
            'name': 'Test Folder'
        })
        new_folder_json = data.get_json()

        self.assertEqual(new_folder_json, {'name': 'Test Folder'})

    def test_create_new_file_unauthorized(self):
        data = self.client.post('/api/file/new-folder', json={
            'name': 'Test Folder'
        })

        self.assert401(data)

    def _get_test_file(self):
        data = {'name': 'test_name', 'test_number': 14}
        data = {key: str(value) for key, value in data.items()}
        data['file'] = (io.BytesIO(b"this is some test data"), 'test.txt')

        return data

    def _log_in_user(self):
        self.client.post('/api/login', json={
            'username': 'test_user', 'password': 'password'
        })


if __name__ == '__main__':
    unittest.main()
