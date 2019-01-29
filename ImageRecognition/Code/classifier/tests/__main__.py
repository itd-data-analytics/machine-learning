"""Makes the \'tests\' folder run all of the containing tests."""

__date__ = '09/20/2018'
__authors__ = [
    'Hayden Phothong, Research Analyst Intern @ ITD'
]

import os
import sys
import unittest

if __name__ == '__main__':
    # Create the test suite
    suite = unittest.TestSuite()

    # Get all of the tests
    path = os.path.dirname(os.path.abspath(__file__))
    if not path.endswith('\\tests'):
        path += '\\tests'
    current_directory = os.getcwd()
    os.chdir(path)
    tests = os.listdir('.')
    for test in tests:
        if test.startswith('test_') and test.endswith('.py'):
            test_loader = unittest.TestLoader()
            suite.addTests(test_loader.discover(
                start_dir='.',
                pattern='test_*.py'
            )
            )

    # Run the tests that were found
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    # Reset current working directory
    os.chdir(current_directory)

    # If there was a failure
    if not result.wasSuccessful():
        raise RuntimeError('Unit tests failed')
