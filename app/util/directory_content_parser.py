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


import os
import pathlib

from datetime import datetime
from app.models.file_metadata import FileMetadata


class DirectoryContentParser(object):

    @staticmethod
    def parse_directory_content(path):
        file_metadata_list = []

        with os.scandir(path) as dir_content:
            for file in dir_content:
                file_stat = file.stat()

                filename = file.name
                file_size = file_stat.st_size
                file_type = pathlib.Path(filename).suffix
                modified_date = datetime.fromtimestamp(file_stat.st_mtime).strftime('%d/%m/%Y %H:%M:%S')
                is_dir = file.is_dir()

                file_metadata = FileMetadata(filename=filename, file_size=file_size, file_type=file_type,
                                             modified_date=modified_date, is_directory=is_dir)
                file_metadata_list.append(file_metadata)

        return sorted(file_metadata_list, key=lambda fm: fm.filename)

    @staticmethod
    def get_file(filename_with_path):
        file = pathlib.Path(filename_with_path)
        file_stat = file.stat()

        filename = file.name
        file_size = file_stat.st_size
        file_type = file.suffix
        modified_date = datetime.fromtimestamp(file_stat.st_mtime).strftime('%d/%m/%Y %H:%M:%S')
        is_dir = file.is_dir()

        file_metadata = FileMetadata(filename=filename, file_size=file_size, file_type=file_type,
                                     modified_date=modified_date, is_directory=is_dir)

        return file_metadata
