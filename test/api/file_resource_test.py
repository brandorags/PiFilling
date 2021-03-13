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


import unittest
import shutil
import io
import os

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

        base_dir = self.app.config['UPLOAD_FOLDER']
        os.mkdir(base_dir)

        temp_dir = base_dir + '/temp_directory'
        temp_dir_1 = temp_dir + '/temp_directory1'
        temp_dir_2 = temp_dir_1 + '/temp_directory2'
        os.mkdir(temp_dir)
        os.mkdir(temp_dir_1)
        os.mkdir(temp_dir_2)

        for i in range(0, 5):
            with open(temp_dir + '/temp' + str(i) + '.txt', 'w') as file:
                file.write('Test test test')

        for i in range(0, 3):
            with open(temp_dir_1 + '/tempOne' + str(i) + '.txt', 'w') as file:
                file.write('Test test test')

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.app.config['UPLOAD_FOLDER'])

    def test_get_file_metadata_list_for_path_success(self):
        self._log_in_user()

        data = self.client.get('/api/file/file-metadata?path=temp_directory')
        file_metadata_list = data.get_json()
        file_metadata_first_item = file_metadata_list[0]

        self.assertEqual(len(file_metadata_list), 6)
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

    def test_get_directory_list_for_path_success(self):
        self._log_in_user()

        data = self.client.get('/api/file/directory-list?path=temp_directory')
        directory_list = data.get_json()
        directory_list_first_item = directory_list[0]

        self.assertEqual(len(directory_list), 1)
        self.assertTrue({'name', 'path'} == directory_list_first_item.keys())
        self.assertEqual(directory_list_first_item['name'], 'temp_directory1')
        self.assertEqual(directory_list_first_item['path'], self.app.config['UPLOAD_FOLDER'] + '/' + 'temp_directory')

    def test_get_directory_list_for_path_unauthorized(self):
        data = self.client.get('/api/file/directory-list?path=temp_directory')

        self.assert401(data)

    def test_upload_file_success(self):
        self._log_in_user()
        file = self._get_test_file()
        headers = {'Current-Directory': 'temp_directory'}

        data = self.client.post('/api/file/upload-file', data=file, content_type='multipart/form-data',
                                headers=headers)
        file_metadata = data.get_json()

        self.assertTrue({'filename', 'fileSize', 'fileType', 'modifiedDate', 'isDirectory'} == file_metadata.keys())

        self.assertEqual(file_metadata['filename'], 'test.txt')
        self.assertEqual(file_metadata['fileType'], '.txt')
        self.assertIsNotNone(file_metadata['modifiedDate'])
        self.assertIsNotNone(file_metadata['fileSize'])
        self.assertFalse(file_metadata['isDirectory'])

    def test_upload_file_unauthorized(self):
        file = self._get_test_file()

        data = self.client.post('/api/file/upload-file', data=file, content_type='multipart/form-data')

        self.assert401(data)

    def test_rename_file_success(self):
        self._log_in_user()

        data = self.client.post('/api/file/rename-file', json={
            'oldFilename': 'temp0.txt',
            'newFilename': 'new_filename.txt',
            'path': 'temp_directory'
        })
        new_filename = data.get_json()

        self.assertEqual(new_filename, 'new_filename.txt')

    def test_rename_file_unauthorized(self):
        data = self.client.post('/api/file/rename-file', json={
            'oldFilename': 'temp0.txt',
            'newFilename': 'new_filename.txt',
            'path': 'temp_directory'
        })

        self.assert401(data)

    def test_rename_file_error(self):
        self._log_in_user()

        data = self.client.post('/api/file/rename-file', json={
            'oldFilename': 'this_file_does_not_exist.txt',
            'newFilename': 'new_filename.txt',
            'path': 'temp_directory'
        })

        self.assert500(data)

    def test_move_files_success_files(self):
        self._log_in_user()

        subsubdirectory = self.app.config['UPLOAD_FOLDER'] + '/' + 'temp_directory' + '/' + \
            'subdirectory' + '/' + 'subsubdirectory'
        os.makedirs(subsubdirectory)

        data = self.client.post('/api/file/move-files', json=[
            {
                'sourcePath': 'temp_directory/temp0.txt',
                'destinationPath': 'temp_directory/subdirectory/subsubdirectory'
            },
            {
                'sourcePath': 'temp_directory/temp3.txt',
                'destinationPath': 'temp_directory/subdirectory/subsubdirectory'
            }
        ])

        self.assert200(data)

    def test_move_files_success_directories(self):
        self._log_in_user()

        subsubdirectory = self.app.config['UPLOAD_FOLDER'] + '/' + 'temp_directory' + '/' + \
            'subdirectory' + '/' + 'subsubdirectory'
        os.makedirs(subsubdirectory)

        other_subsubdirectory = self.app.config['UPLOAD_FOLDER'] + '/' + 'temp_directory' + '/' + \
            'subdirectory' + '/' + 'other_subsubdirectory'
        os.makedirs(other_subsubdirectory)

        data = self.client.post('/api/file/move-files', json=[
            {
                'sourcePath': 'temp_directory/subdirectory/subsubdirectory',
                'destinationPath': 'temp_directory'
            },
            {
                'sourcePath': 'temp_directory/subdirectory/other_subsubdirectory',
                'destinationPath': 'temp_directory'
            }
        ])

        self.assert200(data)

    def test_move_files_unauthorized(self):
        data = self.client.post('/api/file/move-files', json=[
            {
                'sourcePath': 'temp_directory/temp0.txt',
                'destinationPath': 'temp_directory/subdirectory/subsubdirectory'
            },
            {
                'sourcePath': 'temp_directory/temp3.txt',
                'destinationPath': 'temp_directory/subdirectory/subsubdirectory'
            }
        ])

        self.assert401(data)

    def test_move_files_error(self):
        self._log_in_user()

        data = self.client.post('/api/file/move-files', json=[
            {
                'sourcePath': 'temp_directory/temp0.txt',
                'destinationPath': 'nonexistent_directory'
            }
        ])

        self.assert500(data)

    def test_download_files_success_single_file(self):
        self._log_in_user()

        data = self.client.post('/api/file/download-files', json={
                'path': 'temp_directory',
                'files': [
                    {'filename': 'temp0.txt', 'isDirectory': False}
                ]
            }
        )

        self.assert200(data)

    def test_download_files_success_single_directory(self):
        self._log_in_user()

        data = self.client.post('/api/file/download-files', json={
                'path': 'temp_directory',
                'files': [
                    {'filename': 'temp_directory1', 'isDirectory': True}
                ]
            }
        )

        self.assert200(data)

    def test_download_files_success_multiple(self):
        self._log_in_user()

        data = self.client.post('/api/file/download-files', json={
                'path': 'temp_directory',
                'files': [
                    {'filename': 'temp0.txt', 'isDirectory': False},
                    {'filename': 'temp1.txt', 'isDirectory': False},
                    {'filename': 'temp2.txt', 'isDirectory': False},
                    {'filename': 'temp_directory1', 'isDirectory': True}
                ]
            }
        )

        self.assert200(data)

    def test_download_files_unauthorized(self):
        data = self.client.post('/api/file/download-files', json={
                'path': 'temp_directory',
                'files': [
                    {'filename': 'temp0.txt', 'isDirectory': False}
                ]
            }
        )

        self.assert401(data)

    def test_download_files_error(self):
        self._log_in_user()

        data = self.client.post('/api/file/download-files', json={
                'path': 'temp_directory',
                'files': [
                    {'filename': 'nonexistent_file.txt', 'isDirectory': False}
                ]
            }
        )

        self.assert500(data)

    def test_delete_files_success_files(self):
        self._log_in_user()

        data = self.client.delete('/api/file/delete-files', json=[
            {
                'filename': 'temp0.txt',
                'path': 'temp_directory',
                'isDirectory': False
            },
            {
                'filename': 'temp1.txt',
                'path': 'temp_directory',
                'isDirectory': False
            }
        ])

        self.assert200(data)

    def test_delete_files_success_directory(self):
        self._log_in_user()

        data = self.client.delete('/api/file/delete-files', json=[
            {
                'filename': 'temp_directory',
                'path': '',
                'isDirectory': True
            }
        ])

        self.assert200(data)

    def test_delete_files_unauthorized(self):
        data = self.client.delete('/api/file/delete-files', json=[
            {
                'filename': 'temp0.txt',
                'path': 'temp_directory',
                'isDirectory': False
            }
        ])

        self.assert401(data)

    def test_delete_files_error(self):
        self._log_in_user()

        data = self.client.delete('/api/file/delete-files', json=[
            {
                'filename': 'this_file_does_not_exist.txt',
                'path': 'temp_directory',
                'isDirectory': False
            }
        ])

        self.assert500(data)

    def test_create_new_directory_success(self):
        self._log_in_user()

        data = self.client.post('/api/file/new-directory', json={
            'name': 'new_directory',
            'path': 'temp_directory'
        })
        directory_full_name = data.get_json()

        self.assertEqual(directory_full_name, {'name': 'new_directory', 'path': 'temp_directory'})

    def test_create_new_directory_unauthorized(self):
        data = self.client.post('/api/file/new-directory', json={
            'name': 'new_directory',
            'path': 'temp_directory'
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
