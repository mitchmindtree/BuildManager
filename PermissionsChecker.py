#!usr/bin/env python

'''

PermissionsChecker.py

by Mitchell Nordine

Module used for recursively checking file permissions for a given path.
Mainly used in BuildManager.py.

'''


import os, getpass, pwd, grp


class PermissionsChecker():

    def __init__(self, path):
        self.path = path
        self.user = getpass.getuser()
        self.checkPermissions()


    def findOwner(self, path):
        try:
            return pwd.getpwuid(os.stat(path).st_uid).pw_name
        except Exception, e:
            return self.user


    def arePermissionsOk(self, path):
        for p in os.listdir(self.path):
            pj = os.path.join(self.path, p)
            if os.path.isdir(pj):
                if not self.arePermissionsOk(pj):
                    return False
            if self.user != self.findOwner(pj):
                return False
        return True


    def requestChown(self):
        uid = pwd.getpwnam(self.user).pw_uid
        for root, dirs, files in os.walk(self.path):
            for d in dirs:
                os.chown(os.path.join(root, d), uid, -1)
            for f in files:
                os.chown(os.path.join(root, f), uid, -1)


    def checkPermissions(self):
        print("Checking permissions...")
        if not self.arePermissionsOk(self.path):
            print("BuildManager has found files owned by someone other than the current user. This may cause problems during the Makefile build process. BuildManager will fix ownership of all files in the Makefile directory for you.")
            try:
                self.requestChown()
                print("Great success! Permissions changed.")
            except Exception, e:
                print("BuildManager failed to fix ownership. Here's the error we got:")
                print(str(e))
                try:
                    print("Will now try to fix permissions via OS chown command. It will likely require your permission.")
                    os.system("sudo chown -R "+self.user+" "+self.path)
                    print("Great success! Permissions changed.")
                except Exception, e:
                    print("Failed to fix permissions:")
                    print(str(e))
        else:
            print("Permissions OK.")


