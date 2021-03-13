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
import shutil
import os

from app import db
from test.pifilling_test import PiFillingTest
from app.util.file_index_service import FileIndexService
from app.database.entities import Filename, DirectoryPath


class FileIndexServiceTest(PiFillingTest):

    def setUp(self):
        super().setUp()

        base_dir = self.app.config['UPLOADED_FILES_DEST']
        os.mkdir(base_dir)

        temp_dir = base_dir + '/temp_directory'
        os.mkdir(temp_dir)

        with open(temp_dir + '/test.txt', 'w') as file:
            file.write('Test test test')

        temp_dir = base_dir + '/another_temp_directory'
        os.mkdir(temp_dir)

        with open(temp_dir + '/test.txt', 'w') as file:
            file.write('Test test test')

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.app.config['UPLOADED_FILES_DEST'])

    def test_get_file_path_wildcard(self):
        user_id = 1
        file_path_1 = 'temp_directory/test.txt'
        absolute_path_1 = self.app.config['UPLOADED_FILES_DEST'] + '/temp_directory'
        file_path_2 = 'another_temp_directory/test.txt'
        absolute_path_2 = self.app.config['UPLOADED_FILES_DEST'] + '/another_temp_directory'
        FileIndexService.save_file_path(user_id, file_path_1, absolute_path_1)
        FileIndexService.save_file_path(user_id, file_path_2, absolute_path_2)

        results = FileIndexService.get_file_path_wildcard(user_id, 'st.tx')

        self.assertEqual(len(results), 2)

    def test_save_file_path_directory_does_not_exist(self):
        user_id = 1
        file_path = 'temp_directory/test.txt'
        absolute_path = self.app.config['UPLOADED_FILES_DEST'] + '/temp_directory'

        file_metadata = FileIndexService.save_file_path(user_id, file_path, absolute_path)

        self.assertEqual(file_metadata.filename, 'test.txt')
        self.assertEqual(file_metadata.file_type, '.txt')
        self.assertIsNotNone(file_metadata.modified_date)
        self.assertIsNotNone(file_metadata.file_size)
        self.assertFalse(file_metadata.is_directory)

        filename = Filename.query.filter_by(user_id=user_id, directory_id=1, filename='test.txt').first()
        self.assertIsNotNone(filename)

    def test_save_file_path_directory_exists(self):
        user_id = 1
        file_path = 'temp_directory/test.txt'
        absolute_path = self.app.config['UPLOADED_FILES_DEST'] + '/temp_directory'

        directory_path = DirectoryPath(user_id=user_id, absolute_path=absolute_path, directory_name='temp_directory')

        db.session.add(directory_path)
        db.session.commit()

        file_metadata = FileIndexService.save_file_path(user_id, file_path, absolute_path)

        self.assertEqual(file_metadata.filename, 'test.txt')
        self.assertEqual(file_metadata.file_type, '.txt')
        self.assertIsNotNone(file_metadata.modified_date)
        self.assertIsNotNone(file_metadata.file_size)
        self.assertFalse(file_metadata.is_directory)

        filename = Filename.query.filter_by(user_id=user_id, directory_id=1, filename='test.txt').first()

        self.assertIsNotNone(filename)

    def test_get_directory_path(self):
        user_id = 1
        absolute_path = self.app.config['UPLOADED_FILES_DEST'] + '/temp_directory'
        FileIndexService.save_directory_path(user_id, absolute_path)

        directory_path = FileIndexService.get_directory_path(absolute_path)

        self.assertIsNotNone(directory_path)

    def test_get_directory_path_wildcard(self):
        user_id = 1
        absolute_path_1 = self.app.config['UPLOADED_FILES_DEST'] + '/temp_directory'
        absolute_path_2 = self.app.config['UPLOADED_FILES_DEST'] + '/another_temp_directory'
        FileIndexService.save_directory_path(user_id, absolute_path_1)
        FileIndexService.save_directory_path(user_id, absolute_path_2)

        results = FileIndexService.get_directory_path_wildcard(user_id, 'temp')

        self.assertEqual(len(results), 2)

    def test_save_directory_path(self):
        user_id = 1
        absolute_path = self.app.config['UPLOADED_FILES_DEST'] + '/temp_directory'

        directory_path = FileIndexService.save_directory_path(user_id=user_id, absolute_path=absolute_path)

        self.assertIsNotNone(directory_path)


if __name__ == '__main__':
    unittest.main()
