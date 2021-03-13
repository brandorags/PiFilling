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
import os
import xmlrunner

from pathlib import Path


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = os.path.abspath(os.path.dirname(__file__))
    test_suite = loader.discover(start_dir=start_dir, pattern='*test.py')

    results_dir = Path(start_dir + '/test-reports/unittest/')
    if not results_dir.is_dir():
        os.makedirs(results_dir.as_posix())

    with open(results_dir.as_posix() + '/results.xml', 'wb') as results_file:
        runner = xmlrunner.XMLTestRunner(output=results_file)
        result = runner.run(test_suite)

    if not result.wasSuccessful():
        exit(1)
