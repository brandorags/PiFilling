import traceback

from typing import List
from subprocess import run, SubprocessError
from flask import request, Blueprint
from flask_login import login_required
from app import files_upload_set
from app.models.file_metadata import FileMetadata
from app.util.directory_content_parser import DirectoryContentParser
from app.util.http_response_wrapper import ok, internal_server_error


file_resource = Blueprint('file_resource', __name__, url_prefix='/api/file')


@file_resource.route('file-metadata', methods=['GET'])
@login_required
def get_file_metadata_list_for_path() -> List[FileMetadata]:
    try:
        path = files_upload_set.config.destination + '/' + request.args.get('path')
        file_metadata_list = DirectoryContentParser.parse_directory_content(path)

        return ok([metadata.to_json() for metadata in file_metadata_list])
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


@file_resource.route('upload-file', methods=['POST'])
@login_required
def upload_file():
    try:
        file_to_upload = next(iter(request.files.values()))
        current_directory = request.headers.get('Current-Directory')

        file_path = files_upload_set.save(file_to_upload, current_directory)

        absolute_path = files_upload_set.config.destination + '/' + file_path
        file_metadata = DirectoryContentParser.get_file(absolute_path)

        return ok(file_metadata.to_json())
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

        absolute_path = files_upload_set.config.destination + '/' + path + '/' + directory_name

        create_new_directory_proc = run(['mkdir', '-p', absolute_path], capture_output=True)
        if create_new_directory_proc.returncode != 0:
            raise SubprocessError(create_new_directory_proc.stderr)

        return ok({
            'name': directory_name,
            'path': path
        })
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)
