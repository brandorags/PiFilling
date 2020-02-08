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


import shutil
import os

from zipfile import ZipFile
from flask import send_file, send_from_directory


class DownloadHelper(object):

    @staticmethod
    def download_file(file, download_path, base_upload_dir_path):
        os.chdir(base_upload_dir_path)

        current_dir_path = base_upload_dir_path + '/' + download_path
        filename = file['filename']
        filename_no_spaces = '_'.join(filename.split())
        is_zip_file = False

        if file['isDirectory']:
            shutil.make_archive(filename_no_spaces, 'zip', current_dir_path + '/' + filename)
            filename_no_spaces += '.zip'
            is_zip_file = True

        # the zip file path will always be at the base upload directory location
        dir_to_send_from = base_upload_dir_path if is_zip_file else current_dir_path
        filename = filename_no_spaces if is_zip_file else filename

        return send_from_directory(dir_to_send_from, filename, as_attachment=True)

    @staticmethod
    def download_multiple_files(files_to_download, download_path, base_upload_dir_path):
        os.chdir(base_upload_dir_path)

        current_dir = base_upload_dir_path + '/' + download_path
        parent_dir = os.path.dirname(current_dir)

        filenames_to_download = [f['filename'] for f in files_to_download]
        dir_paths_to_download = [current_dir + '/' + f['filename'] for f in files_to_download if f['isDirectory']]

        zip_file_name = current_dir.split('/')[-1]
        zip_file_name = zip_file_name.replace(' ', '_') + '.zip'
        zip_file_path = base_upload_dir_path + '/' + zip_file_name

        with ZipFile(zip_file_path, 'w') as zf:
            for root, subdirs, files in os.walk(current_dir):
                for subdir in subdirs:
                    subdir_abs_path = os.path.join(root, subdir)
                    if len([dir_path for dir_path in dir_paths_to_download if dir_path in subdir_abs_path]) == 0:
                        continue

                    subdir_rel_path = subdir_abs_path.replace(parent_dir + '/', '')
                    zf.write(subdir_abs_path, subdir_rel_path)
                for filename in files:
                    file_abs_path = os.path.join(root, filename)
                    if filename not in filenames_to_download and \
                            len([dir_path for dir_path in dir_paths_to_download if dir_path in file_abs_path]) == 0:
                        continue

                    file_rel_path = file_abs_path.replace(parent_dir + '/', '')
                    zf.write(file_abs_path, file_rel_path)

        return send_file(zip_file_path, mimetype='zip', attachment_filename=zip_file_name, as_attachment=True)
