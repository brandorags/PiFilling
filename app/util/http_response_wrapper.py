# Copyright 2018-2019 Brandon Ragsdale
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
import logging

from flask import jsonify


def ok(obj=None):
    """
    Helper function that returns a specified object
    and a Success status code (200). The specified
    object will be converted to JSON before it is
    returned.

    :param obj: any object that can be converted to JSON
    :return: a JSON object and a 200 status code
    """
    try:
        return jsonify(obj), 200
    except Exception as e:
        trace = traceback.format_exc()
        return internal_server_error(e, trace)


def unauthorized():
    """
    Helper function that returns an Unauthorized status
    code (401) with a generic error message wrapped in JSON.

    :return: a 401 status code and a generic error message
    """
    return jsonify({'message': 'You are not allowed to access this endpoint.'}), 401


def internal_server_error(exception, stack_trace):
    """
    Helper function that returns an Internal Server Error
    status code (500) with a generic error message
    wrapped in JSON.

    :param exception: the exception
    :param stack_trace: the stacktrace
    :return: a 500 status code and a generic error message
    """
    formatted_exception = str(exception) + '\n' + stack_trace
    logging.error(formatted_exception)

    return jsonify({'message': 'An error occurred on the server.'}), 500
