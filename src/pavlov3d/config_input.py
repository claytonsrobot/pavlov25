'''
Title:config_input
Author: Clayton Bennett
Created: 01 June 2024

'''
import numpy as np
import os
from pprint import pprint

import src.pavlov3d.filter_files as ff
import src.pavlov3d.grouping_by_directory
from pavlov3d.directories import Directories
import src.pavlov3d.toml_utils

#from parse_user_input_config import parse_user_input_config

class ConfigInput:

    @classmethod
    def assign_scene_object(cls, scene_object):
        cls.style_object = scene_object.style_object
        cls.scene_object = scene_object

    def __init__(self):
        self.config_entry_filename = r"config_entry.toml"
        self.grouping_entry_filename = r"grouping_entry.toml"
        self.script_dir = Directories.get_program_dir()
        #self.config_entry_filepath = Directories.get_program_dir()+'/media/json_uploads_pavlovuserinputconfig/'+self.config_entry_filename # web app config :: salute
        self.config_entry_filepath = Directories.get_config_dir() / self.config_entry_filename
        self.grouping_entry_filepath = Directories.get_groupings_dir() / self.grouping_entry_filename
        
        # Fail and quit if the file is not found. There is a better way to pause the shell instead.
        Directories.check_file(self.config_entry_filepath)
        Directories.check_file(self.grouping_entry_filepath)
        self.config_directory =Directories.get_config_dir()
        self.config_guide_filepath = self.config_directory / 'config-guide.pdf'
        self.loaded_config = None

        self.import_style_dropdown = None # will stay none
        self.export_style_dropdown = None # will stay none
        self.color_style_dropdown = None # will stay none

        self.export_directory = ""
    
    def load_config_entry(self): 
        loaded_config_entry_toml = src.pavlov3d.toml_utils.load_toml(self.config_entry_filepath)
        config_input_filename = loaded_config_entry_toml["entry"]["config_input_filename"]
        config_input_path = os.path.normpath(Directories.get_config_dir() / config_input_filename)
        Directories.check_file(config_input_path)
        return config_input_path
    
    def load_grouping_entry(self):
        loaded_grouping_entry_toml = src.pavlov3d.toml_utils.load_toml(self.grouping_entry_filepath)
        grouping_selection_filename = loaded_grouping_entry_toml["grouping"]["grouping_selection_filename"]
        grouping_algorithm = loaded_grouping_entry_toml["grouping"]["algorithm"]
        print(f"grouping_selection_filename = {grouping_selection_filename}") 
        
        if grouping_selection_filename is None:
            grouping_selection_path = None
        else:    
            grouping_selection_path = Directories.get_groupings_dir() / grouping_selection_filename
            Directories.check_file(grouping_selection_path)
        return grouping_selection_path,grouping_algorithm
    
    def load_csv(self,filename):
        with open(filename,"r") as file:
            csv_data = np.genfromtxt(file, dtype=None, delimiter=',', skip_header=0).tolist() # test
            csv_data = np.array(csv_data)
        loaded_csv_array =np.nan_to_num(csv_data)
        loaded_csv_dict = {k:v for k,v in zip(loaded_csv_array[0], loaded_csv_array[1:].T)}                
        return loaded_csv_dict

    def clean_imported_numerics(self,loaded_config):
        for key,value in loaded_config.items():
            if isinstance(value,str):
                if value.isnumeric():
                    try:
                        loaded_config[key] = int(value) 
                    except Exception:# was not an interger
                        loaded_config[key] = float(value)
        return loaded_config

    def define_and_load_default_config_input(self):
        print("config_input.define_and_load_default_config_input()")
        config_input_path = self.load_config_entry()
        self.grouping_selection_path, self.grouping_algorithm = self.load_grouping_entry()
        raw_loaded_config = src.pavlov3d.toml_utils.load_toml(config_input_path)["config"]
        #self.loaded_config = self.assign_known_config_filenames(raw_loaded_config,config_input_path,self.config_entry_filepath)
        self.loaded_config = self.clean_imported_numerics(raw_loaded_config) # if the json is poorly formatted for nums

        if self.grouping_algorithm == "group-by-text":
            self.raw_loaded_grouping = src.pavlov3d.toml_utils.load_toml(self.grouping_selection_path) # this does have a particalr
            self.loaded_grouping = (self.raw_loaded_grouping["grouping"]).copy() 
            src.pavlov3d.json_handler.export_to_json(self.loaded_grouping, Directories.get_group_by_text_intermediate_export_json_filepath())
        elif self.grouping_algorithm == "group-by-spreadsheet":
            #self.loaded_csv_grouping = self.load_csv(self.grouping_selection_path) # this will inherently have a different structure compared to the toml import. Hypothetically we could leverage functon overloading to manage this.
            self.loaded_grouping = self.load_csv(self.grouping_selection_path)
            src.pavlov3d.json_handler.export_to_json(self.loaded_grouping, Directories.get_group_by_spreadsheet_intermediate_export_json_filepath())

        elif self.grouping_algorithm == "group-by-directory":
            "Discern dictionary structure based on directory hierarchy"
            self.loaded_grouping = src.pavlov3d.grouping_by_directory.call(directory_path = Directories.get_import_dir())
            #defunct, moved to call: self.loaded_grouping = src.pavlov3d.grouping_by_directory.generate_directory_structure_v3(Directories.get_import_dir())
            #defunct, moved to call: src.pavlov3d.json_handler.export_to_json(self.loaded_grouping, Directories.get_group_by_directory_intermediate_export_json_filepath())


        #self.pull_specific_values_from_json_config_input_object(self.loaded_config)
        if True: # force to show outdated (free simple) gui
            self.loaded_config["filter_files_include_and"] = ""
            self.loaded_config["filter_files_include_or"] = ""
            self.loaded_config["filter_files_exclude"] = ""
            self.loaded_config["filter_files_exclude"] = ""
            self.loaded_config["export_directory"] = ""
        pprint(f"loaded_config = {self.loaded_config}")
        return self.loaded_config, self.loaded_grouping
    
    def assign_known_config_filenames(self,loaded_config,config_input_path,config_entry_filepath):
        # Manually add config names to the config itsef in order to pass them around with the config dictonary
        # This is a hack.
        loaded_config.update({"config_input_path":config_input_path})
        loaded_config.update({"config_entry_filepath":config_entry_filepath})
        return loaded_config
