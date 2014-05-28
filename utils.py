#!usr/bin/env python

'''

utils.py

by Mitchell Nordine

Module containing miscellaneous utils for BuildManager.py modules.

'''


import os, ntpath


def cleanPath(path):
    '''Function for ensuring a working path has been passed.'''
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


