import unittest
import shutil
import io
import subprocess

from werkzeug.security import generate_password_hash
from app import db
from app.database.entities import PiFillingUser
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

        base_dir = self.app.config['UPLOADED_FILES_DEST']
        subprocess.run(['mkdir', base_dir])

        temp_dir = base_dir + '/temp_directory'
        subprocess.run(['mkdir', temp_dir])
        for i in range(0, 5):
            with open(temp_dir + '/temp' + str(i) + '.txt', 'w') as file:
                file.write('Test test test')

    def tearDown(self):
        super().tearDown()

        shutil.rmtree(self.app.config['UPLOADED_FILES_DEST'])

    def test_get_file_metadata_list_for_path_success(self):
        self._log_in_user()

        data = self.client.get('/api/file/file-metadata?path=temp_directory')
        file_metadata_list = data.get_json()
        file_metadata_first_item = file_metadata_list[0]

        self.assertEqual(len(file_metadata_list), 5)
        self.assertTrue({'filename', 'fileSize', 'fileType', 'modifiedDate', 'isDirectory'} ==
                        file_metadata_first_item.keys())

        self.assertEqual(file_metadata_first_item['filename'], 'temp0.txt')
        self.assertEqual(file_metadata_first_item['fileType'], '.txt')
        self.assertIsNotNone(file_metadata_first_item['modifiedDate'])
        self.assertIsNotNone(file_metadata_first_item['fileSize'])
        self.assertFalse(file_metadata_first_item['isDirectory'])

    def test_get_file_metadata_list_for_path_unauthorized(self):
        data = self.client.get('/api/file/file-metadata?path=temp_directory')

        self.assert401(data)

    def test_upload_success(self):
        self._log_in_user()
        file = self._get_test_file()

        data = self.client.post('/api/file/upload', data=file, content_type='multipart/form-data')
        file_metadata_list = data.get_json()
        file_metadata_first_item = file_metadata_list[0]

        self.assertEqual(len(file_metadata_list), 1)
        self.assertTrue({'filename', 'fileSize', 'fileType', 'modifiedDate', 'isDirectory'} ==
                        file_metadata_first_item.keys())

        self.assertEqual(file_metadata_first_item['filename'], 'test.txt')
        self.assertEqual(file_metadata_first_item['fileType'], '.txt')
        self.assertIsNotNone(file_metadata_first_item['modifiedDate'])
        self.assertIsNotNone(file_metadata_first_item['fileSize'])
        self.assertFalse(file_metadata_first_item['isDirectory'])

    def test_upload_success_empty_data(self):
        self._log_in_user()

        data = self.client.post('/api/file/upload', content_type='multipart/form-data')
        file_json = data.get_json()

        self.assertEqual(file_json, [])

    def test_upload_unauthorized(self):
        file = self._get_test_file()

        data = self.client.post('/api/file/upload', data=file, content_type='multipart/form-data')

        self.assert401(data)

    def test_create_new_directory_success(self):
        self._log_in_user()

        data = self.client.post('/api/file/new-directory', json={
            'name': 'test_directory',
            'path': 'test_user/'
        })
        directory_full_name = data.get_json()

        self.assertEqual(directory_full_name, {'name': 'test_directory', 'path': 'test_user/'})

    def test_create_new_directory_unauthorized(self):
        data = self.client.post('/api/file/new-directory', json={
            'name': 'test_directory',
            'path': 'test_user/'
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
