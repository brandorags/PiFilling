import traceback

from flask import request, Blueprint
from flask_login import login_user
from werkzeug.security import check_password_hash
from api.database.models import PiFillingUser
from api.util.http_response_wrapper import ok, unauthorized, internal_server_error


login_resource = Blueprint('login_resource', __name__)


@login_resource.route('/api/login', methods=['POST'])
def login() -> None:
    """
    Logs the user in.

    :return: a generic success message wrapped in JSON
    """
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = PiFillingUser.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=False)
            return ok({'message': 'User has logged in successfully.'})

        return unauthorized()
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)
