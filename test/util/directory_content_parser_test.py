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

from app.util.directory_content_parser import DirectoryContentParser
from app.models.file_metadata import FileMetadata
from app.models.directory_path import DirectoryPath
from test.pifilling_test import PiFillingTest


class DirectoryContentParserTest(PiFillingTest):

    def setUp(self):
        super().setUp()

        base_dir = self.app.config['UPLOADED_FILES_DEST']
        os.mkdir(base_dir)

        temp_dir = base_dir + '/temp_directory'
        os.mkdir(temp_dir)

        for i in range(0, 5):
            with open(temp_dir + '/temp' + str(i) + '.txt', 'w') as file:
                file.write('Test test test')

        os.mkdir(temp_dir + '/temp_directory1')
        os.mkdir(temp_dir + '/temp_directory2')

    def tearDown(self):
        super().tearDown()

        shutil.rmtree(self.app.config['UPLOADED_FILES_DEST'])

    def test_parse_directory_content(self):
        file_metadata_list = DirectoryContentParser.parse_directory_content('temp_directory')
        file_metadata_first_item = file_metadata_list[0]

        self.assertEqual(len(file_metadata_list), 7)
        self.assertTrue(isinstance(file_metadata_first_item, FileMetadata))
        self.assertEqual(file_metadata_first_item.filename, 'temp0.txt')
        self.assertEqual(file_metadata_first_item.file_type, '.txt')
        self.assertIsNotNone(file_metadata_first_item.modified_date)
        self.assertIsNotNone(file_metadata_first_item.file_size)
        self.assertFalse(file_metadata_first_item.is_directory)

    def test_get_directory_list(self):
        directory_list = DirectoryContentParser.get_directory_list('temp_directory')
        directory_list_first_item = directory_list[0]

        self.assertEqual(len(directory_list), 2)
        self.assertTrue(isinstance(directory_list_first_item, DirectoryPath))
        self.assertEqual(directory_list_first_item.name, 'temp_directory1')
        self.assertEqual(directory_list_first_item.path, 'temp_directory')

    def test_get_file(self):
        file_metadata = DirectoryContentParser.get_file('temp_directory/temp0.txt')

        self.assertTrue(isinstance(file_metadata, FileMetadata))
        self.assertEqual(file_metadata.filename, 'temp0.txt')
        self.assertEqual(file_metadata.file_type, '.txt')
        self.assertIsNotNone(file_metadata.modified_date)
        self.assertIsNotNone(file_metadata.file_size)
        self.assertFalse(file_metadata.is_directory)


if __name__ == '__main__':
    unittest.main()
