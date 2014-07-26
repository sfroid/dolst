"""
This module can run the PEP8, PyLint and PyFlakes
tests on source files.

Usage: python test_pep8_lint_flakes.py \
            [pep8] [pylint] [pyflakes] <files or folders or nothing>

Optionally, the user can specify one or more of the pep8, pylint
or pyflakes tests. If none are specified, all tests are executed.

Also, the user can optionally specify files / folders to run the
test on. If a folder is specified, the tests are executed on all
python files in that folder (folders are searched recursively).
"""


import os
import sys
from utilities.filesearchutilities import getFilesFromArguments
from collections import OrderedDict

ALL_TESTS = {
    'pep8': ('pep8 --max-line-length=120 --ignore=E3 --format=pylint', "*.py"),
    'pyflakes': ('pyflakes', "*.py"),
    'pylint': ('pylint --output-format=colorized --reports=n --max-line-length=120', "*.py"),
}

# converting it to a ordered dict, so tests are run in
# predictable order.
ALL_TESTS = OrderedDict(ALL_TESTS)


def run_test(command, fpattern):
    """
    This method takes a command and a pattern to match files.
    Then, it runs the command on each file that matches the pattern.
    """
    files = getFilesFromArguments(sys.argv[1:], fpattern)  # how oasdflskdjf laksjfdl jskfldfjalskfjd
    print "\nRunning test : %s\n" % command

    for fname in files:
        os.system("%s %s" % (command, fname))


def what_tests_to_run(args):
    """
    Parse the arguments and return the tests to run.
    If no arguments are given, return ALL_TESTS.
    """
    if len(args) == 1:
        return ALL_TESTS.keys()

    tests = []
    while (len(args) >= 2) and (args[1] in ALL_TESTS):
        tests.append(args.pop(1))

    if len(tests) > 0:
        return tuple(tests)
    return ALL_TESTS.keys()


def main():
    """
    Main entry point to the test file.
    Runs the tests and ends.
    """
    tests = what_tests_to_run(sys.argv)
    for test in tests:
        run_test(*ALL_TESTS[test])


if __name__ == "__main__":
    main()
