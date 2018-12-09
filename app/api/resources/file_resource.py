import traceback

from typing import List
from subprocess import run, SubprocessError
from flask import request, Blueprint
from flask_login import login_required, current_user
from api import app, files_upload_set
from api.util.http_response_wrapper import ok, internal_server_error
from api.models.file_metadata import FileMetadata
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
        path = current_user.username

        for f in files_to_upload:
            file = files_to_upload[f]
            files_upload_set.save(file, path)

        file_metadata_list = []
        if files_to_upload:
            absolute_path = files_upload_set.config.destination + '/' + path
            file_metadata_list = DirectoryContentParser.parse_directory_content(absolute_path)

        return ok([metadata.to_json() for metadata in file_metadata_list])
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

        absolute_path = files_upload_set.config.destination + '/' + path + directory_name

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
