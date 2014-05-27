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


import os, getpass, tmuxp, pwd, grp, ntpath
from docopt import docopt
from HeaderChecker import updateHeaders
from pprint import pprint


def isMakefileHere(path):
    if os.path.isfile(os.path.join(path, "Makefile")):
        return True
    elif os.path.isfile(os.path.join(path, "makefile")):
        return True
    else:
        return False


def getCppMakePath(path):
    p = path
    try:
        print("Attempting to find Makefile path...")
        for i in range(10):
            if isMakefileHere(p):
                print("Makefile path found: " + p)
                return p
            else:
                p = os.path.dirname(p)
    except Exception, e:
        print("BuildManager couldn't find the Makefile path... Here's the error:")
        print(str(e))
        return path
    print("BuildManager couldn't find the Makefile path. Will try original path: " + path)
    return path


def getRustMainFile(path):
    files = [f for f in os.listdir(path) if f.endswith(".rs")]
    if any(f for f in files if open(os.path.join(path, f), 'r').read().find("fn main(") != -1):
        return f
    else:
        return None


def getRustMakePath(path):
    p = path
    try:
        print("Attempting to find rust main file path...")
        for i in range(10):
            rustmain = getRustMainFile(p)
            if rustmain is not None:
                print("Rust main file found: " + rustmain)
                return os.path.join(p, rustmain)
            else:
                p = os.path.dirname(p)
    except Exception, e:
        print("BuildManager couldn't find the Makefile path... Here's the error:")
        print(str(e))
        return path
    print("BuildManager couldn't find the Makefile path. Will try original path: " + path)
    return path


def getMakePath(lang, path):
    if lang == "cpp":
        return getCppMakePath(path)
    elif lang == "rust":
        return getRustMakePath(path)


def buildCpp(path): 
    print("Now attempting to build makefile.")
    origin = os.getcwd()
    os.chdir(path)
    headerDiff = updateHeaders(path)
    s = genMakeString(headerDiff)
    os.system(s)
    os.chdir(origin)


def buildRust(path):
    print("Now attempting to build rust file.")
    origin = os.getcwd()
    os.chdir(os.path.dirname(path))
    os.system("rustc "+path)
    os.chdir(origin)


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


def pathLeaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def runCpp(path, pane, winname):
    pane.send_keys('make run', enter=True)
    print("Running the Makefile found in "+path+" in window "+winname)


def runRust(rustmain, pane, winname):
    pane.send_keys('./'+os.path.splitext(rustmain)[0])
    print("Running the Rust main file "+rustmain+" in window"+winname)


def runInNewTmuxWindow(lang, path):
    serv = tmuxp.Server()
    sesh = serv.getById('$0')
    if lang == "rust":
        rustmain = pathLeaf(path)
        path = os.path.dirname(path)
    win = sesh.findWhere({"window_name" : "RUN_"+pathLeaf(path)})
    winname = "RUN_"+pathLeaf(path)
    if not win:
        win = sesh.new_window(attach=True, window_name=winname)
    else:
        win = sesh.select_window(winname)
    pane = win.attached_pane()
    pane.send_keys('cd '+path, enter=True)
    if lang == "cpp":
        runCpp(path, pane, winname)
    elif lang == "rust":
        path = os.path.join(path, rustmain)
        runRust(rustmain, pane, winname)


def runInNewTab():
    os.system("""osascript -e 'tell application "Terminal" to activate' -e 'tell application "System Events" to tell process "Terminal" to keystroke "t" using command down' -e 'tell application "Terminal" to do script "make run" in selected tab of the front window'""")


def findOwner(path):
    try:
        return pwd.getpwuid(os.stat(path).st_uid).pw_name
    except Exception, e:
        return getpass.getuser()


def arePermissionsOk(user, path):
    for p in os.listdir(path):
        pj = os.path.join(path, p)
        if os.path.isdir(pj):
            if not arePermissionsOk(user, pj):
                return False
        if user != findOwner(pj):
            return False
    return True


def requestChown(user, path):
    uid = pwd.getpwnam(user).pw_uid
    for root, dirs, files in os.walk(path):
        for d in dirs:
            os.chown(os.path.join(root, d), uid, -1)
        for f in files:
            os.chown(os.path.join(root, f), uid, -1)


def checkPermissions(user, path):
    print("Checking permissions...")
    if not arePermissionsOk(user, path):
        print("BuildManager has found files owned by someone other than the current user. This may cause problems during the Makefile build process. BuildManager will fix ownership of all files in the Makefile directory for you.")
        try:
            requestChown(user, path)
            print("Great success! Permissions changed.")
        except Exception, e:
            print("BuildManager failed to fix ownership. Here's the error we got:")
            print(str(e))
            try:
                print("Will now try to fix permissions via OS chown command. It will likely require your permission.")
                os.system("sudo chown -R "+user+" "+path)
                print("Great success! Permissions changed.")
            except Exception, e:
                print("Failed to fix permissions:")
                print(str(e))
    else:
        print("Permissions OK.")


def getLanguage(ext):
    if ext == ".cpp" or ext == ".h" or ext == ".hpp":
        return "cpp"
    elif ext == ".rs" or ext == "rust":
        return "rust"
    else:
        print("ext = "+ext)
        print("Entered language not found - cpp will be assumed.") # Should automatically find language.
        return "cpp"


def main():
    args = docopt(__doc__, version='Build Manager -- SUPER RADICAL EDITION')
    lang = getLanguage(args.get('--lang'))
    path = cleanPath(args.get('<path>'))
    path = getMakePath(lang, path)
    origin = os.getcwd()
    if lang == "cpp":
        os.chdir(path)
        checkPermissions(getpass.getuser(), path)
    elif lang == "rust":
        os.chdir(os.path.dirname(path))
        checkPermissions(getpass.getuser(), os.path.dirname(path))
    os.chdir(origin)
    if lang == "cpp":
        buildCpp(path)
    elif lang == "rust":
        buildRust(path)
    if (args['--run']):
        try:
            print("Attempting to run in new Tmux window...")
            runInNewTmuxWindow(lang, path)
        except Exception, e:
            print("Failed to run in new Tmux window:")
            print(str(e))
            print("Now trying to open in new tab instead...")
            try:
                runInNewTab()
            except Exception, e:
                print("Failed to run in new Terminal tab:")
                print(str(e))
                print("Now just going to run in Vim window instead...")
                os.system("make run")
    else:
        print("No run command found, finishing up :-)")


if __name__ == "__main__":
    main() 

