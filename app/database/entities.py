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


from app import db

from flask_login import UserMixin


class PiFillingUser(UserMixin, db.Model):
    __tablename__ = 'pifilling_user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean)

    def to_json(self):
        """
        Returns a dictionary with keys in the JSON standard
        camel case format.

        :return: a JSON safe version of PiFillingUser that
        doesn't contain the user's ID or password hash
        """
        return {
            'username': self.username,
            'isAdmin': self.is_admin
        }


class DirectoryPath(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('pifilling_user.id'), nullable=False)
    absolute_path = db.Column(db.String, unique=True, nullable=False)
    directory_name = db.Column(db.String, index=True, nullable=False)

    def to_json(self):
        """
        Returns a dictionary with keys in the JSON standard
        camel case format.

        :return: a JSON safe version of DirectoryPath that
        doesn't contain the user's ID or password hash
        """
        return {
            'absolutePath': self.absolute_path,
            'directoryName': self.directory_name
        }


class Filename(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('pifilling_user.id'), nullable=False)
    directory_id = db.Column(db.Integer, db.ForeignKey('directory_path.id'), nullable=False)
    filename = db.Column(db.String, index=True, nullable=False)

    __table_args__ = (db.UniqueConstraint('directory_id', 'filename', name='uc_directory_id_filename'),)

    def to_json(self):
        """
        Returns a dictionary with keys in the JSON standard
        camel case format.

        :return: a JSON safe version of Filename that
        doesn't contain the user's ID or password hash
        """
        return {
            'directoryId': self.directory_id,
            'filename': self.filename
        }
