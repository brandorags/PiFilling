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


import traceback

from typing import Dict
from flask import request, Blueprint
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from app.database.entities import PiFillingUser
from app.util.http_response_wrapper import ok, unauthorized, internal_server_error


admin_resource = Blueprint('admin_resource', __name__, url_prefix='/api/admin')


@admin_resource.route('create-user', methods=['POST'])
@login_required
def create_user() -> Dict:
    """
    Creates a new user. The user who accesses this endpoint
    must have admin privileges.

    :return: a generic success message wrapped in JSON
    """
    try:
        logged_in_user = PiFillingUser.query.filter_by(id=current_user.id).first()
        if not logged_in_user or not logged_in_user.is_admin:
            return unauthorized()

        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256:200000', salt_length=32)
        new_user = PiFillingUser(username=data['username'], password_hash=hashed_password, is_admin=False)

        db.session.add(new_user)
        db.session.commit()

        return ok(new_user.to_json())
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)
