"""
Title: directories.py
Author: Clayton Bennett
Created: 29 January 2025

Purpose: 
Keep directory assignment organized, particularly for using project folders.
Migrate away from directory amangement in environmental.py

Example:
from directories import Directories

"""
import os
import inspect
import json
from pathlib import Path

class Directories:
    core = None
    project = None
    configs = None
    exports = None
    imports = None
    groupings = None


    ## migrated
    #initial_program_dir = None
    #project_dir = None

    #setters
    @classmethod
    def set_core_dir(cls,path):
        cls.core = path
    @classmethod
    def set_project_dir(cls,path):
        # if a legitimate full path is not provided, assume that the project directory is within the core\projects\ directory
        if os.path.isdir(path):
            cls.project = path
        else:
            relative_path =  cls.get_core_dir()+"\\projects\\"+path
            if os.path.isdir(relative_path):
                cls.project = relative_path
        print(f"Project directory set: {cls.project}")
    """
    @classmethod
    def set_configs_dir(cls,path):
        cls.configs = path
    @classmethod
    def set_exports_dir(cls,path):
        cls.exports = path
    @classmethod
    def set_imports_dir(cls,path):
        cls.imports = path
    @classmethod
    def set_groupings_dir(cls,path):
        cls.groupings = path
        """

    # getters
    @classmethod
    def get_core_dir(cls):
        #return cls.core
        return cls.core
    @classmethod
    def get_program_dir(cls):
        return cls.get_core_dir()
    @classmethod
    def get_project_dir(cls):
        return cls.project
    @classmethod
    def get_config_dir(cls):
        return cls.get_project_dir()+"\\configs\\"
    @classmethod
    def get_export_dir(cls):
        return cls.get_project_dir()+"\\exports\\"
    @classmethod
    def get_import_dir(cls):
        return cls.get_project_dir()+"\\imports\\"
    @classmethod
    def get_groupings_dir(cls):
        return cls.get_config_dir()+"\\groupings\\"
    
    # migrated
    @classmethod
    def initilize_program_dir(cls): # called in CLI. Should also be called at other entry points.
        cls.set_core_dir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        print(f"cls.initial_program_dir = {cls.get_core_dir()}")
        #cls.initialize_startup_project()
    @classmethod
    def initialize_startup_project(cls):
        filename = "./projects/default-project.json"
        with open(filename,"r") as file:
            json_data = file.read()
        loaded_json = json.loads(json_data)
        cls.set_project_dir(cls.get_core_dir()+"\\projects\\"+loaded_json["project_directory"])

    @classmethod
    def check_file(cls,filepath):
        if not(os.path.isfile(filepath)):
            print(f"The file does not exist: {filepath}")
            #raise RuntimeError("Stopping execution")
            raise SystemExit
        else:
            # the file exists
            pass
    @classmethod
    def check_first_level_import_directory_names(cls):
        cls.get_import_dir() # path of top layer
        
        #group_names = [x[1] for x in os.walk(cls.get_import_dir())]
        group_names = next(os.walk(cls.get_import_dir()))[1]

        print(f"group_names = {group_names}")
        return group_names
    
    @classmethod
    def check_second_level_import_directory_names(cls,group_names):
        subgroup_names = []
        for group_name in group_names:
            subgroups_of_group = next(os.walk(cls.get_import_dir()+group_name))[1]
            subgroup_names.extend(subgroups_of_group)
        print(f"subgroup_names = {subgroup_names}")
        return subgroup_names

    @classmethod
    def check_third_level_import_file_names(cls,group_names,subgroup_names):
        file_paths = []
        file_names = []
        for group_name in group_names:
            for subgroup_name in subgroup_names: 
                directory_pathlib = Path(cls.get_import_dir()+group_name+"/"+subgroup_name)
                for file_path in directory_pathlib.iterdir():
                    if file_path.is_file():
                        file_paths.append(str(file_path))
                        filename = os.path.basename(str(file_path).replace('\\', '/'))
                        file_names.append(filename)
        print(f"file_paths = {file_paths}")
        
        # check how file paths are already assigned - assumed they are al in improrts/ 
        return file_paths, file_names