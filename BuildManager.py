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
    BuildManager.py [--lang=<ext>] [-r | --run] <path>

Options:
    -h --help           Show this screen.
    -v --version        Show version.
    -r --run            Run the program following building.
    --lang=<ext>        Language with extension.

'''


import os, tmuxp
from docopt import docopt
from RustBM import RustBuildManager
from CppBM import CppBuildManager
from PermissionsChecker import PermissionsChecker
from utils import *


def getMakePath(lang, path):
    if lang == "cpp":
        return getCppMakePath(path)
    elif lang == "rust":
        return getRustMakePath(path)



def runInNewTmuxWindow(path, runstring):
    serv = tmuxp.Server()
    sesh = serv.getById('$0')
    win = sesh.findWhere({"window_name" : "RUN_"+pathLeaf(path)})
    winname = "RUN_"+pathLeaf(path)
    if not win:
        win = sesh.new_window(attach=True, window_name=winname)
    else:
        win = sesh.select_window(winname)
    pane = win.attached_pane()
    pane.send_keys('cd '+path, enter=True)
    print("Running the file found in "+path+" in window "+winname)
    pane.send_keys(runstring, enter=True)


def runInNewTab():
    os.system("""osascript -e 'tell application "Terminal" to activate' -e 'tell application "System Events" to tell process "Terminal" to keystroke "t" using command down' -e 'tell application "Terminal" to do script "make run" in selected tab of the front window'""")


def run(path, runstring):
    try:
        print("Attempting to run in new Tmux window...")
        runInNewTmuxWindow(path, runstring)
    except Exception, e:
        print("Failed to run in new Tmux window:")
        print(str(e))
        print("Now trying to open in new tab instead...")
        try:
            runInNewTab(runstring)
        except Exception, e:
            print("Failed to run in new Terminal tab:")
            print(str(e))
            print("Now just going to run in Vim window instead...")
            os.system(runstring)



def getBuildManager(ext):
    if ext == ".cpp" or ext == ".h" or ext == ".hpp":
        return CppBuildManager()
    elif ext == ".rs" or ext == "rust":
        return RustBuildManager()
    else:
        print("ext = "+ext)
        print("Entered language not found - cpp will be assumed.") # Should automatically find language.
        return CppBuildManager()


def main():
    args = docopt(__doc__, version='Build Manager -- SUPER RADICAL EDITION')
    buildmanager = getBuildManager(args.get('--lang'))
    path = cleanPath(args.get('<path>'))
    path = buildmanager.getBuildPath(path)
    origin = os.getcwd()
    PermissionsChecker(path)
    os.chdir(origin)
    buildmanager.build()
    if (args['--run']):
        run(path, buildmanager.getRunString())
    else:
        print("No run command found, finishing up :-)")


if __name__ == "__main__":
    main() 

