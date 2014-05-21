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
from pprint import pprint
import tmuxp


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


def runInNewTmuxWindow(path):
    serv = tmuxp.Server()
    sesh = serv.getById('$0')
    win = sesh.findWhere({"window_name" : "RUN_JEN"})
    if win:
        pane = win.attached_pane()
    else:
        win = sesh.new_window(attach=True, window_name="RUN_JEN")
        pane = win.attached_pane()
    pane.send_keys('cd '+path, enter=True)
    pane.send_keys('make run', enter=True)


def runInNewTab():
    os.system("""osascript -e 'tell application "Terminal" to activate' -e 'tell application "System Events" to tell process "Terminal" to keystroke "t" using command down' -e 'tell application "Terminal" to do script "make run" in selected tab of the front window'""")


def main():
    args = docopt(__doc__, version='Build Manager -- SUPER RADICAL EDITION')
    path = cleanPath(args['<makePath>'])
    headerDiff = updateHeaders(path)
    s = genMakeString(headerDiff)
    os.system(s)
    if (args['--run']):
        print("Running dis business...")
        try:
            runInNewTmuxWindow(path)
        except Exception, e:
            msg = str(e) + "\nNow trying to open in new tab instead..."
            print(msg)
            try:
                runInNewTab()
            except Exception, e:
                msg = str(e) + "\nNow just going to run in Vim window instead..."
                print(msg)
                os.system("make run")
    else:
        print("No run command found, finishing up :-)")


if __name__ == "__main__":
    main() 

