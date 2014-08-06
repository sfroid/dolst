"""
Watches a folder for any changes every few seconds (5 by default)
and runs the given command (test_pep8_lint_flakes.py by default)
"""

import os
import sys
import time
import logging
from utilities.log_utils import set_logging_level_to_debug
from subprocess import Popen, PIPE
from settings import settings

try:
    from utilities.filesearchutilities import get_files_from_arguments
except ImportError:
    print "Could not import utilities. Have you sourced the environment?"
    exit()

FULL_TEST_RUN_TIME = 3600
COMMAND = ["python", "tests/test_pep8_lint_flakes.py"]


def get_file_mod_time(fpath):
    """
    Returns the last modification time of the given file
    as a number.
    """
    return os.path.getmtime(fpath)


def run_tests(command, fnames=None):
    """
    Runs the command which runs the tests.
    """
    bad_files = set()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if fnames is None:
        logging.info("Running tests on all files with the command:\n    %s\n", command)
        result = Popen(command, stdout=PIPE).communicate()[0]
    else:
        command = command + [fname for fname in fnames]
        logging.info("Running tests on selected files with the command:\n    %s\n", command)
        result = Popen(command, stdout=PIPE).communicate()[0]

    for line in result.split("\n"):
        if line.startswith("BAD_FILES"):
            bad_files.update(set(line.split("=")[1].split(",")))

    return bad_files, result


def get_added_files(new_files, old_files):
    """
    Return the strings (file names/paths) present in new_files which
    not present in old_files
    """
    new_set = set(new_files)
    old_set = set(old_files)
    return new_set.difference(old_set)


def get_modified_files(new_fch_times, old_fch_times):
    """
    Given dictionaries of name, mod_time pairs of latest and old files,
    return list of filenames that changed
    """
    mod_files = set()
    for fname, mod_time in new_fch_times.items():
        if fname in old_fch_times:
            if mod_time > old_fch_times[fname]:
                mod_files.add(fname)
    return mod_files


def run_tests_on_changes(command, file_data, dirty_files):
    """
    Run the tests only on added files or on
    modified files
    """
    (latest_files, latest_file_change_times,
     old_files, old_file_change_times) = file_data

    added_files = get_added_files(latest_files, old_files)
    dirty_files.difference_update(set(added_files))
    modified_files = get_modified_files(latest_file_change_times, old_file_change_times)
    dirty_files.difference_update(set(modified_files))

    all_to_test = added_files.union(modified_files).union(dirty_files)
    new_and_modified = added_files.union(modified_files)

    if len(new_and_modified) > 0:
        os.system("reset")
        dirty_files, result = run_tests(command, all_to_test)
        print result
    else:
        print "Nothing to test/report. Time = %s" % time.ctime()

    return dirty_files


def main(kwargs):
    """
    Main entry point for the tests.
    """
    command = kwargs.pop('command', COMMAND)
    only_modified = kwargs.pop('only_modified', False)
    args = kwargs.pop('argv', [])
    command = command + args

    dirty_files = set()

    old_files = get_files_from_arguments([], "*.py")
    old_file_change_times = dict((fn, get_file_mod_time(fn)) for fn in old_files)

    # on first run, run tests on all files
    if only_modified is False:
        os.system("reset")
        dirty_files, result = run_tests(command)
        last_full_test_time = time.time()
        print result


    while 1:
        sleep_time = settings.get_setting("TEST_SETTINGS", 'file_check_delay', 5)
        time.sleep(sleep_time)

        # get all files
        latest_files = get_files_from_arguments([], "*.py")
        latest_file_change_times = dict((fn, get_file_mod_time(fn)) for fn in latest_files)

        if only_modified is False:
            if (time.time() - last_full_test_time) > FULL_TEST_RUN_TIME:
                last_full_test_time = time.time()
                dirty_files, result = run_tests(command)
                print result
                continue

        dirty_files = run_tests_on_changes(command,
                                           (latest_files, latest_file_change_times,
                                            old_files, old_file_change_times),
                                           dirty_files)

        old_files = latest_files
        old_file_change_times = latest_file_change_times


def parse_args():
    """
    Parse the arguments and return as a dictionary
    """
    run_on_only_modified = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "only_modified":
            sys.argv = sys.argv[2:]
            logging.info("Only running tests on changes")
            run_on_only_modified = True
        else:
            sys.argv = sys.argv[1:]

    return {"only_modified": run_on_only_modified,
            "argv": sys.argv}



if __name__ == "__main__":
    set_logging_level_to_debug()
    main(parse_args())
