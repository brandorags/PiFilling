import traceback
import os

from typing import List
from subprocess import run, SubprocessError
from flask import request, Blueprint
from flask_login import login_required, current_user
from api import app, files_upload_set, db
from api.util.http_response_wrapper import ok, internal_server_error
from api.database.db_models import FileMetadata
from api.util.directory_content_parser import DirectoryContentParser


file_resource = Blueprint('file_resource', __name__, url_prefix='/api/file')


@file_resource.route('file-metadata', methods=['GET'])
@login_required
def get_file_metadata_list_for_path() -> List[FileMetadata]:
    try:
        path = request.args.get('path')
        file_metadata_list = DirectoryContentParser.parse_directory_content(path)

        return ok([metadata.to_json() for metadata in file_metadata_list])
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


@file_resource.route('upload', methods=['POST'])
@login_required
def upload() -> List[FileMetadata]:
    try:
        files_to_upload = request.files
        saved_files = []

        user = current_user

        for f in files_to_upload:
            file = files_to_upload[f]
            filename_with_path = files_upload_set.save(file, user.username)

            split_filename_with_path = filename_with_path.rsplit('/', 1)
            relative_file_path = split_filename_with_path[0]
            filename = split_filename_with_path[1]

            absolute_file_path = files_upload_set.path(filename_with_path)
            file_size = os.stat(absolute_file_path).st_size

            saved_file = FileMetadata(user_id=user.id, path=relative_file_path,
                                      filename=filename, file_size=file_size)
            saved_files.append(saved_file)

        if saved_files:
            db.session.bulk_save_objects(saved_files)
            db.session.commit()

        return ok([file.to_json() for file in saved_files])
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


@file_resource.route('new-directory', methods=['POST'])
@login_required
def create_new_directory() -> [str]:
    try:
        data = request.get_json()
        directory_name = data['name']
        path = data['path']
        base_path = app.config['UPLOADED_FILES_DEST']

        create_new_directory_proc = run(['mkdir', base_path + path + directory_name], capture_output=True)
        if create_new_directory_proc.returncode != 0:
            raise SubprocessError(create_new_directory_proc.stderr)

        return ok({
            'name': directory_name,
            'path': path
        })
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)
