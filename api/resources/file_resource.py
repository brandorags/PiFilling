import traceback

from typing import List
from flask import request, Blueprint
from flask_login import login_required, current_user
from api import files_upload_set, db
from api.util.http_response_wrapper import ok, internal_server_error
from api.database.models import FileMetadata


file_resource = Blueprint('file_resource', __name__)


@file_resource.route('/api/file/upload', methods=['POST'])
@login_required
def upload_file() -> List[FileMetadata]:
    try:
        files_to_upload = request.files
        saved_files = []

        user = current_user

        for f in files_to_upload:
            file = files_to_upload[f]
            result = files_upload_set.save(file, user.username)

            split_result = result.rsplit('/', 1)
            path = split_result[0]
            filename = split_result[1]

            saved_file = FileMetadata(user_id=user.id, path=path, filename=filename)
            saved_files.append(saved_file)

        if saved_files:
            db.session.bulk_save_objects(saved_files)
            db.session.commit()

        return ok([file.to_json() for file in saved_files])
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)
