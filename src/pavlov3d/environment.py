'''
Title: environment.py
Author: Clayton Bennett
Created: 23 July 2024
'''
import platform
import sys

def vercel():
    #return not(windows()) # conflated, when using any linux that is not a webserver
    # the important questions is actually "are we running on a webserver?"
    return False # hard code this

def windows():
    if 'win' in platform.platform().lower():
        windows=True
    else:
        windows=False
    return windows
    
def pyinstaller():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        pyinstaller = True
    else:
        pyinstaller = False
    return pyinstaller

def frozen():
    if getattr(sys, 'frozen', True):
        frozen = True
    else:
        frozen = False
    return frozen

def operatingsystem():
    return platform.system() #determine OS
