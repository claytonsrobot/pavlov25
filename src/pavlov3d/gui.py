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
    - Consider how to use multiple pages instead of one screen.
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
    Check. Make filtering not case sensitive. Check.

01 June 2024:
    What does user_input_object do inside of gui.py?
    What vars do we store in gui that we could store somewhere else? 
    ^Especially for default inputs, which could come from a config_input file (json 2024).
    removed: check_box=False # relic

22 January 2025:
    The GUI terminology should reference the terminology used in the CLI.
    What does this mean?
    Step 3 is step 3. The purpose of the GUI is to lock in user oversight on the config.
    So rather than having an "Export" button on the GUI, there should be a "Save configuration and return to CLI" button, which will print status and offer a hint to press 4.
    Which makes the configuration GUI separate from a hypothetical model preview GUI - perfect.
    Revisit the program flow. [Data selection and cleansing] is separate from [Style selection].
    There can also be a button for "Save configuration and then build the program".
    Project management, too.   


'''
import FreeSimpleGUI as sg
import pprint
import os
from pathlib import Path # for chopping off filename when searching directory
#import pandas as pd # for data management
#import plugins
from pavlov3d.parse_user_input_config import parse_user_input_config
import src.pavlov3d.filter_files as ff
from pavlov3d.directories import Directories

#pd.options.display.max_columns = None
#pd.options.display.max_rows = None
#pd.options.display.expand_frame_repr = False
# import queryTracker

standardTextSize=6 # doesn't do anything

#config_input_object = ConfigInput() 
#config_input_object.define_and_load_default_config_input()
#config_input_object.pull_values_from_json_config_input_object(config_input_object.loaded_config)
#config_input_object.import_json_values()


''' json config load default approach replaces '''

class Gui:
    style_object = None
    allowed_keys = set(['data_directory','filenames','column_time','height_column','dict_groups_tiers'])
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
        

    def __init__(self,optional_instance_name='gui'):
        self.optional_instance_name = optional_instance_name
        #self.user_input_object = UserInput()
        #self.user_input_object.assign_interface_object(self)
        
        self.__dict__.update((key, None) for key in self.allowed_keys)
        self.__dict__.update((key, None) for key in self.internal_keys)
        self.dict_groups_tiers = dict()
        self.selected_item = None

        self._set_known_styles()
        self.publish = False # stays false until the publish button is pushed. If exited and the publish button is never pushed, the program will exit in main.

        self.export_control_override = False
        self.export_control_window_object = None
        
    def _set_known_styles(self):

        self.import_style_dictionary = dict({"MultiSheet 2D":f'plugins.import_plugin_CSV_2D',
                                             "SingleSheet MultiColumn 2D":f'plugins.import_plugin_CSV_singleSheet_multiColumn',
                                             "MultiSheet 4D":f'plugins.import_plugin_CSV_4D'})
        """future work: "MultiSheet 7D":plugins.import_plugin_CSV_7D,
                                             "STL, Multiple": plugins.import_plugin_STL,
                                             "PNG, Multiple": plugins.import_plugin_PNG}) """
        #process_data_singleSheet_multiColumn

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
                                            "Binned Gradient per Assigned Vector":'plugins.color_plugin_binned_gradient',
                                            "True Gradient per Assigned Vector":'plugins.color_plugin_true_gradient'}) # have a method to test that each entry here is in the folder
                                            #"Color per Group, Shade per Subgroup":'plugins.color_plugin_shaded_groups'
                                            #"Color per Group, Shaded":'plugins.color_plugin_per_group_shaded.py'
                                            #"Color per Subgroup, Shaded":'plugins.color_plugin_per_subgroup_shaded.py'
        # these dictionaries should be pulled from color_plugins instead 
        
        self.dict_model_ID = dict({"Binned Gradient per Assigned Vector":'binned_gradient_color_model',
                                "Color per Datapoint Key":'barchart_keys_color_model',## this is actually good, it causes the known gui references and the unknown dynamic plugins to have a similar name, thus easier to add. settled.'
                                "Color per Object":'singular_color_model_per_curve',
                                "True Gradient per Assigned Vector":'true_gradient_color_model'})
        
        self.values_import_filetype = ['CSV / XLSX','STL']
        self.values_import_filetype_wishlist = ['CSV / XLSX','PNG / JPG (incomplete)','GPX (incomplete)','PKL (incomplete)','H5 (incomplete)','MAT (incomplete)','BREP (incomplete)','STL (incomplete)','DBF (incomplete)','GLB (incomplete)','FBX (incomplete)','IGES (incomplete)','OBJ (incomplete)','PLY (incomplete)','STEP (incomplete)','TXT (incomplete)','RDA / RDS (incomplete)'] # stl and brep are now out of order, but they are in the dropdown for stoke
        # use the assimp import packge(s)
        self.values_import_style = list(self.import_style_dictionary.keys())
        self.values_export_style = list(self.export_style_dictionary.keys())
        self.values_color_style = list(self.color_style_dictionary.keys())

        self.default_import_filetype_dropdown = self.values_import_filetype[0]
        self.default_import_style_dropdown = self.values_import_style[0]
        self.default_export_style_dropdown = self.values_export_style[1]#0
        self.default_color_style_dropdown = self.values_color_style[4]

    def get_filtered_list_gui(self):

        # this is here because of the file selection opportunity in the pysimple gui browser, but its ..... ugh probably not a good hill to die on

        if self.main_window['-SELECT_DIR-'].get() is True and self.main_window['-SELECT_FILES-'].get() is False:
            #dirname = self.main_window['data_directory'].Get()
            #file_list = ff.get_filtered_list(dirname)
            file_list = self._check_filelist(None)

        elif self.main_window['-SELECT_DIR-'].get() is False and self.main_window['-SELECT_FILES-'].get() is True:
            filenames = self.values['-HOLDBROWSE-']
            full_file_list = filenames.split(';')
            file_list = []
            for filename in full_file_list:
                path = Path(filename)
                filename = str(path.name)
                file_list.append(filename)
            foldername = str(path.parent)
            self.main_window['-FILELISTBOX-'].update(file_list)
            self.main_window['data_directory'].update(foldername)

        return file_list
 
    def _check_filelist(self,cij):

        dirname = self.main_window['data_directory'].Get()
        pattern_and = self.main_window['filter_files_include_and'].Get()
        pattern_or = self.main_window['filter_files_include_or'].Get()
        pattern_not = self.main_window['filter_files_exclude'].Get()
        if cij is not None:
            #original_case_list_filtered = ff.check_filelist(dirname,pattern_and,pattern_or,pattern_not,self.user_input_object)
            #original_case_list_filtered = ff.check_filelist(dirname,pattern_and,pattern_or,pattern_not,cij["filetype_list"])
            original_case_list_filtered = ff.check_filelist(dirname,pattern_and,pattern_or,pattern_not,self.user_input_object.filetype_allowed_list)
        #                                     def check_filelist(dirname,pattern_and,pattern_or,pattern_not,filetype_list):
        # use cij
        else:
            print("\nincomplete\n")
            original_case_list_filtered = ff.check_filelist(dirname,pattern_and,pattern_or,pattern_not,self.user_input_object.filetype_allowed_list)
            pass
        return original_case_list_filtered
    
    def dataPeek_window(self,df):# this doesn't work currently.  namely, it's not a window.
        '''
        Show the dataframe view window.
        ''' 
        layout = [
                  [sg.Multiline(size=(70,10),key='-MULTILINE-',expand_x=True, expand_y=True)],
                  [sg.B('Ok', bind_return_key=True), sg.B('Cancel')],
                  ]

        window_dataPeek = sg.Window('Data Peek', layout, resizable=True,finalize=True)
        window_dataPeek['-MULTILINE-'].print(df.head())
        #window_dataPeek['-MULTILINE-'].print(df.columns.tolist())
        #window_dataPeek['-MULTILINE-'].print(df.columns.values)
        #window_dataPeek['-MULTILINE-'].print(df.info()) 
        while True:
            event, self.values_data = window_dataPeek.read()
            if event in ('Cancel', sg.WIN_CLOSED):
                break
            if event == 'Ok':
                break
        window_dataPeek.close()

    def window_color_style_selection(self):
        layout = [
            [sg.Check(list(self.color_style_dictionary.keys())[0], key='-CHECK-COLOR_PER_KEY-')],
            [sg.Check(list(self.color_style_dictionary.keys())[1], key='-CHECK-COLOR_PER_GROUP-')],
            [sg.Check(list(self.color_style_dictionary.keys())[2], key='-CHECK-COLOR_PER_SUBGROUP-')],
            [sg.Check(list(self.color_style_dictionary.keys())[3], key='-CHECK-COLOR_PER_CURVE-')],
            [sg.Check(list(self.color_style_dictionary.keys())[4], key='-CHECK-COLOR_BINNED_GRADIENT-')],
            [sg.Check(list(self.color_style_dictionary.keys())[5], key='-CHECK-COLOR_TRUE_GRADIENT-')],
            [sg.Check('Unlisted Plugins', key='-CHECK-COLOR-PLUGINS-'),sg.Input(size=(60,1),default_text='',key='-COLOR-PLUGINS-INPUT-',enable_events = False)],
            [sg.Button('Submit', key='-SUBMIT-COLORS-')]
            ]
        color_style_window = sg.Window('Color Style', layout, size=(715, 300),resizable=True)
        while True:
            event, self.values_color = color_style_window.read()

            if event == sg.WIN_CLOSED or event == "Exit":
                break
            elif event=="-SUBMIT-COLORS-":
                #my_list = [1, 2, 3, 4, 5]
                #bool_list = [True, False, True, False, True]
                bool_list = [self.values['-CHECK-COLOR_PER_KEY-'],
                             self.values['-CHECK-COLOR_PER_GROUP-'],
                             self.values['-CHECK-COLOR_PER_SUBGROUP-'],
                             self.values['-CHECK-COLOR_PER_CURVE-'],
                             self.values['-CHECK-COLOR_BINNED_GRADIENT-'],
                             self.values['-CHECK-COLOR_TRUE_GRADIENT-'],
                             self.values['-CHECK-COLOR-PLUGINS-']
                             ]
                value_list = [list(self.color_style_dictionary.values())[0],
                              list(self.color_style_dictionary.values())[1],
                              list(self.color_style_dictionary.values())[2],
                              list(self.color_style_dictionary.values())[3],
                              list(self.color_style_dictionary.values())[4],
                              list(self.color_style_dictionary.values())[5],
                              str(self.values['-COLOR-PLUGINS-INPUT-'])
]
                color_plugin_list = [x for x, flag in zip(value_list, bool_list) if flag]
                #for all checked boxes, and from input box, append plugin values into a list and set as value for self.main_window["color_style_plugin"]
                chosen_color_plugins = ';'.join(str(x) for x in color_plugin_list)
                self.main_window["color_style_plugin"].update(chosen_color_plugins)# update text to be list of plugins
                color_style_window.close()
        color_style_window.close()
        
    def window_user_input_config_selection(self,cij):
        #config_path = self.config_input_object.config_directory + cij.config_input_file
        print(f"cij.keys = ")
        pprint.pprint(cij.keys)
        config_path =cij['config_input_path'] # assessed in the user_input_ tool # hacky bullshit, get it another way.
        #config_path = script_dir + self.config_entry_object.config_directory_relative + self.config_entry_object.config_file
        layout = [
            [sg.Text('Filepath:'), sg.Input(size=(60, 1),default_text=config_path, enable_events = True,key="-CONFIG-FILE-"), sg.T(size=(standardTextSize,1)),sg.FilesBrowse('Browse', target='-CONFIG-FILE-',visible=True)],
            [sg.Button('Peek', key='-PEEK-CONFIG-'),sg.Button('Use Selected Config and Exit', key='-SUBMIT-CONFIG-'),sg.Button('Cancel', key='-CANCEL-CONFIG-')]
            ]
        config_window = sg.Window('Color Style', layout, size=(715, 200),resizable=True)
        self.config_window = config_window
        config_object = parse_user_input_config()
        while True:
            event, self.config_values = config_window.read()
            if event == sg.WIN_CLOSED or event == "Exit" or event=="-CANCEL-CONFIG-":
                break
            elif event=="-SUBMIT-CONFIG-":
                filename = os.path.normpath(config_window["-CONFIG-FILE-"].Get())
                #print(filename)
                if os.path.isfile(filename):
                    config_object.load_json_to_gui(filename = filename,gui_object = self)
                    self.refresh_filelistbox() # doink the filters
                else:
                    print(f'Input config file not found: {filename}')
                config_window.close()
            elif event == "-PEEK-CONFIG-":
                filename = os.path.normpath(config_window["-CONFIG-FILE-"].Get())
                if os.path.isfile(filename):
                    config_object.preview(filename = filename)
                else:
                    print(f'Input config file not found: {filename}')
        config_window.close()
        return config_window["-CONFIG-FILE-"].Get()
    
    def window_user_input_config_save(self):

        layout = [
            [sg.Text('Config Name:'), sg.Input(size=(40, 1),default_text='', enable_events = True,key="-SAVE-CONFIG-FILENAME-"),sg.Text('(please use no spaces or file extension)')],
            [sg.Text('If you use a name that is already used, it will overwrite the existing file.')],
            [sg.Button('Save Current Interface Values to Default Config Directory and Exit', key='-SAVE-CONFIG-'),sg.Button('Cancel', key='-CANCEL-SAVE-CONFIG-')]
            ]
        self.save_config_window = sg.Window('Save Configuration', layout, size=(715, 200),resizable=True)
        print(self.save_config_window)
        
        while True:
            event, self.save_config_values = self.save_config_window.read()
            if event == sg.WIN_CLOSED or event == "Exit" or event=="-CANCEL-SAVE-CONFIG-":
                break
            elif event == '-SAVE-CONFIG-':
                # Save configuration file to default config location
                filename = self.save_config_window["-SAVE-CONFIG-FILENAME-"].Get()+'.json'
                filepath = self.config_input_object.config_directory+'\\'+filename
                filepath = os.path.normpath(filepath)
                config_object = parse_user_input_config()
                config_object.save_gui_values_as_file(filepath,gui_object = self)
                self.save_config_window.close()

        #self.save_config_window = save_config_window
        self.save_config_window.close()
        return self.save_config_window["-SAVE-CONFIG-FILENAME-"].Get()

    
    def window_text_style(self):
        
        layout = [
            [sg.Text('Title Angle:'), sg.Input(size=(20, 1),default_text='[0,0,0]', enable_events = True,key="-TITLE-ANGLE-THD-")],
            [sg.Text('Time Axis Angle:'), sg.Input(size=(20, 1),default_text='[0,0,0]', enable_events = True,key="-TIMEAXIS-ANGLE-THD-")],
            [sg.Text('Height Axis Angle:'), sg.Input(size=(20, 1),default_text='[0,0,0]', enable_events = True,key="-HEIGHTAXIS-ANGLE-THD-")],
            [sg.Text('Depth Axis Angle:'), sg.Input(size=(20, 1),default_text='[0,0,0]', enable_events = True,key="-DEPTHAXIS-ANGLE-THD-")],
            [sg.Text('Unit: Degrees.')],
            [sg.Text('In brackets, comma separated, 3 values.')],
            [sg.Text('Example: [1,0,0]')],
            [sg.Button('Preview', key='-PREVIEW-TEXT-STYLE-'),sg.Button('Apply and Exit', key='-SUBMIT-TEXT-STYLE-'),sg.Button('Cancel', key='-CANCEL-TEXT-STYLE-')]
            ]
        text_window = sg.Window('Addtional Model Settings: Text Style', layout, size=(370, 250),resizable=True)

        while True:
            event, self.values_text = text_window.read()

            if event == sg.WIN_CLOSED or event == "Exit" or event=="-CANCEL-TEXT-STYLE-":
                break
            elif event=="-SUBMIT-TEXT-STYLE-":
                # set values,to come
                do_stuff_more=1
                text_window.close

                text_window.close()
            elif event == "-PEEK-TEXT-STYLE-":
                # i need a 3D plot. These junts need to be three separate fields with arrows to drive the value
                pyplot
                dothislater

        text_window.close()
        return
    
    def window_preview_pyplot(self):
        print('Pyplot Preview To Be Constructed')
        import preview_text_3D
        preview_text_3D.show()

    def run_and_get_inputs(self):

        cij=self.config_input_object.loaded_config

        # this is incomplete - i need to complete my intermediate schema transfer, that will normalize between group-by- hierarchies
        cig=self.config_input_object.loaded_grouping
        #cig=self.config_input_object.loaded_grouping["grouping"]
        print(f"cij = {cij}")
        self.load_file_encoding(cij)
        # Define the layout of the main window
        #print("before layout: default_data_directory = ",default_data_directory)
        values_stack_directions = ["diagonal_stack","time_stack","depth_stack"]
        #sg.theme('DarkTeal9')
        sg.theme('DarkBlue13') 
        layout = [
            [sg.Text('Thank you for using Pavlov!'),sg.Button("Instructions"),sg.Button("Package Dependencies"),
             sg.Button("Load Inputs from Config File"),sg.Button("Save Current Values as Config File")],
            [sg.Text('File Type'),sg.Combo(size=(24, 1),default_value=self.default_import_filetype_dropdown, values = self.values_import_filetype,key="import_filetype_dropdown"),sg.T(size=(standardTextSize,1)),
             sg.Text('Import Style:'),
            sg.Combo(size=(24, 1),default_value=self.default_import_style_dropdown, values = self.values_import_style,key="import_style_dropdown"),sg.T(size=(standardTextSize,1)),
            sg.Text('Import Plugin Override:'), sg.Input(size=(40, 1),default_text=cij['import_style_plugin'], key="import_style_plugin"),sg.T(size=(standardTextSize,1))],
            [sg.Text('Data Directory:'), sg.Input(size=(60, 1),default_text=Directories.get_import_dir(), enable_events = True,key="data_directory"), sg.T(size=(standardTextSize,1)),
            sg.Radio('Select Directory',group_id='folderBrowseBehavior',default=True,key='-SELECT_DIR-'),
            sg.Radio('Select Files',group_id='folderBrowseBehavior',key='-SELECT_FILES-'),
            sg.FilesBrowse('Browse', target='-HOLDBROWSE-',visible=True),
            sg.Input('Hold FilesBrowse Selection - Hidden',visible=False,key='-HOLDBROWSE-',enable_events=True)],# invisible
            [sg.Text('Filter Files, Include (AND):'), sg.Input(size=(55, 1),default_text=cij['filter_files_include_and'], enable_events = True, key = 'filter_files_include_and')],
            [sg.Text('Filter Files, Include (OR):'), sg.Input(size=(55, 1),default_text=cij['filter_files_include_or'], enable_events = True, key = 'filter_files_include_or')],
            [sg.Text('Filter Files, Exclude:'), sg.Input(size=(55, 1),default_text=cij['filter_files_exclude'], enable_events = True, key = 'filter_files_exclude')],

            [sg.Text('Files:'),
                sg.T(size=(51,1)),
                sg.T(size=(standardTextSize,1),text_color = 'White', k='-FILTERINCLUDE NUMBER-')],
            [sg.Listbox(values="Starting up...", select_mode=sg.SELECT_MODE_SINGLE, size=(73, 8), enable_events = True, key='-FILELISTBOX-')],
            [sg.Button("Peek at Selected File"),sg.Button("Remove Selected File"),sg.Button("Reset")],
            [sg.Text('Time Column ID:'), sg.Input(size=(26, 1),default_text=cij['column_time'], key="column_time"),sg.T(size=(standardTextSize,1)),
            sg.Text('Depth Column ID:'), sg.Input(size=(25, 1),default_text=cij['column_depth'], key="depth_column"),sg.T(size=(standardTextSize,1))],
            [sg.Text('Height Column ID:'), sg.Input(size=(25, 1),default_text=cij['column_height'], key="height_column"),sg.T(size=(standardTextSize,1)),
            sg.Text('Color Column ID**:'), sg.Input(size=(25, 1),default_text=cij['column_color'], key="color_column"),sg.T(size=(standardTextSize,1)),sg.Text('**Default: Use Height Column')],
            [sg.Text('Metadata Column IDs (strings):'), sg.Input(size=(30, 2),default_text=cij['columns_metadata'], key="metadata_columns"),sg.T(size=(standardTextSize,1)),
            sg.Text('Data Start (column # or row #):'), sg.Input(size=(6, 2),default_text=cij['data_start_idx'], key="data_start_idx"),sg.T(size=(standardTextSize,1))],
            
            [sg.Text('Groups:'), sg.Input(size=(68, 1),default_text=cig['group_names'], key="group_names"),sg.T(size=(standardTextSize,1))],
            [sg.Text('Subgroups:'), sg.Input(size=(65, 1),default_text=cig['subgroup_names'], key="subgroup_names"),
                sg.T(size=(standardTextSize,1))],   

            [sg.Text('Scene Contents Stack Direction:'), sg.Text('Group Contents Stack Direction:'), sg.Text('Subgroup Contents Stack Direction:')],
            [sg.Combo(size=(18, 1),default_value=cij['stack_direction_groups'], values = values_stack_directions,key="stack_direction_groups"),sg.T(size=(standardTextSize,1)),
             sg.Combo(size=(18, 1),default_value=cij['stack_direction_subgroups'], values = values_stack_directions,key="stack_direction_subgroups"),sg.T(size=(standardTextSize,1)),
             sg.Combo(size=(18, 1),default_value=cij['stack_direction_curves'], values = values_stack_directions,key="stack_direction_curves"),sg.T(size=(standardTextSize,1))],
            [sg.Text('Export Directory:'), sg.Input(size=(60, 1),default_text=self.config_input_object.export_directory, key="export_directory"),  
                sg.T(size=(standardTextSize,1))],
            [sg.Text('Export Style:'),
            sg.Combo(size=(22, 1),default_value=self.default_export_style_dropdown, values = self.values_export_style,key="export_style_dropdown"),sg.T(size=(standardTextSize,1)),
            sg.Text('Export Plugin Override:'), sg.Input(size=(40, 1),default_text=cij['export_style_plugin'], key="export_style_plugin"),sg.T(size=(standardTextSize,1))],

            [sg.Text('Color Style:'),
            sg.Combo(size=(36, 1),default_value=self.default_color_style_dropdown, values = self.values_color_style,key="color_style_dropdown"),sg.T(size=(standardTextSize,1)),
            sg.Button("Choose Multiple Colors"),
            sg.Text('Color Plugin Override:'), sg.Input(size=(28, 1),default_text=cij['color_style_plugin'], key="color_style_plugin"),sg.T(size=(standardTextSize,1))],
            [sg.Button("Addtional Export Model Settings"), sg.Button("Preview Export Model")],
            [sg.Text('FBX File Encoding:'),sg.Radio("ASCII",group_id="encoding", key="-ASCII_RADIO-", default = self.encoding["-ASCII_RADIO-"]),sg.Radio("BIN (default)",group_id="encoding", default=self.encoding["-BIN_RADIO-"], key="-BIN_RADIO-")],
            [sg.Button("Show Overview Graph"),sg.Button("Publish FBX File and Close"),sg.Button("Exit")], #sg.Button("Settings")
            [sg.StatusBar("", size=(20, 1), key='-STATUS1-'),sg.Text(size=(8,1)),sg.Text('Pavlov Software & Services LLC')]
        ]

        # Create the window
        #background_color_hex = '#DAE0E6'
        self.main_window = sg.Window("Pavlov 3D - Developer Mode", layout, resizable=True,finalize=True,element_justification='l',auto_size_text=True)#,
                                     #background_color=background_color_hex)#'c'
        _fresh_list = self._check_filelist(cij)
        
        self.main_window['-FILELISTBOX-'].update(_fresh_list) # uniqueCodeReference_powerLip2go
        self.main_window['-FILTERINCLUDE NUMBER-'].update(f'{len(_fresh_list)} files')
        file_list = self.get_filtered_list_gui() # suppressing this does in fact break things
        
        # this is only good when you click the option to browse by file
        #file_list = _check
        self.selected_item = file_list[0]
        #self.selected_item = _fresh_list[0]

        while True:
            event, self.values = self.main_window.read()
            #gui_object.values
            if event == sg.WIN_CLOSED or event == "Exit":
                break
                
            elif event == "Instructions":
                sg.popup(f'This software tool is meant to provide Preceding Analysis Visualization.'\
                        '\n\nFBX files published by Pavlov are best viewed using CAD Assistant by Open Cascade.'\
                        '\n\nThis version of Pavlov 3D imports two columns of data from all selected CSV files in a directory.'\
                        '\n\nControl which CSV files are selected by listing file name string patterns to include or exclude. Multiple patterns for inclusion and exclusion can be listed, separated by commas.'\
                        '\n\nControl which columns of data are imported by inputting text strings found in the column label name. Alternatively, the column number can be used. Index 0 indicates the first column.'\
                        '\n\nThe TIME axis represents the forward direction, and the HEIGHT axis represents the vertical direction.'\
                        '\nIn this two-column version of Pavlov, the DEPTH of each data value is automatically assigned to be 20% of the HEIGHT value.'\
                        '\n\nStyle selection determines how many polygons are used to represent each data point.'\
                        '\nIf there are dozens of raw data files, each containing thousands of datapoints, it is ideal to have the lightest possible representation of data.'\
                        '\n    Minimalist style: 1 triangle per data point. Default.'\
                        '\n    Pyramid style: 3 triangles.'\
                        '\n    Bar style: 10 triangles.'\
                        '\n    Cube style: 10 triangles.'\
                        '\n    Icosahedron style: 20 triangles.'\
                        # Aesthetically pleasing but not advised.'\
                        '\n\nFBX files with ASCII encoding are legible plaintext and are slightly smaller in file size compared to BIN encoding.'\
                        '\nFBX files with BIN encoding are encrypted, allow for embedded media, allow for conversion to GLB file type, and are slightly larger in file size compared to ASCII encoding.',
                        title="Instructions")
                        # The roof of the each pyramid is missing.
                        # The floor of the each cube is missing.
                        # The floor of the each bar is missing.
                        # Incorporate a Minimalist - Floating style, represent each data point with 1 triangle.'

            elif event == "Package Dependencies":
                sg.popup(f'Please install the following Python packages for Pavlov to function properly:'\
                        '\n\npip install pysimplegui'\
                        '\npip install numpy'\
                        '\npip install pandas'\
                        '\npip install matplotlib'\
                        '\n\nInstall the Autodesk FBX Python SDK: \nhttps://www.autodesk.com/developer-network/platform-technologies/'\
                        '\n'\
                        '\nInstall Open Cascade CAD Assistant: \nhttps://www.opencascade.com/products/cad-assistant/'\
                        '\n'\
                        '\nIn the future, a PAVlov web app will be launched, and no local installations will be required.',    
                        title="Package Dependencies")
                
            elif event =="Load Inputs from Config File":
                self.window_user_input_config_selection(cij)

            elif event =="Save Current Values as Config File":
                self.window_user_input_config_save()
                
            elif event == 'data_directory':
                dirname = self.main_window['data_directory'].Get()
                if os.path.isdir(dirname):
                    pervasive_dirname = Path(dirname)
                    _fresh_list = self._check_filelist(cij)
                    self.main_window['-FILELISTBOX-'].update(_fresh_list) # uniqueCodeReference_wunderFins

            elif event == '-HOLDBROWSE-':
                if self.values['-SELECT_DIR-'] is True and self.values['-SELECT_FILES-'] is False:
                    filenames = self.values['-HOLDBROWSE-']
                    filename = filenames.split(';', 1)[0]
                    path = Path(filename)
                    foldername = str(path.parent)
                    self.main_window['data_directory'].update(foldername)
                elif self.values['-SELECT_DIR-'] is False and self.values['-SELECT_FILES-'] is True:
                    filenames = self.values['-HOLDBROWSE-']
                    full_file_list = filenames.split(';')
                    file_list = []
                    for filename in full_file_list:
                        path = Path(filename)
                        filename = str(path.name)
                        file_list.append(filename)
                    foldername = str(path.parent)
                    self.main_window['-FILELISTBOX-'].update(file_list)
                    self.main_window['data_directory'].update(foldername)
                    # currently non-functional - will break when you touch the filters
                self.check_and_update_file_count()
                    
            elif event == 'filter_files_include_and':
                self.refresh_filelistbox()

            elif event == 'filter_files_include_or':
                self.refresh_filelistbox()

            elif event == 'filter_files_exclude':
                self.refresh_filelistbox()
                
            elif event == '-FILELISTBOX-':# uniqueCodeReference_funnelMug4me
                selection = self.values[event]
                if selection:
                    self.selected_item = selection[0]
                    #self.main_window['-STATUS-'].update(f"{item} selected")     
                    
            elif event == "Peek at Selected File":
                self.filenames = self.main_window['-FILELISTBOX-'].Values # uniqueCodeReference_peak2Tweak
                print("peek: ",self.selected_item)
                try: #if isinstance(pervasive_dirname, str): #I would prefer to not use try, but here we are
                    target = pervasive_dirname / self.selected_item
                    print(f'try:pervasive_dirname')
                except: #else:
                    target = Directories.get_import_dir() / self.selected_item
                    print(f'except:default_data_directory   ')
                if os.path.isfile(target):
                    try:
                        df = pd.read_csv(target)
                    except Exception:
                        #df = pd.read_excel(target)
                        df = pd.read_excel(Directories.get_import_dir() / filename,skiprows=self.user_input_object.skiprows)
                        # not functioning
                    print('\n\n',self.selected_item)
                    print('\n',df.info())
                    print(df.head())
                #dataPeek_window(df)
                '''
                if dataPeek_window() is True:
                        window_dataPeek.close()
                        window = make_window()
                        '''

                #sg.popup(f"Place Holder. \n{selected_item} \nShow First Five Rows of the Highlighted File. \nAllow for side scrolling, to explore all column header names. \nShow column index numbers?",
                #         title="Data Peek")
            elif event == "Remove Selected File":
                self.remove_selected_file_from_filelistbox()
                           
            elif event == "Reset":
                self.reset_filelistbox()

            elif event == "Show Overview Graph":
                sg.popup(f"Placeholder \nYour PNG Here DAVE DAVE DAVE DAVE",title = "Overview Graph")
                
                # Import data if it hasn't been imported yet, or if current file list doesn't match previous list recorded during import
                '''psuedocode:
                matplotlib(title=filecount)
                time_label = files[0],row[match(Time)]
                height_label = files[0],row[match(Height)]
                #groupings, for line color determination, and legend (don't show individual curve names, just the group and subgroup names)
                # check pysimplegui embedded matplotlib examples
                for file_i in files:
                    time_vector = file_i,timeColumn
                    height_vector = heightColumn
                    matplotlib, add curve (time_vector,height vector)
                '''
                # will need to import in order to show a preview
                # should this import differ from the import plug in? Probably not

            elif event=="Choose Multiple Colors":#"Select Color Style(s)":
                self.window_color_style_selection()

            elif event == "Addtional Export Model Settings":
                self.window_text_style()

            elif event == "Preview Export Model":
                self.window_preview_pyplot()
                
            elif event == "Publish FBX File and Close": 
                self.publish_FBX_file()
                self.main_window.close()        
        self.main_window.close()


        return self.user_input_object
    
    def load_file_encoding(self, cij):
        self.encoding = dict()
        self.encoding["-ASCII_RADIO-"] = False # default
        self.encoding["-BIN_RADIO-"] = True
        if cij['file_encoding']=='bin':
            self.encoding["-ASCII_RADIO-"] = False
            self.encoding["-BIN_RADIO-"] = True
        elif cij['file_encoding']=='ascii':
            self.encoding["-ASCII_RADIO-"] = True
            self.encoding["-BIN_RADIO-"] = False
        else:#default. why? 50% larger filesize, but, convertible to glb, which allows a 50% reduction in filesize
            self.encoding["-ASCII_RADIO-"] = False
            self.encoding["-BIN_RADIO-"] = True



    def refresh_filelistbox(self):
        _fresh_list = self._check_filelist(None) # doink the filter
        self.main_window['-FILELISTBOX-'].update(_fresh_list)  
        self.check_and_update_file_count()

    def remove_selected_file_from_filelistbox(self):
        file_list = self.main_window['-FILELISTBOX-'].Values # uniqueCodeReference_peak2Tweak
        file_list.remove(self.selected_item)
        self.main_window['-FILELISTBOX-'].update(file_list)
        self.check_and_update_file_count()
        
    def reset_filelistbox(self):
        # WHen the reset button
        if self.values['-SELECT_DIR-'] is True and self.values['-SELECT_FILES-'] is False:
            self.refresh_filelistbox()
            # incomplete
        elif self.values['-SELECT_DIR-'] is False and self.values['-SELECT_FILES-'] is True:
            filenames = self.values['-HOLDBROWSE-']
            full_file_list = filenames.split(';')
            file_list = []
            for filename in full_file_list:
                path = Path(filename)
                filename = str(path.name)
                file_list.append(filename)
            foldername = str(path.parent)
            self.main_window['-FILELISTBOX-'].update(file_list)
            self.main_window['data_directory'].update(foldername)

    def check_and_update_file_count(self):
        file_list_len = len(self.main_window['-FILELISTBOX-'].get_list_values())
        self.main_window['-FILTERINCLUDE NUMBER-'].update(f'{file_list_len} files')

    def publish_FBX_file(self):

        '''DESTROY conversion, do that junt in user_input, right?'''
        print(f'\nPUBLISH\n')
        self.publish = True
        self.data_directory = self.values["data_directory"]
        self.export_directory = self.values["export_directory"]
        # update filelist, limit to whats in the window

        #file_list = get_filtered_list() # this is the whole un-culled list
        self.filenames = self.main_window['-FILELISTBOX-'].Values # uniqueCodeReference_thunder3Dome # these values still have the csv extension

        self.column_time = self.values["column_time"]
        self.height_column = self.values["height_column"]
        
        self.depth_column = self.values["depth_column"]
        self.color_column = self.values["color_column"]
        self.metadata_columns = self.values["metadata_columns"]
        self.data_start_idx = self.values["data_start_idx"]

        self.stack_direction_groups = self.values["stack_direction_groups"]
        stack_direction_subgroups = self.values["stack_direction_subgroups"]
        self.stack_direction_curves = self.values["stack_direction_curves"]
        self.stack_vector = str(self.stack_direction_groups+","+stack_direction_subgroups+","+self.stack_direction_curves)
        # note recommended bro, wth is this
        #self.stack_vector = self.values["stack_direction"]

        self.import_style_dropdown = self.values["import_style_dropdown"]
        self.export_style_dropdown = self.values["export_style_dropdown"]
        self.color_style_dropdown = self.values["color_style_dropdown"]
        self.import_style_plugin = self.values["import_style_plugin"]
        self.export_style_plugin = self.values["export_style_plugin"]
        self.color_style_plugin = self.values["color_style_plugin"]

        group_names = self.values["group_names"]
        subgroup_names = self.values["subgroup_names"]
        group_names = group_names.split(',')
        subgroup_names = subgroup_names.split(',')
        for i,group in enumerate(group_names):
            group_names[i] = group_names[i].strip()
        for i,group in enumerate(subgroup_names):
            subgroup_names[i] = subgroup_names[i].strip()

        self.dict_groups_tiers = dict()
        self.dict_groups_tiers[2] = subgroup_names
        self.dict_groups_tiers[1] = group_names
        # why
        # all groups need to be declared manually in a list
        # in the case of kates data, i can declare the group to be the site location. compare to how this was done for gratzer single page data

        # down stream of load_file_encoding
        if self.values["-ASCII_RADIO-"]:#default, in case of True True
            self.file_encoding = "ASCII" 
            self.values["file_encoding"] = 'ascii'
        elif self.values["-BIN_RADIO-"]:
            self.file_encoding = "BIN"
            self.values["file_encoding"] = 'bin'
        export_filesize=10.4 # make this a dynamic read
        msg_export = f"Export Directory: {self.export_directory}, File Encoding: {self.file_encoding}, File Size: {export_filesize} MB"
        self.main_window['-STATUS1-'].update(msg_export) 
        self.user_input_object.pull_data_from_gui_object()

        #return data_directory, files,column_time,height_column,group_names,subgroup_names,groups_tier3
    def return_gui_vars(self):
        return self.data_directory, self.filenames,self.column_time,self.height_column,self.dict_groups_tiers
