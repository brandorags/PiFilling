import traceback

from flask import request, Blueprint
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from api.util.http_response_wrapper import ok, unauthorized, internal_server_error
from api import db
from api.database.models import PiFillingUser


admin_resource = Blueprint('admin_resource', __name__)


@admin_resource.route('/api/admin', methods=['POST'])
@login_required
def create_user() -> None:
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
