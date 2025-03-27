'''
Author: Clayton Bennett
Date created: 23 September 2023
Name: gui.py

Future development:
Option to save overview chart.
Record previously used values.
Tool tips.
Consider adding in a "Estimated file size" readout above the Publish button. Number updates with changes to encoding and style radio buttons. Would require importing of data to identify count of data points.

Resources drawn from https://pypi.org/project/PySimpleGUI/.


Task:

10 October 2023:
    - Convert publish popup to a publish notice in the status bar on the main page. Which status bar?
11 October 2023:
    - Coonsider how to use multiple pages instead of one screen.
    0. Which GUI style would you like? (single page, multipage, command line)
    1. Where is your data?
    2. Choice: Use all data (quick select), or control which files are imported (show 2b)
    2b. File selection is based on patterns in file name. Is there a common text string in the files you want to keep? Seperate multiple entries with a comma. For any files you want to reject, based on file name, enter the reject pattern(s).
    2c. Do you want to peek at different files, to know if you want to include them or not?
    3. Data selection. Select based on available columns share by all files. Select based on availble columns, not shared by all files. Select based on text name entry. Select based on column number.
    4. Would you like to group data together? If yes, go to 4a.
    4a. Text names for all tier 1 groups. Text names for all tier 2 groups.
    5. Export directory - where should your export file end up? Same as import data, or select folder.
    6. What style would you like for you 3D data objects? Show examples
    - resolve return naming issues, upon exit. However, what about publish? Nah, leave the windo open. Keep the GUI simple for now, go work on the axes and the letters and the objects and the scaling and the groupins, oh godddddd.

25 November 2023:
This needs to be converted into a class. Prepare to add 'self.' so many times. I hate it.
The grouping needs to be performed - an algorithm for this possibly already exists - check the grouping subfolder.
We need multipage, for complex settings, to not overwhelm the user.
Should the interface close when we hit 'Publish'? Ideally, the process can continue with the GUI open, but this might require a 'parallel' process.
Big thing - we need the whole thing to launch and open without a default data directory populated. The default is great for testing, but not for a final user.

26 January 2024:
    Make filtering not case sensitive.
'''

#import PySimpleGUI as sg
import FreeSimpleGUI as sg
import os
#import pathlib # for chopping off filename when searching directory
#import pandas as pd # for data management
from user_input import UserInput as userInput_class
#from gui_export_control import GuiExportControl
#window_export_control = GuiExportControl.window_export_control
from src.directories import Directories

#pd.options.display.max_columns = None
#pd.options.display.max_rows = None

standardTextSize=6 # doesn't do anything
script_dir = Directories.get_core_dir()
default_data_directory = r"D:\Documents_main\Work\Pavlov\data_sources\SOCEM_data_2022_simple"

default_export_directory = r"C:/Users/clayton/Downloads" # not used, sent to temp instead
config_directory = Directories.get_config_dir()

default_config_path = config_directory+ r'\USGS_gratzer.json'
pervasive_dirname = default_data_directory

default_groups = "TypeA, TypeB, TypeC"
default_subgroups = "test0, test1, test2, test3, test4"

default_stack_direction_groups = "diagonal_stack"
default_stack_direction_subgroups = "time_stack"   
default_stack_direction_curves = "depth_stack"
values_stack_directions = ["Diagonal (Time and Depth)","Time","Depth"]
#values_stack_directions = ["Diagonal (Time and Depth)","Time","Depth","Radial"]

default_column_time="Time"#siteag
default_column_height="Force"#p
default_column_depth='default'
default_column_color='default'
default_columns_metadata=''#stationnm,agencycd,mediumcd,sampledt,year,sampletm,dttm,altva,declatva,declongva,nataqfrcd,aqfrcd,welldepthva
default_data_start_idx=1#14

export_filesize=10.4# this needs to do some math
check_box=False

