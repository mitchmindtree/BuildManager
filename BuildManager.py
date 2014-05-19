#!usr/bin/env python


'''

BuildManager.py

by Mitchell Nordine

A script used for managing the process of compiling and running
C++ programs.

So far it...
- Checks for headers and rebuilds clang_complete commands if required.

Usage:
    BuildManager.py [-h | --help] [-v | --version]
    BuildManager.py [-r | --run] <makePath>

Options:
    -h --help           Show this screen.
    -v --version        Show version.
    -r --run            Run the program following building.

'''


import os
from docopt import docopt
from HeaderChecker import updateHeaders


def genMakeString(headerDiff):
    '''Function that generates the make command string.'''
    if headerDiff:
        print("Sit Back, time to build cc_args along with project...")
        s = "make PROJECT_CC='~/.vim/bin/cc_args.py clang' PROJECT_CXX='~/.vim/bin/cc_args.py clang++ -std=c++11 -stdlib=libc++' -B"
    else:
        s = "make"
    return s


def cleanPath(path):
    while path[-1] is " " or path[-1] is "/":
        path = path[:-1]
    path = os.path.expanduser(path)
    path = os.path.normpath(path)
    if os.path.exists(path):
        return path
    else:
        raise Exception("I can't find the given path! You're not leading me astray... are you?")


def main():
    args = docopt(__doc__, version='Header Checker -- SUPER RADICAL EDITION')
    path = cleanPath(args['<path>'])
    headerDiff = updateHeaders(path)
    s = genMakeString(headerDiff)
    os.system(s)
    if (args['--run']):
        os.system("make run")


if __name__ == "__main__":
    main() 

