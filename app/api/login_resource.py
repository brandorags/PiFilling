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
