import os
import sys
from utils.filesearchutilities import getFilesFromArguments

all_tests = {
    'pep8': ('pep8', "*.py"),
    'pyflakes': ('pyflakes', "*.py"),
    'pylint': ('pylint', "*.py"),
}

def runTest(command, fpattern):
    from pprint import pprint as pp
    files = getFilesFromArguments(sys.argv[1:], fpattern)

    for fname in files:
        os.system("%s %s"%(command, fname))

def whatTestsToRun(args):
    if len(args) == 1:
        return all_tests.keys()

    tests = []
    while (len(args) >= 2) and (args[1] in all_tests):
        tests.append(args.pop(1))

    if len(tests) > 0:
        return tuple(tests)
    return all_tests.keys()

def main():
    tests = whatTestsToRun(sys.argv)
    for test in tests:
        runTest(*all_tests[test])

if __name__ == "__main__":
    main()