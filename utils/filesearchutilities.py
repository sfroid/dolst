import os
import sys
import fnmatch

def getRootDirPath():
    currdir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(currdir)
    return root

def getFilesRecursively(args, ffilter):
    files = []
    for arg in args:
        if os.path.isfile(arg):
            if fnmatch.filter([arg], ffilter):
                files.append(arg)
        elif os.path.isdir(arg):
            matches = []
            for root, dirnames, filenames in os.walk(arg):
                for filename in fnmatch.filter(filenames, ffilter):
                    matches.append(os.path.join(root, filename))
            files.extend(matches)

    return files

def getFilesFromArguments(args, ffilter="*.*"):
    files = []
    if len(args) == 0:
        # run on all files in the root folder
        dpath = getRootDirPath()
        inputArguments = [dpath]
    else:
        inputArguments = sys.argv[1:]

    return getFilesRecursively(inputArguments, ffilter)


def main():
    from pprint import pprint as pp

    files = getFilesFromArguments(sys.argv[1:], "*.py")
    pp(files)

if __name__ == "__main__":
    main()
