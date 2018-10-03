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

from typing import Dict
from flask import request, Blueprint
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from api.util.http_response_wrapper import ok, unauthorized, internal_server_error
from api import db
from api.database.models import PiFillingUser


admin_resource = Blueprint('admin_resource', __name__)


@admin_resource.route('/api/admin/create-user', methods=['POST'])
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

        return ok({'message': 'New user has been created.'})
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)
