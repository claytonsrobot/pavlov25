'''
Title:config_input
Author: Clayton Bennett
Created: 01 June 2024

'''
import os
import inspect
import json
import numpy as np
import platform # assumes local is windows and server is linux for vercel
import filter_files as ff
import environmental
from directories import Directories
from pprint import pprint
import toml_handler


if 'win' in platform.platform().lower():
    vercel=False
else:
    vercel=True

#from parse_user_input_config import parse_user_input_config

class ConfigInput:

    @classmethod
    def assign_scene_object(cls, scene_object):
        cls.style_object = scene_object.style_object
        cls.scene_object = scene_object

    def __init__(self):
        #self.config_entry_filename = r"config_entry.json"
        #self.grouping_entry_filename = r"grouping_entry.json"
        self.config_entry_filename = r"config_entry.toml"
        self.grouping_entry_filename = r"grouping_entry.toml"
        #self.script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.script_dir = Directories.get_program_dir()
        #self.config_entry_filepath = self.script_dir+'\\'+self.config_entry_filename # the old way, for local config
        #self.config_guide_filepath = self.config_directory+'\\config-guide.pdf'
        self.config_entry_filepath = Directories.get_config_dir()+f'{self.config_entry_filename}'
        self.grouping_entry_filepath = Directories.get_groupings_dir()+f'{self.grouping_entry_filename}'
        
        Directories.check_file(self.config_entry_filepath)
        Directories.check_file(self.grouping_entry_filepath)
        #self.script_dir+'\\'+self.config_entry_filename # the old way, for local config
        self.config_directory =Directories.get_config_dir()
        self.config_guide_filepath = self.config_directory+'\\config-guide.pdf'
        self.loaded_config = None

        self.import_style_dropdown = None # will stay none
        self.export_style_dropdown = None # will stay none
        self.color_style_dropdown = None # will stay none

        #self.filter_files_include_and = None
        #self.filter_files_include_or = None
        #self.filter_files_exclude = None

        self.export_directory = ""
    
    def load_config_entry(self):

        #script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        
        #load this, then get resuults, then feed
        
        #self.config_entry_filepath = Directories.get_program_dir()+'/media/json_uploads_pavlovuserinputconfig/'+self.config_entry_filename # web app config :: salute
        print(f"self.config_entry_filepath = {self.config_entry_filepath}")
        #loaded_config_entry_json = self.load_json(self.config_entry_filepath)
        loaded_config_entry_toml = toml_handler.load_toml(self.config_entry_filepath)
        #config_input_filename = loaded_config_entry_json["config_input_filename"]
        config_input_filename = loaded_config_entry_toml["entry"]["config_input_filename"]
        config_input_path = os.path.normpath(Directories.get_config_dir()+"\\"+config_input_filename)
        Directories.check_file(config_input_path)
        return config_input_path
    
    def load_grouping_entry(self):
        
        #loaded_grouping_entry_json = self.load_json(self.grouping_entry_filepath)
        loaded_grouping_entry_toml = toml_handler.load_toml(self.grouping_entry_filepath)
        #grouping_selection_filename = loaded_grouping_entry_json["grouping_selection_filename"]
        #grouping_algorithm = loaded_grouping_entry_json["algorithm"]
        grouping_selection_filename = loaded_grouping_entry_toml["grouping"]["grouping_selection_filename"]
        grouping_algorithm = loaded_grouping_entry_toml["grouping"]["algorithm"]
        grouping_selection_path = os.path.normpath(Directories.get_groupings_dir()+"\\"+grouping_selection_filename)
        Directories.check_file(grouping_selection_path)
        return grouping_selection_path,grouping_algorithm
    
    """
    def load_json(self,filename):
        # we need a way to check that the json file is formatted properly, namey that commas are in the right place, before attemptig to load itusing json.loads(), because otherwise it might freak out
        with open(filename,"r") as file:
            json_data = file.read()
        try:
            loaded_json = json.loads(json_data)
        except:
            print(f"The JSON file is not properly formatted. Check for missing and hanging commas.: {filename}")
            raise RuntimeError("Stopping execution")
        #print(f'{filename}: ')
        #print(json.dumps(self.loaded_config, indent=4))
        return loaded_json
        """
    
    def load_csv(self,filename):
        with open(filename,"r") as file:
            csv_data = np.genfromtxt(file, dtype=None, delimiter=',', skip_header=0).tolist() # test
            csv_data = np.array(csv_data)

        loaded_csv_array =np.nan_to_num(csv_data)
        
        loaded_csv_dict = {k:v for k,v in zip(loaded_csv_array[0], loaded_csv_array[1:].T)}        
        
        return loaded_csv_dict
    """
    def pull_specific_values_from_json_config_input_object(self,loaded_json):
        # not called, prior to 04 February 2025 nor after. See comparable code in user_input.pull_config_input_object()
        #self.loaded_config=loaded_json
        
        # convert this to a input dictionary, instead of assigning calues as attributes of self.
        # ideally this doesnt need mapping - the dictionary comes dfirect, and then some things are added
        #self.data_directory = loaded_json["data_directory"]
        #self.directory_file_list
        #ff
        pattern_and = self.loaded_config["filter_files_include_and"]
        pattern_or = self.loaded_config["filter_files_include_or"]
        pattern_not = self.loaded_config["filter_files_exclude"]
        group_names = self.loaded_config["group_names"]
        subgroup_names = self.loaded_config["subgroup_names"]


        #filter_files_object.directory = self.loaded_config["data_directory_relative"]
        # filters should exist outside of the gui.py file, and can be referenced from there and from here

        self.dict_groups_tiers = ff.define_groups(group_names,subgroup_names) # specific to group-by-text # redundant?

        self.stack_direction = [''] # use
        self.skiprows=int(self.loaded_config["data_start_idx"])-1   #38 # for CSV and XLSX import
        #self.tiers = dict()
        #self.stack_vector = None
        """

    def clean_imported_json_numerics(self,loaded_config):

        for key,value in loaded_config.items():
            #print(value)
            if isinstance(value,str):
                if value.isnumeric():
                    try:
                        loaded_config[key] = int(value) 
                    except Exception:# was not an interger
                        loaded_config[key] = float(value)
        return loaded_config

    def define_and_load_default_config_input(self):
        self.config_input_path = self.load_config_entry()
        self.grouping_selection_path, self.grouping_algorithm = self.load_grouping_entry()
        #config_input_object = ConfigInput() 

        #self.loaded_config = self.load_json(self.config_input_path)
        self.loaded_config = toml_handler.load_toml(self.config_input_path)["config"]
        self.loaded_config = self.assign_known_config_filenames(self.loaded_config,self.config_input_path,self.config_entry_filepath)
        self.loaded_config = self.clean_imported_json_numerics(self.loaded_config) # if the json is poorly formatted for nums

        #if str(self.grouping_selection_path).endswith(".json"):
        if self.grouping_algorithm == "group-by-text":
            #self.loaded_json_grouping = self.load_json(self.grouping_selection_path)
            self.loaded_grouping = toml_handler.load_toml(self.grouping_selection_path)
            #self.loaded_grouping_toml = self.clean_imported_json_numerics(self.loaded_grouping_toml)
            
        #elif str(self.grouping_selection_path).endswith(".csv"):
        elif self.grouping_algorithm == "group-by-map":
            self.loaded_csv_grouping = self.load_csv(self.grouping_selection_path)
            print(f"self.loaded_csv_grouping = {self.loaded_csv_grouping}")

        elif self.grouping_algorithm == "group-by-directory":
            # explore first and second level directories in the projects/{project_name}/"imports" folder
            pass

        self.determine_data_directory(self.loaded_config,self.script_dir)
        #self.determine_export_directory(self.loaded_config,self.script_dir)
        #self.pull_specific_values_from_json_config_input_object(self.loaded_config)
        if True: # force to show outdated (free simple) gui
            self.loaded_config["filter_files_include_and"] = ""
            self.loaded_config["filter_files_include_or"] = ""
            self.loaded_config["filter_files_exclude"] = ""
            self.loaded_config["filter_files_exclude"] = ""
            self.loaded_config["export_directory"] = ""
        pprint(f"loaded_config = {self.loaded_config}")
        return 
    
    def assign_known_config_filenames(self,loaded_config,config_input_path,config_entry_filepath):
        loaded_config.update({"config_input_path":config_input_path})
        loaded_config.update({"config_entry_filepath":config_entry_filepath})
        return loaded_config
    
    def determine_data_directory(self,loaded_config,script_dir):
        #self.data_directory = (script_dir+loaded_config["data_directory_relative"]).replace("\\","/")

        if vercel==False:
            # This is actually wrong, we have a different directory for the json config files
            #folder='\\media\\csv_uploads_pavlovdata\\'
            folder='\\imports\\'
            print(f"Directories.get_program_dir: {Directories.get_program_dir()}")
            self.data_directory = Directories.get_program_dir()+folder+'*'
            self.data_directory = Directories.get_project_dir()+folder+'*'
            print(f'self.data_directory = {self.data_directory}')
        else:
            folder='\\tmp\\'
            folder=self.scene_object.blob_dir+'/csv_uploads_pavlovdata/'
            self.data_directory = folder
        return True
        


    #def determine_export_directory(self,loaded_config,script_dir):
    #    self.export_directory = script_dir+loaded_config["export_directory_relative"]


if __name__ == "__main__":
    
    script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    config_directory = Directories.get_config_dir()
    filename = r"gui_defaults_01June24.json"
    filepath = config_directory+filename
    filepath = os.path.normpath(filepath)

    config_input_object = ConfigInput()
    #loaded_json= config_input_object.load_json(filepath)
    loaded_config= toml_handler.load_toml(filepath)
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

