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


class FileIndex(object):

    def __init__(self, filename, directory_name, absolute_path, is_directory):
        self.filename = filename
        self.directory_name = directory_name
        self.absolute_path = absolute_path
        self.is_directory = is_directory

    def to_json(self):
        """
        Returns a dictionary with keys in the JSON standard
        camel case format.

        :return: a JSON version of FileIndex
        """
        return {
            'filename': self.filename,
            'directoryName': self.directory_name,
            'absolutePath': self.absolute_path,
            'isDirectory': self.is_directory
        }
