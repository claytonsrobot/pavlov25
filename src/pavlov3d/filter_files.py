'''
Title: filter_files.py
Author: Clayton Bennett
Created: 01 June 2024

Purpose:
Generalized file filtering that can be called from the gui, from a cli, or from json import scripts / modules.

This should be a functon rather than a class. So that we can keep using it over and over again in gui.
'''
import os
import platform # assumes local is windows and server is linux for vercel
from src.pavlov3d import environment

if 'win' in platform.platform().lower():
    vercel=False
else:
    vercel=True


def convert_filter_patterns_to_lists(pattern_and,pattern_or,pattern_not):
    #.lower().split(",")
    pattern_and = pattern_and.lower().split(",")
    pattern_or = pattern_or.lower().split(",")
    pattern_not = pattern_not.lower().split(",")
    return pattern_and,pattern_or,pattern_not

def remove_blank_entry(pattern):
    if not(pattern==['']):
        if ' ' in pattern:
            pattern.remove(' ')
        if '' in pattern:
            pattern.remove('')
    return pattern

def snip_filenames_from_request_session(filepaths):
    filenames = []
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        filenames.append(filename)
    return filenames

def get_filtered_list_dict(filetype_list,dirname):
    # i need a way for this to work either way, in terms of grouping-by-directory
    """
    Returns dictionary of files
    Key is short filename
    Value is the full filename and path

    :return: Dictionary of demo files
    :rtype: Dict[str:str]
    """
    
    files_dict = {}
    dirname=dirname.replace('*','')
    if environment.vercel() == False:
        dirname = dirname.replace('/','\\')
    else:
        dirname = dirname.replace('\\','/')

    if isinstance(filetype_list,list):
        pass
    elif isinstance(filetype_list,str):
        filetype_list = filetype_list.split(",")
    else:
        pass
        print ("Check the value of filetype_allowed in the chosen import plugin.")
        print('The variable assigment should look like this: ')
        print('Example 1: self.filetype_allowed = ["gpx"]')
        print('Example 2: self.filetype_allowed = ["csv","xlsx","xls"]')

    print(f"filetype_list = {filetype_list}")
    #print(f"filetype_list -d = {filetype_list.__dict__}")
    for i,filetype in enumerate(filetype_list): # access the filetype_list somehow
        if not(filetype.startswith(".")):
            filetype_list[i]="."+filetype  
        else:
            pass
    
    for filename in os.listdir(dirname):
        #print(f'filename = {filename}')
        #if filename.endswith('.csv') or filename.endswith('.xlsx'):

        #if filename.endswith('.gpx'): # what if you import the user input config here

        for filetype in filetype_list:
            #print(f"filetype = {filetype}")
            if filename.endswith(filetype): # what if you import the user input config here
                fname_full = os.path.join(dirname, filename)
                if filename not in files_dict.keys():
                    files_dict[filename] = fname_full

            else:
                #reject files of wrong type
                #print(f"Reject: {filename}")
                pass
                    
    return files_dict

def get_filelist_filetyped(filetype_list,dirname): # generalize please, or reference filetypes from config file or from import plugin
    if isinstance(filetype_list,list):
        file_list = sorted(list(get_filtered_list_dict(filetype_list,dirname).keys()))
    else:
        print(f"Error: filetype_list is not of type list")

    return file_list

def get_vercel_session_filelist_csvxlsx(dirname,session_object):
    list_names, list_blob_urls, list_objects = session_object.get_list_csv_current()
    file_list = list_names
    print(f'ff: list_names = {list_names}')
    list_names, list_blob_urls, list_objects = session_object.get_list_csv_current()
    return file_list

def check_filelist(dirname,pattern_and,pattern_or,pattern_not,filetype_list):
    pattern_and,pattern_or,pattern_not = convert_filter_patterns_to_lists(pattern_and,pattern_or,pattern_not)
    # converted to list
    pattern_and = remove_blank_entry(pattern_and)
    pattern_or = remove_blank_entry(pattern_or)
    pattern_not = remove_blank_entry(pattern_not)

    file_list = get_filelist_filetyped(filetype_list,dirname) # generalize please, or reference filetypes from config file or from import plugin
    fresh_list = [x.lower() for x in file_list]
    #return fresh_list


    def make_relevant_dictionary_to_preserve_original_letter_case(file_list,fresh_list):
        dict_files=dict.fromkeys(fresh_list)
        for i,t in enumerate(list(dict_files.keys())):
            dict_files[t] = file_list[i]
        return dict_files
    
    dict_files = make_relevant_dictionary_to_preserve_original_letter_case(file_list,fresh_list)

    # deal with pattern_or
    if not(pattern_and==['']):
        for pattern_and_i in pattern_and:
            fresh_list = list(filter(lambda filt: pattern_and_i.strip() in filt, fresh_list))
    if not(pattern_not==['']):
        for pattern_not_i in pattern_not:
            fresh_list = [filt for filt in fresh_list if pattern_not_i.strip() not in filt]
    
    if not(pattern_or==['']):
        i=0
        while i<len(fresh_list):
            filename = fresh_list[i]
            keep=False
            for pattern_or_i in pattern_or:
                if pattern_or_i.strip() in filename:
                    keep=True
            if keep==False:
                #print(f'remove: {filename}')
                fresh_list.remove(filename)
            elif keep==True:
                i+=1
    
    # instead return the unadulterated original values at the same indicies of the current fresh_list
    # match keys to list to get references for dictionary python

    original_case_list_filtered = [dict_files.get(original_case) for original_case in fresh_list]
    #filtered_file_list = original_case_list
    #return filtered_file_list
    return original_case_list_filtered # this way, you can type any case into the filter fields, but the original case will be shwon in window['-FILELISTBOX-']

