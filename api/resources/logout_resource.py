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

from flask import Blueprint
from flask_login import login_required, logout_user
from api.util.http_response_wrapper import ok, internal_server_error


logout_resource = Blueprint('logout_resource', __name__)


@logout_resource.route('/api/logout', methods=['POST'])
@login_required
def logout() -> None:
    """
    Logs the user out.

    :return: a generic success message wrapped in JSON
    """
    try:
        logout_user()
        return ok({'message': 'You have been logged out.'})
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)