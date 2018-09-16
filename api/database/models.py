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
