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