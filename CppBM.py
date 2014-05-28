#!usr/bin/env python

'''

CppBM.py

by Mitchell Nordine

Module containing build procedures for C++ compilation.

'''


import os
from BM import BuildManager
from HeaderChecker import updateHeaders


class CppBuildManager(BuildManager):


    def isMakefileHere(path):
        if os.path.isfile(os.path.join(path, "Makefile")):
            return True
        elif os.path.isfile(os.path.join(path, "makefile")):
            return True
        else:
            return False


    def getBuildPath(path):
        p = path
        try:
            print("Attempting to find Makefile path...")
            for i in range(10):
                if self.isMakefileHere(p):
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


    def build(path): 
        print("Now attempting to build makefile.")
        origin = os.getcwd()
        os.chdir(path)
        headerDiff = updateHeaders(path)
        s = self.genBuildString(headerDiff)
        os.system(s)
        os.chdir(origin)


    def genBuildString(headerDiff):
        '''Function that generates the make command string.'''
        if headerDiff:
            print("Sit Back, time to build cc_args along with project...")
            s = "make PROJECT_CC='~/.vim/bin/cc_args.py clang' PROJECT_CXX='~/.vim/bin/cc_args.py clang++ -std=c++11 -stdlib=libc++' -B"
        else:
            s = "make"
        return s


    def getRunString(self):
        return 'make run'


