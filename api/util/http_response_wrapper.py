import traceback
import logging

from flask import jsonify


def ok(obj):
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
