from api import db

from flask_login import UserMixin


class PiFillingUser(UserMixin, db.Model):
    __tablename__ = 'pifilling_user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean())
