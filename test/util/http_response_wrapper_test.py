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


import unittest

from test.pifilling_test import PiFillingTest
from app.util.http_response_wrapper import ok, unauthorized, internal_server_error


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
