"""
NOTE: This file is strictly an internal utility whose purpose is to add admin users to the database.
It is not to be used with the web application whatsoever.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from getpass import getpass


app = Flask(__name__)
app.config.from_pyfile('app_config.py')

db = SQLAlchemy(app)

from app.database.entities import *

db.create_all()


def create_user():
    username = input('Enter the username of the new user: ')
    password = getpass('Enter the password of the new user: ')

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256:200000', salt_length=32)
    new_user = PiFillingUser(username=username, password_hash=hashed_password, is_admin=True)

    db.session.add(new_user)
    db.session.commit()

    # TODO: create a new directory for the user here

    add_another_user_prompt = input('\nThe new user has been inserted into the database. '
                                    'Would you like to add another user? (y|n) ')

    if add_another_user_prompt.lower() == 'y':
        create_user()


def main():
    print('---- PiFilling User Creator ----\n')

    create_user()

    print('\nBye!')


if __name__ == '__main__':
    main()
