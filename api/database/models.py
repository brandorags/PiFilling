# Copyright 2018 Brandon Ragsdale
#
# This file is part of PiFilling.
#
# PiFilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PiFilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PiFilling.  If not, see <https://www.gnu.org/licenses/>.


from api import db

from typing import Dict
from flask_login import UserMixin


class PiFillingUser(UserMixin, db.Model):
    __tablename__ = 'pifilling_user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean())

    def to_json(self) -> Dict:
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
