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
import os

from zipfile import ZipFile
from test.pifilling_test import PiFillingTest
from app.util.download_helper import DownloadHelper


class DownloadHelperTest(PiFillingTest):

    def setUp(self):
        super().setUp()

        base_dir = self.app.config['UPLOAD_FOLDER']
        os.mkdir(base_dir)

        temp_dir = base_dir + '/temp_directory'
        temp_dir_1 = temp_dir + '/temp_directory1'
        temp_dir_2 = temp_dir + '/temp_directory2'
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

    def test_download_file_file(self):
        file = {'filename': 'temp0.txt', 'isDirectory': False}
        download_path = 'temp_directory'
        base_upload_dir_path = self.app.config['UPLOAD_FOLDER']
        file_response = DownloadHelper.download_file(file, download_path, base_upload_dir_path)

        self.assertIn('temp0.txt', file_response.response.file.name)

    def test_download_file_directory(self):
        file = {'filename': 'temp_directory', 'isDirectory': True}
        download_path = ''
        base_upload_dir_path = self.app.config['UPLOAD_FOLDER']
        file_response = DownloadHelper.download_file(file, download_path, base_upload_dir_path)

        self.assertIn('temp_directory.zip', file_response.response.file.name)

    def test_download_multiple_files(self):
        files = [
            {'filename': 'temp0.txt', 'isDirectory': False},
            {'filename': 'temp2.txt', 'isDirectory': False},
            {'filename': 'temp3.txt', 'isDirectory': False},
            {'filename': 'temp_directory1', 'isDirectory': True}
        ]
        download_path = 'temp_directory'
        base_upload_dir_path = self.app.config['UPLOAD_FOLDER']
        file_response = DownloadHelper.download_multiple_files(files, download_path, base_upload_dir_path)

        self.assertIn('temp_directory.zip', file_response.response.file.name)

        os.chdir(base_upload_dir_path)

        zip_file_output_dir = 'zip_file_output'
        os.mkdir(zip_file_output_dir)
        os.chdir(zip_file_output_dir)

        with ZipFile('../temp_directory.zip', 'r') as zf:
            zf.extractall()

        zip_file_list = []
        for root, subdirs, files in os.walk('temp_directory'):
            for filename in files:
                file_path = os.path.join(root, filename)
                zip_file_list.append(file_path)

        self.assertIn('temp_directory/temp0.txt', zip_file_list)
        self.assertIn('temp_directory/temp2.txt', zip_file_list)
        self.assertIn('temp_directory/temp3.txt', zip_file_list)
        self.assertIn('temp_directory/temp_directory1/tempOne0.txt', zip_file_list)
        self.assertIn('temp_directory/temp_directory1/tempOne1.txt', zip_file_list)
        self.assertIn('temp_directory/temp_directory1/tempOne2.txt', zip_file_list)


if __name__ == '__main__':
    unittest.main()
