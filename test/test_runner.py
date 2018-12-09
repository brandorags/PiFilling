import unittest
import os


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = os.path.abspath(os.path.dirname(__file__))
    test_suite = loader.discover(start_dir=start_dir, pattern='*test.py')

    runner = unittest.TextTestRunner()
    runner.run(test_suite)
