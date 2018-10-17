import unittest

from test.pifilling_test import PiFillingTest
from api.util.http_response_wrapper import ok, unauthorized, internal_server_error


class HttpResponseWrapperTest(PiFillingTest):

    def test_ok(self):
        test_json = {
            'username': 'test_user',
            'password': 'password'
        }

        response = ok(test_json)

        self.assertEqual(response[0].json, test_json)
        self.assertEqual(response[1], 200)

    def test_unauthorized(self):
        response = unauthorized()

        self.assertEqual(response[1], 401)

    def test_internal_server_error(self):
        exception = 'this is the exception'
        stack_trace = 'this is the stack trace'

        response = internal_server_error(exception, stack_trace)

        self.assertEqual(response[1], 500)


if __name__ == '__main__':
    unittest.main()
