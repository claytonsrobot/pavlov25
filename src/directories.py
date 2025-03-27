"""
Title: directories.py
Author: Clayton Bennett
Created: 29 January 2025

Purpose: 
Keep directory assignment organized, particularly for using project folders.
Migrate away from directory amangement in environmental.py

Example:
from src.directories import Directories

"""
import os
import inspect
from src import toml_utils
from pathlib import Path
from src import environmental

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
        if environmental.vercel==False:
            return cls.get_project_dir()+"\\imports\\"
        elif environmental.vercel==True: # web app, blob
            folder='\\tmp\\' # https://maxson-engineering-notes.vercel.app/personal/pavlov3-d/chat-gpt-pavlov3-d-django-improvements-report/
            folder=cls.scene_object.blob_dir+'/csv_uploads_pavlovdata/' # blob=dir shold be known here.
            return folder
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
        filename_default_project_entry = "./projects/default-project.toml"
        loaded_entry = toml_utils.load_toml(filename_default_project_entry)
        cls.set_project_dir(cls.get_core_dir()+"\\projects\\"+loaded_entry["project_directory"])

    @staticmethod
    def check_file(filepath):
        if not(os.path.isfile(filepath)):
            print(f"The file does not exist: {filepath}")
            #raise RuntimeError("Stopping execution")
            raise SystemExit
        else:
            # the file exists
            return True
        
    @classmethod
    def get_group_names_and_subgroup_names_and_file_names_from_import_directory_hierarchy(cls,directory):
        # assumes three tiers - in future make modular to any size
        #directory = cls.get_import_dir()
        print(f"directory = {directory}")
        group_names = cls.check_first_level_import_directory_names(directory)
        subgroup_names = cls.check_second_level_import_directory_names(directory,group_names)
        file_paths, file_names = cls.check_third_level_import_file_names(directory,group_names,subgroup_names)
        return group_names, subgroup_names, file_paths, file_names

    @classmethod
    def check_first_level_import_directory_names(cls,directory):
        # looks at tree in grouping directory to assess group names 
        # cls.get_import_dir() # path of top layer
        #group_names = [x[1] for x in os.walk(cls.get_import_dir())]
        group_names = next(os.walk(directory))[1]
        print(f"group_names = {group_names}")
        return group_names
    
    @classmethod
    def check_second_level_import_directory_names(cls,directory,group_names):
        subgroup_names = []
        for group_name in group_names:
            subgroups_of_group = next(os.walk(directory+group_name))[1]
            subgroup_names.extend(subgroups_of_group)
        print(f"subgroup_names = {subgroup_names}")
        return subgroup_names

    @classmethod
    def check_third_level_import_file_names(cls,directory,group_names,subgroup_names):
        file_paths = []
        file_names = []
        for group_name in group_names:
            for subgroup_name in subgroup_names: 
                try:
                    directory_pathlib = Path(directory) / group_name / subgroup_name
                    for file_path in directory_pathlib.iterdir(): # special chars make it go whack
                        if file_path.is_file():
                            file_paths.append(str(file_path))
                            filename = os.path.basename(str(file_path).replace('\\', '/'))
                            file_names.append(filename)
                except Exception as e:
                    print(f"Error processing directory: {directory_pathlib}. Error: {e}")
        return file_paths, file_names
    
    @staticmethod
    def generate_directory_structure(root_dir):
        ## Example usage
        #root_directory = "/path/to/root"
        #directory_structure = generate_directory_structure(root_directory)
        directory_structure = {}
        for root, dirs, files in os.walk(root_dir):
            # Create a nested dictionary path based on the current root path
            current_level = directory_structure
            path_parts = os.path.relpath(root, root_dir).split(os.sep)
            for part in path_parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            # Add the files at the current root level, skipping 'desktop.ini'
            current_level["files"] = [file for file in files if file != 'desktop.ini']
        return directory_structure
