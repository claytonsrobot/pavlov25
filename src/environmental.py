'''
Title: environmental.py
Author: Clayton Bennett
Created: 23 July 2024
'''
import platform
import sys
#import os
#import inspect
#import glob
#from pathlib import Path 
    
def vercel():
    if 'win' in platform.platform().lower():
        vercel=False
    else:
        vercel=True
    return vercel

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


"""
def find_temp_MEI_dir():
    print("find_temp_MEI_dir()")
    temp_dir = Path(getattr(sys,'_MEIPASS', Path.cwd()))

    return temp_dir """