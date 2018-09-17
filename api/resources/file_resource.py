import traceback

from flask import request, Blueprint
from flask_login import login_required, current_user
from api.util.http_response_wrapper import ok, internal_server_error


file_resource = Blueprint('file_resource', __name__)


@file_resource.route('/api/file', methods=['POST'])
@login_required
def upload_file() -> None:
    try:
        files = request.files
        for file in files:
            print(file)

        return ok({'message': 'File was uploaded!'})
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)