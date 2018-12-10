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


import traceback

from flask import request, Blueprint
from flask_login import login_user
from werkzeug.security import check_password_hash
from app.database.entities import PiFillingUser
from app.util.http_response_wrapper import ok, unauthorized, internal_server_error


login_resource = Blueprint('login_resource', __name__, url_prefix='/api/login')


@login_resource.route('', methods=['POST'])
def login() -> PiFillingUser:
    """
    Logs the user in.

    :return: the logged in user
    """
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = PiFillingUser.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=False)
            return ok(user.to_json())

        return unauthorized()
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)
