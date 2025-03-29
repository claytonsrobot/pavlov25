"""
Title: directories.py
Author: Clayton Bennett
Created: 24 December 2024

Purpose:
Build project directory
Add import, export, and config directories as necessary
Add config entry point json file, which can point to config collection

Add shortcuts to imports and exports to central drectories?
"""
import time
import os
from pathlib import Path
from src import environmental
from src.directories import Directories 
from pprint import pprint
import shutil
import sys
import subprocess

def populate_new_project_dir(project_name="default-sample",choice=""):

    #https://python.plainenglish.io/create-your-python-structure-b545583c8a2a
    # Define the directory structure and file names
    
    # should copy a sample. Hidden when unpacked.
    structure_sample = {
        f"{project_name}":["config_entry.json"],
        f"{project_name}/configs":["config_inputs_default.json",
                                   "config_inputs_template.json"],
        
        f"{project_name}/exports":["sample_export.fbx",
                                   "sample_export.glb",
                                   #"sample_export.blend",
                                   "sample_export_front.png",
                                   "sample_export_top.png",
                                   "sample_export_right.png",
                                   "sample_export_iso.png"],

        f"{project_name}/imports":["sample_import_groupA_subgroup1A.csv",
                                   "sample_import_groupA_subgroup2A.csv",
                                   "sample_import_groupA_subgroup3B.csv",
                                   "sample_import_groupA_subgroup4B.csv"],

        f"{project_name}/groupings":["sample_group_map_AB1234.csv"],   
    }

    # should copy an empty. Hidden when unpacked.
    structure_empty = {
        f"{project_name}":["config_entry.json"],
        f"{project_name}/configs":["config_inputs_default.json",
                                   "config_inputs_template.json",
                                   "README.md"],
        
        f"{project_name}/exports":["README.md"],

        f"{project_name}/imports":["README.md"],
                                   
        f"{project_name}/groupings":["sample_group_map_AB1234.csv",
                                     "README.md"],   
    }

    """ TAKEN FROM URL- THIS IS NOT THE PROPERTY OF PAVLOV SOFTWARE & SERVICES"""
    

    # Function to create directories and files with error handling
    def create_structure(structure):
        print("\nstructure\n")
        pprint(structure)
        for folder, files in structure.items():
            try:
                Path(folder).mkdir(parents=True, exist_ok=True)
                print(f"Directory {folder} created successfully.")
            except Exception as e:
                print(f"Error creating directory {folder}: {e}")
                continue
            
            for file in files:
                print(f"file = {file}")
                try:
                    file_path = Path(folder) / file
                    # copy instead of make blank
                    file_path.touch(exist_ok=True)
                    print(f"File {file_path} created successfully.")
                except Exception as e:
                    print(f"Error creating file {file_path}: {e}")

    # Create the directory and file structure
    if choice == "" or choice =="empty":
        print("\ncreate_structure\n")
        create_structure(structure_empty)
    elif choice == "sample":
        create_structure(structure_sample)
"""^^^above^^^ TAKEN FROM URL- THIS IS NOT THE PROPERTY OF PAVLOV SOFTWARE & SERVICES ^^^above^^^^"""

class DirectoryControl:

    @staticmethod
    def create_directory(path):
        directory = Path(path) 
        if directory.exists(): 
            print(f"The directory '{path}' already exists.") 
        else: 
            directory.mkdir(parents=True, exist_ok=True) # default 0o755 rwxrwxr-x
            #directory.mkdir(parents=True, exist_ok=True,mode=0o755) # rwxrwxr-x
            #directory.mkdir(parents=True, exist_ok=True,mode=0o777) # rwxrwxrwx
            DirectoryControl.populate_fresh_project_directory(path)
            print(f"The directory '{path}' has been created.") 
    
    @staticmethod
    def populate_fresh_project_directory():
        pass
        #

    @staticmethod
    def create_directory_with_structure(project_dir_name_str,option):
        # should copy existing files from stock library folder
        if project_dir_name_str == "" or project_dir_name_str is None:
            unix_mark = str(int(time.time()))
            project_dir_name_str = "pavlov-project_"+unix_mark

        else:
            pass
        print(f"os.getcwd() = {os.getcwd()}")
        print(f"Directories.get_program_dir() = {Directories.get_program_dir()}")

        os.chdir(Directories.get_program_dir()+"/projects/")
        populate_new_project_dir(project_dir_name_str,option)
        os.chdir(Directories.get_program_dir())

    @staticmethod
    def copy_project_directory(project_dir_name_str,option):
        
        new_dir = project_dir_name_str+"_copy-"+str(int(time.time())) 
        shutil.copytree(project_dir_name_str,new_dir)
        print(f"Directory copied to: {new_dir}")
        print(f"Current project: {Directories.get_project_dir()}")
        

    @staticmethod
    def list_subdirectories():
        pass

    # Example usage
    # print_directory_tree('/your/directory/path')

    @staticmethod
    def walk(path):
        if path is not None:
            return os.walk(path).send(None)
        else:
            return os.walk(os.getcwd()).send(None)
        
    @staticmethod
    def destroy_directory(path):
        if not(os.path.exists(path)):
            print("Path not found.")
            return True
        confirm = str(input("Confirm destroy directory (Y/n): "))
        if confirm.lower()=="y":
            try:
                os.path.rmdir(path)
            except:
                print("There is a problem, likely with permission.")
                print("Directory not destroyed.")
            else:
                print("Directory destroyed.")
            return None
            
        else:
            print("Directory not destroyed.")
            return False

def tree(dir_path, indent=''):
    #Prints the directory tree starting from the given path
    for item in os.listdir(dir_path):
        full_path = os.path.join(dir_path, item)
        if os.path.isdir(full_path):
            print(indent + '├── ' + item)
            tree(full_path, indent + '│   ')
        else:
            print(indent + '├── ' + item)
            
def openfile(line):
    
    filepath = str(line)
    print(f"filepath: {filepath}")
    if os.path.exists(filepath):
        try:
            if environmental.windows():
                os.startfile(str(filepath))
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, filepath])
        except: 
            print("The file exists but failed to open.")
    else:
        print("The identified file does not exist. Check the filetype.")

def opentxt(line):

    filepath = str(line)
    print(f"filepath: {filepath}")
    if os.path.exists(filepath):
        try:
            if environmental.windows():
                os.system(f"notepad {str(filepath)}")
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, filepath])
        except: 
            print("The file exists but failed to open.")
    else:
        print("The identified file does not exist. Check the filetype.")

def opendir(line):
    directory = str(line)
    print(f"filepath: {directory}")
    if os.path.exists(directory):
        try:
            if environmental.windows():
                os.startfile(str(directory))
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, directory])
        except: 
            print("The file exists but failed to open.")
    else:
        print("The identified file does not exist. Check the filetype.")
