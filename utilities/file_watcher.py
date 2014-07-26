import os
import time

try:
    from utilities.filesearchutilities import getFilesFromArguments
except:
    print "Could not import utilities. Have you sourced the environment?"
    exit()

def getFileTime(fpath):
    return os.path.getmtime(fpath)

def runTests():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.system("reset; pwd; python tests/test_pep8_lint_flakes.py")

def main():
    old_files = getFilesFromArguments([], "*.py")

    last_file_change_time = dict((fn, getFileTime(fn)) for fn in old_files)

    while 1:
        time.sleep(5)
        new_files = getFilesFromArguments([], "*.py")
        if len(new_files) != len(old_files):
            old_files = new_files
            last_file_change_time = dict((fn, getFileTime(fn)) for fn in old_files)
            runTests()
            continue

        if sorted(new_files) != sorted(old_files):
            old_files = new_files
            last_file_change_time = dict((fn, getFileTime(fn)) for fn in old_files)
            runTests()
            continue

        old_files = new_files
        new_file_change_time = dict((fn, getFileTime(fn)) for fn in old_files)

        if max(new_file_change_time.values()) > max(last_file_change_time.values()):
            last_file_change_time = dict((fn, getFileTime(fn)) for fn in old_files)
            runTests()
            continue

if __name__ == "__main__":
    main()

