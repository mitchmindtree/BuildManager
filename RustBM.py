#!usr/bin/env python

'''

RustBM.py

by Mitchell Nordine

Module containing build procedures for Rust (.rs) compilation.

'''


import os
from BM import BuildManager


class RustBuildManager(BuildManager):


    def getMainFile(self, path):
        if os.path.isfile(os.path.join(path, "main.rs")):
            return "main.rs"
        elif os.path.isfile(os.path.join(path, "Main.rs")):
            return "Main.rs"
        else:
            return None


    def getBuildPath(self, path):
        p = path
        try:
            print("Attempting to find rust build path...")
            for i in range(10):
                f = self.getMainFile(p)
                if not f == None:
                    print("Rust main file path found: " + os.path.join(p, f))
                    self.path = p
                    self.mainfile = f
                    return p
                else:
                    p = os.path.dirname(p)
        except Exception, e:
            print("BuildManager couldn't find the Makefile path... Here's the error:")
            print(str(e))
            self.path = path
            self.mainfile = "main.rs"
            return path
        print("BuildManager couldn't find the Makefile path. Will try original path: " + path)
        self.path = path
        self.mainfile = "main.rs"
        return path


    def build(self):
        print("Now attempting to build rust file.")
        origin = os.getcwd()
        os.chdir(self.path)
        os.system("rustc "+os.path.join(self.path, self.mainfile))
        os.chdir(origin)


    def getRunString(self):
        return './'+os.path.splitext(self.mainfile)[0]


