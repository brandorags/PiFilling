# Copyright Brandon Ragsdale
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
import shutil
import os

from flask import request, Blueprint
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import app
from app.util.download_helper import DownloadHelper
from app.util.directory_content_parser import DirectoryContentParser
from app.util.http_response_wrapper import ok, internal_server_error


file_resource = Blueprint('file_resource', __name__, url_prefix='/api/file')


@file_resource.route('file-metadata', methods=['GET'])
@login_required
def get_file_metadata_list_for_path():
    try:
        path = _get_base_directory() + '/' + request.args.get('path')
        file_metadata_list = DirectoryContentParser.parse_directory_content(path)

        return ok([metadata.to_json() for metadata in file_metadata_list])
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)
    
    
@file_resource.route('directory-list', methods=['GET'])
@login_required
def get_directory_list_for_path():
    try:
        path = _get_base_directory() + '/' + request.args.get('path')
        directory_list = DirectoryContentParser.get_directory_list(path)

        return ok([directory.to_json() for directory in directory_list])
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


@file_resource.route('upload-file', methods=['POST'])
@login_required
def upload_file():
    try:
        file_to_upload = next(iter(request.files.values()))
        current_directory = request.headers.get('Current-Directory')
        filename = secure_filename(file_to_upload.filename)
        directory_path = _get_base_directory() + '/' + current_directory
        file_path = os.path.join(directory_path, filename)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        file_to_upload.save(file_path)
        file_to_upload.close()

        file_metadata = DirectoryContentParser.get_file(file_path)

        return ok(file_metadata.to_json())
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


@file_resource.route('rename-file', methods=['POST'])
@login_required
def rename_file():
    try:
        data = request.get_json()
        old_filename = data['oldFilename']
        new_filename = data['newFilename']
        path = data['path']

        absolute_path_old_filename = _get_base_directory() + '/' + path + '/' + old_filename
        absolute_path_new_filename = _get_base_directory() + '/' + path + '/' + new_filename

        os.rename(absolute_path_old_filename, absolute_path_new_filename)

        return ok(new_filename)
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


@file_resource.route('move-files', methods=['POST'])
@login_required
def move_files():
    try:
        data = request.get_json()
        for d in data:
            source_path = _get_base_directory() + '/' + d['sourcePath']
            destination_path = _get_base_directory() + '/' + d['destinationPath']

            if os.path.exists(destination_path) and os.path.isdir(destination_path):
                shutil.move(source_path, destination_path)
            else:
                raise Exception('The destination path ' + destination_path + ' does not exist.')

        return ok()
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


@file_resource.route('download-files', methods=['POST'])
@login_required
def download_files():
    try:
        data = request.get_json()
        download_path = data['path']
        files_to_download = data['files']

        if len(files_to_download) == 1:
            file = files_to_download[0]
            return DownloadHelper.download_file(file, download_path, _get_base_directory())
        else:
            return DownloadHelper.download_multiple_files(files_to_download, download_path, _get_base_directory())
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


@file_resource.route('delete-files', methods=['DELETE'])
@login_required
def delete_files():
    try:
        data = request.get_json()
        for d in data:
            filename = d['filename']
            path = d['path']
            is_directory = d['isDirectory']

            absolute_path_file_to_delete = _get_base_directory() + '/' + path + '/' + filename

            if is_directory:
                shutil.rmtree(absolute_path_file_to_delete)
            else:
                os.remove(absolute_path_file_to_delete)

        return ok()
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


@file_resource.route('new-directory', methods=['POST'])
@login_required
def create_new_directory():
    try:
        data = request.get_json()
        directory_name = data['name']
        path = data['path']
        directory_path = path + '/' + directory_name

        absolute_path = _get_base_directory() + '/' + directory_path
        if not os.path.exists(absolute_path):
            os.mkdir(absolute_path)

        return ok({
            'name': directory_name,
            'path': path
        })
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


def _get_base_directory():
    return app.config['UPLOAD_FOLDER']