class Gui:
    style_object = None
    allowed_keys = set(['data_directory','filenames','column_time','column_height','dict_groups_tiers'])
    internal_keys = set(['values','window'])
    user_input_object = None
                        
    @classmethod
    def assign_style_object(cls,style_object):
        cls.style_object=style_object
    
    @classmethod
    def assign_config_input_object(cls,config_input_object):
        cls.config_input_object=config_input_object

    @classmethod
    def assign_user_input_object(cls,user_input_object,cli_object):
        cls.user_input_object=user_input_object
        cls.user_input_object.assign_interface_object(cls)

    def __init__(self,optional_instance_name='gui'):
        self.optional_instance_name = optional_instance_name
        self.user_input_object = userInput_class() # 
        self.user_input_object.assign_interface_object(self)
        self.data_start_idx=default_data_start_idx
        
        self.__dict__.update((key, None) for key in self.allowed_keys)
        self.__dict__.update((key, None) for key in self.internal_keys)
        self.dict_groups_tiers = dict()
        self.selected_item = None

        self._set_known_styles()
        self.publish = False # stays false until the publish button is pushed. If exited and the publish button is never pushed, the program will exit in main.

        self.stack_direction_groups = default_stack_direction_groups
        stack_direction_subgroups = default_stack_direction_subgroups
        self.stack_direction_curves = default_stack_direction_curves
        self.selected_encoding = "BIN"
        self.export_directory = default_export_directory
        self.metadata_columns = None
        self.import_style_plugin = ''
        self.export_style_plugin = ''
        self.color_style_plugin = ''

        self.export_control_override = False
        self.export_control_window_object = None
                                          
    def _set_known_styles(self):

        self.import_style_dictionary = dict({"One File, One Sheet":f'plugins.import_plugin_CSV_2D',
                                             "More than One File, One Sheet Each":f'plugins.import_plugin_CSV_singleSheet_multiColumn'})

        self.export_style_dictionary = dict({"Triangle Column 3D":'plugins.export_plugin_createFBX_triangle_columns_3D',
                                             "Triangle Column 2D":'plugins.export_plugin_createFBX_triangle_columns_2D',
                                             "Line Graph 3D":'plugins.export_plugin_createFBX_lineGraph_3D',
                                             "Square Scatter 3D":'plugins.export_plugin_createFBX_square_depth',
                                             "Bar 2D":'plugins.export_plugin_createFBX_bar_2D',
                                             "Bar 3D":'plugins.export_plugin_createFBX_bar_3D'})#.py
        
        self.color_style_dictionary = dict({"Color per Datapoint Key":'plugins.color_plugin_singular_keys_barchart',
                                            "Color per Group":'plugins.color_plugin_per_group',
                                            "Color per Subgroup":'plugins.color_plugin_per_subgroup',
                                            "Color per Object":'plugins.color_plugin_per_curve',
                                            "Binned Color Gradient":'plugins.color_plugin_binned_gradient',
                                            "Smooth Color Gradient":'plugins.color_plugin_true_gradient'})
        
        self.dict_matID = dict({"Binned Gradient per Assigned Vector":'binned_gradient_color_model',
                                "Color per Datapoint Key":'barchart_keys_color_model',## this is actually good, it causes the known gui references and the unknown dynamic plugins to have a similar name, thus easier to add. settled.'
                                "Color per Object":'singular_color_model_per_curve',
                                "True Gradient per Assigned Vector":'true_gradient_color_model'})
        
        self.values_import_filetype = ['CSV / XLSX','STL']
            # use the assimp import packge(s)
        self.values_import_style = list(self.import_style_dictionary.keys())
        self.values_export_style = list(self.export_style_dictionary.keys())
        self.values_color_style = list(self.color_style_dictionary.keys())

        self.default_import_filetype_dropdown = self.values_import_filetype[0]
        self.default_import_style_dropdown = self.values_import_style[0]
        self.default_export_style_dropdown = self.values_export_style[0]
        self.default_color_style_dropdown = self.values_color_style[4]

    def get_file_list_dict(self):
        try:
            dirname = self.main_window['-DATA_DIRECTORY-'].Get()
        except:
            dirname = default_data_directory

        files_dict = {}
        for filename in os.listdir(dirname):
            if filename.endswith('.csv') or filename.endswith('.xlsx'):
                fname_full = os.path.join(dirname, filename)
                if filename not in files_dict.keys():
                    files_dict[filename] = fname_full
        return files_dict

    def get_file_list(self):
        file_list = sorted(list(self.get_file_list_dict().keys()))
        return file_list
 
    def check_filelist(self):
        file_list = self.get_file_list()
        fresh_list = [x.lower() for x in file_list]

        @staticmethod
        def make_relevant_dictionary_to_preserve_original_letter_case(file_list,fresh_list):
            dict_files=dict.fromkeys(fresh_list)
            for i,t in enumerate(list(dict_files.keys())):
                dict_files[t] = file_list[i]
            return dict_files
        dict_files = make_relevant_dictionary_to_preserve_original_letter_case(file_list,fresh_list)

        original_case_list = [dict_files.get(original_case) for original_case in fresh_list]
        return original_case_list # this way, you can type any case into the filter fields, but the original case will be shwon in window['-FILELISTBOX-']

    
    def window_additional_settings(self):

        layout = [
            [sg.Text('FBX File Encoding:'),sg.Radio("ASCII",group_id="encoding", key="-ASCII_RADIO-"),sg.Radio("BIN (default)",group_id="encoding", default=True, key="-BIN_RADIO-")],
            [sg.Text('Data Start (column # or row #):'), sg.Input(size=(6, 2),default_text=default_data_start_idx, key="data_start_idx")],
            [sg.Text('Stack Directions:')],
            [sg.Text('Scene:'),sg.Combo(size=(25, 1),default_value=default_stack_direction_groups, values = values_stack_directions,key="stack_direction_groups")], 
            [sg.Text('Groups:'),sg.Combo(size=(25, 1),default_value=default_stack_direction_subgroups, values = values_stack_directions,key="stack_direction_subgroups")],
            [sg.Text('Subgroup:'),sg.Combo(size=(25, 1),default_value=default_stack_direction_curves, values = values_stack_directions,key="stack_direction_curves")],
            [sg.Text('**imagine example graphics here**')],
            [sg.Button('Okay, Apply Settings'), sg.Button('Nevermind, Exit')],
            ]
        settings_window = sg.Window('Addtional Settings', layout, size=(370, 250),resizable=True)
        self.settings_window = settings_window
        while True:
            event, self.settings_values = settings_window.read()
            if event == sg.WIN_CLOSED or event == "Exit" or event=='Nevermind, Exit':
                break
            elif event=='Okay, Apply Settings':
                feedme=1
        settings_window.close()
        return


    def run_and_get_inputs(self):
        sg.theme('DarkBlue13') 
        layout = [
            [sg.Text('Thank you for using Pavlov!'),sg.Button("Instructions"),sg.Button('See Examples')],
            [sg.Text('')],
            [sg.Text('How many files do you want to import?:'),
            sg.Combo(size=(33, 1),default_value=self.default_import_style_dropdown, values = self.values_import_style,key="import_style_dropdown")],
            [sg.Text('Where are your files?:'), sg.Input(size=(60, 1),default_text=default_data_directory, enable_events = True,key="-DATA_DIRECTORY-")],
            [sg.Text('_____________________________________________________________________________________')],
            [sg.Text('Please identify which data columns should correspond to model directions and model color:')],
            [sg.Text('Time:'), sg.Input(size=(12, 1),default_text=default_column_time, key="column_time"),
            sg.Text('Height:'), sg.Input(size=(12, 1),default_text=default_column_height, key="column_height"),
            sg.Text('Depth:'), sg.Input(size=(12, 1),default_text=default_column_depth, key="column_depth"),
            sg.Text('Color:'), sg.Input(size=(12, 1),default_text=default_column_color, key="column_color_column")],
            [sg.Text('_____________________________________________________________________________________')],
            [sg.Text('Please include group names, from the file naming convention, to determine spatial organization:')],            
            [sg.Text('Groups:'), sg.Input(size=(68, 1),default_text=default_groups, key="group_names")],
            [sg.Text('Subgroups:'), sg.Input(size=(65, 1),default_text=default_subgroups, key="subgroup_names")],
            [sg.Text('_____________________________________________________________________________________')],
            [sg.Text('Please choose the geometry style and color style for your model:')],             
            [sg.Text('Geometry Style:'),
            sg.Combo(size=(22, 1),default_value=self.default_export_style_dropdown, values = self.values_export_style,key="export_style_dropdown")],
            [sg.Text('Color Style:'),
            sg.Combo(size=(28, 1),default_value=self.default_color_style_dropdown, values = self.values_color_style,key="color_style_dropdown")],
            [sg.Text('')],
            [sg.Button("Addtional Settings")],
            [sg.Button("Publish FBX File and Close"),sg.Button("Exit")], #sg.Button("Settings")
            [sg.StatusBar("", size=(20, 1), key='-STATUS1-'),sg.Text(size=(8,1)),sg.Text('Pavlov Software & Services LLC')]
        ]
        # Create the window
        self.main_window = sg.Window("Pavlov 3D - Basic", layout, resizable=True,finalize=True,element_justification='l',auto_size_text=True)

        while True:
            event, self.values = self.main_window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            elif event == "Instructions":
                self.popup_instructions()
            elif event == '-DATA_DIRECTORY-':
                dirname = self.main_window['-DATA_DIRECTORY-'].Get()
                if os.path.isdir(dirname):
                    pervasive_dirname = dirname
  
            elif event=="Choose Multiple Colors":#"Select Color Style(s)":
                self.window_color_style_selection()

            elif event == "Addtional Settings":
                self.window_additional_settings()
                
            elif event == "Publish FBX File and Close": 
                self.publish_FBX_file()
                self.main_window.close()        

        self.main_window.close()
        return self.user_input_object

    def popup_instructions(self):
        sg.popup(f'This software tool is meant to provide Preceding Analysis Visualization.'\
        '\n\nFBX files published by Pavlov are best viewed using CAD Assistant by Open Cascade.'\
        '\n\nThis basic version of Pavlov 3D imports two, three, or four columns of data from all selected CSV/XLSX files in a directory.'\
        '\n\nControl which CSV files are selected by listing file name string patterns to include or exclude. Multiple patterns for inclusion and exclusion can be listed, separated by commas.'\
        '\n\nControl which columns of data are imported by inputting text strings found in the column label name. Alternatively, the column number can be used. Index 0 indicates the first column.'\
        '\n\nThe TIME axis represents the forward direction, and the HEIGHT axis represents the vertical direction.'\
        '\nIn this two-column version of Pavlov, the DEPTH of each data value is automatically assigned to be 50% of the HEIGHT value.'\
        '\n\nStyle selection determines how data is represented geometrically.'\
        '\n\nIf a color column is not provided, color will represent height data reduntantly.'
,
        title="Instructions")

    def publish_FBX_file(self):
        self.publish = True
        self.data_directory = self.values["-DATA_DIRECTORY-"]
        #self.filenames = self.get_file_list() # this is the whole un-culled list
        self.filenames = self.check_filelist()
        
        self.column_time = self.values["column_time"]
        self.column_height = self.values["column_height"]
        self.column_depth = self.values["column_depth"]
        self.color_column = self.values["column_color_column"]
        if self.column_depth.lower()=="default":
            self.column_depth = ''
        if self.color_column.lower()=="default":
            self.color_column = ''

        #self.stack_direction_groups = self.values["stack_direction_groups"]
        '''start'''
        """ default_text=default_data_start_idx, key="data_start_idx"
        default_value=default_stack_direction_groups,key="stack_direction_groups"
        default_stack_direction_subgroups,key="stack_direction_subgroups"
        default_stack_direction_curves,key="stack_direction_curves" """

        '''end'''
        try:
            self.stack_direction_groups = self.values["stack_direction_groups"]
            stack_direction_subgroups = self.values["stack_direction_subgroups"]
            self.stack_direction_curves = self.values["stack_direction_curves"]
            self.data_start_idx = self.values["data_start_idx"]
            selected_encoding = ""
            if self.values["-ASCII_RADIO-"]:
                self.selected_encoding = "ASCII" 
            elif self.values["-BIN_RADIO-"]:
                self.selected_encoding = "BIN"

        except Exception:
            print('simple gui window never opened, defaults assigned')
        self.stack_vector = str(self.stack_direction_groups+","+stack_direction_subgroups+","+self.stack_direction_curves)

        self.import_style_dropdown = self.values["import_style_dropdown"]
        #self.import_filetype_dropdown = default_import_filetype_dropdown
        self.export_style_dropdown = self.values["export_style_dropdown"]
        self.color_style_dropdown = self.values["color_style_dropdown"]

        group_names = self.values["group_names"]
        subgroup_names = self.values["subgroup_names"]
        group_names = group_names.split(',')
        subgroup_names = subgroup_names.split(',')
        for i,group in enumerate(group_names):
            group_names[i] = group_names[i].strip()
        for i,group in enumerate(subgroup_names):
            subgroup_names[i] = subgroup_names[i].strip()

        self.dict_groups_tiers = dict()
        self.dict_groups_tiers[1] = group_names
        self.dict_groups_tiers[2] = subgroup_names

        msg_export = f"Export Directory: {self.export_directory}, File Encoding: {self.selected_encoding}, File Size: {export_filesize} MB"
        self.main_window['-STATUS1-'].update(msg_export) 
        self.user_input_object.pull_data_from_gui_object()

    def return_gui_vars(self):
        return self.data_directory, self.filenames,self.column_time,self.column_height,self.dict_groups_tiers
