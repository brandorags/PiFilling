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

from typing import Dict
from flask import Blueprint
from flask_login import login_required, logout_user
from app.util.http_response_wrapper import ok, internal_server_error


logout_resource = Blueprint('logout_resource', __name__, url_prefix='/api/logout')


@logout_resource.route('', methods=['POST'])
@login_required
def logout() -> Dict:
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
