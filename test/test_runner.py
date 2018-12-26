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

    with open(results_dir.as_posix() + 'results.xml', 'wb') as results_file:
        runner = xmlrunner.XMLTestRunner(output=results_file)
        runner.run(test_suite)
