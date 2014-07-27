"""
Utility functions for searching and finding files

    { sfroid : 2014 }

"""

import os
import sys
import fnmatch


def get_root_dir_path():
    """
    Get the root directory path of the repo
    assuming that this file is in the utilties folder.
    """
    currdir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(currdir)
    return root


def get_files_recursively(args, ffilter):
    """
    Given a set of files/folders as args, we recursively
    all files that match the given filter ffilter.
    """
    files = []
    for arg in args:
        if os.path.isfile(arg):
            if fnmatch.filter([arg], ffilter):
                files.append(arg)
        elif os.path.isdir(arg):
            matches = []
            for rdftuple in os.walk(arg):
                root, filenames = rdftuple[0], rdftuple[2]
                for filename in fnmatch.filter(filenames, ffilter):
                    matches.append(os.path.join(root, filename))
            files.extend(matches)

    return files


def get_files_from_arguments(args, ffilter="*.*"):
    """
    Given files/folders in args (list), we recursively
    get all files matching the given filter.
    """
    if len(args) == 0:
        # run on all files in the root folder
        dpath = get_root_dir_path()
        input_arguments = [dpath]
    else:
        input_arguments = sys.argv[1:]

    return get_files_recursively(input_arguments, ffilter)


def main():
    """
    Test function
    """
    from pprint import pprint as pp

    files = get_files_from_arguments(sys.argv[1:], "*.py")
    pp(files)


if __name__ == "__main__":
    main()