def get_n_tier_group_names_and_subgroup_names_and_file_names_from_group_by_directory_cij_loaded_grouping():
    "Generic"
    pass

def get_three_tier_group_names_and_subgroup_names_and_file_names_from_group_by_directory_cij_loaded_grouping(data):
    "Flat, based on text"
    group_names, subgroup_names, file_paths, file_names = get_three_tier_group_names_and_subgroup_names_and_file_names_from_group_by_directory_data(data = data)
    file_paths = [(Directories.get_project_dir() / file) for file in file_paths]

    return group_names, subgroup_names, file_paths, file_names

def get_three_tier_group_names_and_subgroup_names_and_file_names_from_group_by_directory_data(data):
    """
    Extracts group names, subgroup names, file paths, and file names from a three-tier directory structure.

    Args:
        data (dict): The directory structure returned by `generate_directory_structure_v2()`.

    Returns:
        tuple: (group_names, subgroup_names, file_paths, file_names)
            - group_names (list): Names of the top-level directories (groups).
            - subgroup_names (list): Names of second-tier directories (subgroups).
            - file_paths (list): Full paths of all files in the subgroups.
            - file_names (list): Names of all files in the subgroups.
    """
    group_names = []
    subgroup_names = []
    file_paths = []
    file_names = []

    # Root directory name
    root_directory = data["directory"]

    # Top-level directories (groups)
    for group in data.get("directories", []):
        group_name = group["directory"]
        group_names.append(group_name)

        # Second-tier directories (subgroups)
        for subgroup in group.get("directories", []):
            subgroup_name = subgroup["directory"]
            subgroup_names.append(subgroup_name)

            # Files within the subgroups
            for file in subgroup.get("files", []):
                file_names.append(file)
                file_paths.append(f"{root_directory}/{group_name}/{subgroup_name}/{file}")

    return group_names, subgroup_names, file_paths, file_names
    
    
if __name__ == "__main__":
    
    config_directory = Directories.get_config_dir()
    filename = r"gui_defaults_01June24.json"
    filepath = config_directory+filename
    filepath = os.path.normpath(filepath)

    config_input_object = ConfigInput()
    #loaded_json= config_input_object.load_json(filepath)
    loaded_config= src.pavlov3d.toml_utils.load_toml(filepath)
    #loaded_json_gui_expected_defaults = config_input_object.load_json(filepath)
    #loaded_json_kate_config = config_input_object.load_json(default_config_path)
    #print(json.dumps(loaded_json,indent=4))
    print('\n')
    print(loaded_config.keys())
    print('\n')

    #config_object = parse_user_input_config()
    #config_object.load_json_to_gui(filename = filename,gui_object = self)
    #config_object.save_gui_values_as_file(filepath,gui_object = self) # need a way sans gui

    #config_input_object.pull_specific_values_from_json_config_input_object(loaded_config)

