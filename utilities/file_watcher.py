import os
import time

try:
    from utilities.filesearchutilities import getFilesFromArguments
except:
    print "Could not import utilities. Have you sourced the environment?"
    exit()


def get_file_time(fpath):
    return os.path.getmtime(fpath)


def run_tests(fname=None):
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.system("reset; python tests/test_pep8_lint_flakes.py")


def main():
    old_files = getFilesFromArguments([], "*.py")

    last_file_change_times = dict((fn, get_file_time(fn)) for fn in old_files)
    run_tests()

    while 1:
        time.sleep(5)
        new_files = getFilesFromArguments([], "*.py")
        if len(new_files) != len(old_files):
            # file deleted - run this on all files
            old_files = new_files
            last_file_change_times = dict((fn, get_file_time(fn)) for fn in old_files)
            run_tests()
            continue

        if sorted(new_files) != sorted(old_files):
            # file renamed (or added and deleted) - run on all files
            old_files = new_files
            last_file_change_times = dict((fn, get_file_time(fn)) for fn in old_files)
            run_tests()
            continue

        old_files = new_files
        new_file_change_times = dict((fn, get_file_time(fn)) for fn in old_files)

        if (max(new_file_change_times.values()) > max(last_file_change_times.values())):
            last_file_change_times = dict((fn, get_file_time(fn)) for fn in old_files)
            run_tests()
            continue

if __name__ == "__main__":
    main()
