import unittest
import os
import xmlrunner


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = os.path.abspath(os.path.dirname(__file__))
    test_suite = loader.discover(start_dir=start_dir, pattern='*test.py')

    output_dir = './test-reports/unittest'
    runner = xmlrunner.XMLTestRunner(output=output_dir)
    runner.run(test_suite)
