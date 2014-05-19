#!usr/bin/env python


'''

HeaderChecker.py

by Mitchell Nordine

A small python script to check whether any new header files have been added
to a C++ src directory. If they have, it will update the checkedHeaders.json
accordingly.

    - Checks for the path and prepares it for use.

Usage:
    HeaderChecker.py [-h | --help] [-v | --version]
    HeaderChecker.py [-b | --build] <path>

Options:
    -h --help           Show this screen.
    -v --version        Show version.
    -b --build          Build make.

'''


import os, json
from docopt import docopt


def getJsonFP(path):
    '''Returns the path of the JSON file containing previously checked headers.'''
    return path + "/.checkedHeaders.json"


def isDifferent(new, checked):
    '''Check for difference between header list and previously checked.'''
    return True if new != checked else False


def getCheckedHeaders(path):
    '''Retrieve the previously checked headers from JSON.'''
    f = open(getJsonFP(path), 'r')
    checked = json.load(f)
    f.close()
    return checked


def findHeaders(path):
    '''Search directory recursively and find all headers.'''
    headerList = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if os.path.splitext(f)[1] == '.h']
    print 'Number of wavs found in', directory, '=', len(headerList)
    return headerList


def writeNewChecked(headers):
    '''Write the refreshed list of headers to the json file.'''
    f = open(getJsonFP(path), 'w')
    json.dump(headers, f)
    f.close()


def updateHeaders(path, build=False):
    '''
    - Finds all headers in that path.
    - Retrieves the previously checked headers from .json file.
    - Compares lists.
    - If different, writes the new list to the .json and builds with cc_args.
    - Else if same, does a regular build.
    - Runs program.
    '''
    headers = findHeaders(path)
    if headers is None:
        print("Couldn't find any headers in that path I'm afraid.")
    checked = getCheckedHeaders(path)
    if checked is None:
        writeNewChecked(headers) 
    diff = isDifferent(headers, checked)
    if diff:
        print("Found some juicy new headers! Writing them now...")
        writeNewChecked(headers)
    else:
        print("No new headers found.")
    return diff


def main():
    args = docopt(__doc__, version='Header Checker -- SUPER RADICAL EDITION')
    path = cleanPath(args['<path>'])
    updateHeaders(path, args['--build'])


if __name__ == "__main__":
    main() 

