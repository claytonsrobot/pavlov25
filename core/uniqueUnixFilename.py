'''
Title: uniqueUnixFilename.py
Author: Clayton Bennett
Created: 23 June 2023

Input: filename(string),filetype(string)
'''
from datetime import datetime
import time


def mark():
    now = datetime.now()
    now_unix = time.mktime(now.timetuple())
    now_unix = int(now_unix)
    return now_unix

def uniqueUnixFilename(filename): # not used anyways.

    now_unix = mark()
    filename_out = filename+'_'+str(now_unix)
    return filename_out

def uniqueUnix():
    now_unix = mark()
    nowUnix = str(now_unix)
    return nowUnix

'''
find last hyphen
find all text between last hypen and '.py'
add v
This is here for versioning of the name

scriptname = os.path.basename(__file__)
scriptname = 'test_me_34June20.py'
leftbookend = scriptname.rfind('_')# final hyphen
rightbookend = scriptname.rfind('.py')
versionname = scriptname[leftbookend+1:rightbookend]
#result = re.search('_(.*).py', scriptname) # extract text between last hypthen and the .py filetype
#versionname =result.group(1)
print(versionname)
'''

