import traceback

from flask import request, Blueprint
from flask_login import login_required
from api import files_upload_set
from api.util.http_response_wrapper import ok, internal_server_error


file_resource = Blueprint('file_resource', __name__)


@file_resource.route('/api/file/upload', methods=['POST'])
@login_required
def upload_file() -> None:
    try:
        files = request.files
        for filename in files:
            file = files[filename]
            file_path = files_upload_set.save(file)
            print(file_path)

        return ok({'message': 'File(s) was uploaded!'})
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)
