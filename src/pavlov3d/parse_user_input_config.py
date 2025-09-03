'''
Title: parse_user_input_config.py
Created: 27 February 2024 
Author: Clayton Bennett
'''
import os
from pathlib import Path
import json 
import datetime


class parse_user_input_config:
    def __init__(self):
        self.name = Path(__file__).name.lower().removesuffix('.py')
        self.filetype='json'
        self.loaded_data= None
        self.filename = None

    def load_json(self,filename):
        with open(self.filename,"r") as file:
            #self.loaded_data = json.load(file)
            self.loaded_data = json.loads(file.read())
        print('parse 2')

    def load_json_to_gui(self,filename,gui_object):
        self.filename = filename
        print(f'\nConfigurtation file loaded to populate user inputs: {self.filename}\n')
        #print(f'gui_object.main_window.key_dict.keys()={gui_object.main_window.key_dict.keys()}')
        with open(self.filename,"r") as file:
            #self.loaded_data = json.load(file)
            self.loaded_data = json.loads(file.read())
        print('parse 1')
        for key,value in self.loaded_data.items():
            if key in gui_object.main_window.key_dict.keys(): 
                gui_object.main_window[key].update(value)
        gui_object.main_window['-STATUS1-'].update(f'Input values loaded from {self.filename}')
        
    def preview(self,filename):
        with open(filename,"r") as file:
            loaded_data = json.load(file)
        for key,value in loaded_data.items():
            print(key,':',value)

    def save_gui_values_as_file(self,filename,gui_object):
        print('Config file custom save is not yet operational')
        print(f'filename = {filename}')
        today = datetime.date.today()
        # this is bullshit, change the keys to match the import
        dictionary = {
            "project_id":gui_object.save_config_window["-SAVE-CONFIG-FILENAME-"].Get(),
            "dev":"Clayton Bennett, probably",
            "date":str(today),  
            "project description":"Custom inputs saved from GUI, no details provided",
            "import_filetype_dropdown":gui_object.main_window["import_filetype_dropdown"].Get(),
            "data_directory":gui_object.main_window["data_directory"].Get(),
            "column_time":gui_object.main_window["column_time"].Get(),
            "column_height":gui_object.main_window["column_height"].Get(),
            "column_depth":gui_object.main_window["column_depth"].Get(),
            "column_color":gui_object.main_window["column_color"].Get(),
            "columns_metadata":gui_object.main_window["columns_metadata"].Get(),
            "-SELECT_DIR-":gui_object.main_window["-SELECT_DIR-"].Get(),
            "-SELECT_FILES-":gui_object.main_window["-SELECT_FILES-"].Get(),
            "export_directory":gui_object.main_window["export_directory"].Get(),
            "filter_files_include_and":gui_object.main_window["filter_files_include_and"].Get(),
            "filter_files_include_or":gui_object.main_window["filter_files_include_or"].Get(),
            "filter_files_exclude":gui_object.main_window["filter_files_exclude"].Get(),
            "-HOLDBROWSE-":gui_object.main_window["-HOLDBROWSE-"].Get(),
            "group_names":gui_object.main_window["group_names"].Get(),
            "subgroup_names":gui_object.main_window["subgroup_names"].Get(),
            "data_start_idx":gui_object.main_window["data_start_idx"].Get(),
            'stack_direction_groups':gui_object.main_window['stack_direction_groups'].Get(),
            'stack_direction_subgroups':gui_object.main_window['stack_direction_subgroups'].Get(),
            'stack_direction_curves':gui_object.main_window['stack_direction_curves'].Get(),
            "import_style_dropdown":gui_object.main_window["import_style_dropdown"].Get(),
            "export_style_dropdown":gui_object.main_window["export_style_dropdown"].Get(),
            "color_style_dropdown":gui_object.main_window["color_style_dropdown"].Get(),
            "import_style_plugin":gui_object.main_window["import_style_plugin"].Get(),
            "export_style_plugin":gui_object.main_window["export_style_plugin"].Get(),
            "color_style_plugin":gui_object.main_window["color_style_plugin"].Get(),
            "-ASCII_RADIO-":gui_object.main_window["-ASCII_RADIO-"].Get(),
            "-BIN_RADIO-":gui_object.main_window["-BIN_RADIO-"].Get(),
            "-STATUS1-":gui_object.values["-STATUS1-"]
        } # add values for text label directions

        json_object = json.dumps(dictionary, indent=4)
        with open(filename, "w") as outfile:
            outfile.write(json_object)
            # this junt will override if you use the same name
    




