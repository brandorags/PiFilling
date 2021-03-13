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


class FileMetadata(object):

    def __init__(self, filename, file_size, file_type, modified_date, is_directory):
        self.filename = filename
        self.file_size = file_size
        self.file_type = file_type
        self.modified_date = modified_date
        self.is_directory = is_directory

    def to_json(self):
        """
        Returns a dictionary with keys in the JSON standard
        camel case format.

        :return: a JSON version of FileMetadata
        """
        return {
            'filename': self.filename,
            'fileSize': self.file_size,
            'fileType': self.file_type,
            'modifiedDate': self.modified_date,
            'isDirectory': self.is_directory
        }
