'''
Title: user_input.py
Author: Clayton Bennett
Created: 25 November 2023

Purpose: Hold and pass variables from GUI input to the processing script.
Color plugin may or may not be a list. If it is from the dropdown, it will not be a list and it should not be made into a list.
If color plugin is from the text field (as "gui_object.color_style_plugin"), it should be made into a list
Or maybe all plugins shuld be made into lists, regardless of source,so that all of the processing can be the same.
'''
import os
import sys
#import re
#from pprint import pprint

from src import filter_files as ff
from src import environment
import src.grouping_by_string
import src.grouping_by_directory
import src.config_input
from src.directories import Directories

class UserInput:
    gui_object = None
    style_object = None
    plugin_class_dict = dict()
    plugin_class_dict.fromkeys(list(["color","import", "export"]))
    
    @classmethod # called inside of gui.py after user_input_object is instanced
    def assign_interface_object(cls,interface_object):
        cls.interface_object = interface_object
        print(f'assign_interface_object')
    
    @classmethod
    def assign_style_object(cls,style_object):
        cls.style_object = style_object
        cls.scene_object = style_object.scene_object

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py')
        self.instance_name = 'user_input_object'
        self.filenames = None

        dict_groups_tiers = None
        self.stack_vector_array = None # numeric vectors
        self.stack_direction_list = None # text

        self.import_style_plugin = None
        self.export_style_plugin = None
        self.color_style_plugin = None
        self.import_style_dropdown = None
        self.export_style_dropdown = None
        self.color_style_dropdown = None
        self.import_function= None
        self.export_function= None
        self.export_function_list = None
        self.color_function = None
        self.export_control_object = None
        self.metadata_columns = None
        #self.tiers = None
        self.skiprows = None

        self.plugin_fields = [self.import_style_plugin,self.export_style_plugin,self.color_style_plugin]
        self.dropdown_fields = [self.import_style_dropdown,self.export_style_dropdown,self.color_style_dropdown]
        self.style_function_fields = [self.import_function,self.export_function,self.color_function]

        self.pngShow = False 
        self.pngExport = False 

        self.axis_rotation_degrees_THD_CCW_time = None
        self.axis_rotation_degrees_THD_CCW_height = None
        self.axis_rotation_degrees_THD_CCW_depth = None

        self.filter_files_include_and = None
        self.filter_files_include_or = None
        self.filter_files_exclude = None

    def __str__(self):
        return "%s"% (self.name)
    
    def set_default_text_style(self):
        # Fine for default, but get aall of this out into the expoort plugins - value can then be called per curve_object or group_object
        # the setting of this needs to be igrated to the GUI, in a new window triggered by a button
        # the defaults found when the window is open should be based on the export style selected.
        self.titleRotation_style = 'TemperatureStyle'# 'Top,corner-to-corner' # wrong!
        self.axisRotation_style = 'TemperatureStyle' # 'Top,Front', 'Bottom,Front', manual # wrong!
        self.title_rotation_degrees_THD_CCW = [90,0,0]
        ##self.titleRotation = 0# 'Top,corner-to-corner' # wrong!
        ##  self.axisRotation = 0 # 'Top,Front', 'Bottom,Front', manual # wrong!
        self.scene_description_text = 'ABCDEFG HIJKLMNOP QRSTUV WXYZ 0123456789 !@#$%^&*() [] +-_,.<>:;' 
        # each export style should have typical text orination scheme - we can use a dataframe for this, with expected values for each choice

    def pull_config_input_object(self,config_input_object):
        print("user_input.pull_config_input_object()")
        self.grouping_algorithm = config_input_object.grouping_algorithm # necessary for hierarchy_object._assign_group_membership_for_complete_hierarchy()
        # it would be better to say use dictA.update(dictB)
        
        # make dictionary instead of mapping!
        # this needs to change 30 Dec 2024

        # edit this after the fact, instead of requiring skip_interface?

        # need to filter without the gui :)
        cij = config_input_object.loaded_config # self.dict_config_input = loaded_json # like this, make dictionary! instead of individual mapping, below:
        
        self.cij = cij # or use cij
        self.dict_config = dict()
        self.dict_config.update(cij)
        #self.group_names = cij["group_names"]
        #self.subgroup_names = gj["subgroup_names"]
        
        #if config_input_object.grouping_selection_path is not None:
        if config_input_object.grouping_algorithm != "group-by-directory":
            #gj = config_input_object.loaded_grouping["grouping"] # this is weirdly influencetial?
            gj = config_input_object.loaded_grouping
            self.group_names = gj["group_names"]
            self.subgroup_names = gj["subgroup_names"]
        else:
            pass
            #self.group_names = config_input_object.group_names 
            #self.subgroup_names = config_input_object.subgroup_names



        self.stack_direction_groups = cij["stack_direction_groups"]
        self.stack_direction_subgroups = cij["stack_direction_subgroups"]
        self.stack_direction_curves = cij["stack_direction_curves"]
        self.time_series_transcoding = cij["time-series-transcoding"] # expect: null, false, excel-datetime, unix-datetime, seconds,minutes,hours,days,years,gigasecond,Planck-time
        self.keep_true_destroy_false_unassigned_curves = cij["keep-true-destroy-false-unassigned-curves"]
        ##self.filetype_allowed = ["gpx"] # hack  # fix this, associate the filetype with the import module

        try:
            self.filter_files_include_and = cij['filter_files_include_and'] # for gui
            self.filter_files_include_or = cij['filter_files_include_or'] # for gui
            self.filter_files_exclude = cij['filter_files_exclude'] # for gui
        except:
            pass
        
        self.stack_direction_list = [self.stack_direction_groups,self.stack_direction_subgroups,self.stack_direction_curves]
        self.column_time = cij["column_time"]
        self.column_height = cij["column_height"]
        self.column_depth = cij["column_depth"]
        self.column_color = cij["column_color"]
        self.columns_metadata = cij["columns_metadata"]
        self.data_start_idx = cij["data_start_idx"]
        self.import_style_plugin = cij["import_style_plugin"].split(';') # dumb, convert to list
        self.export_style_plugin = cij["export_style_plugin"].split(';')
        self.color_style_plugin = cij["color_style_plugin"].split(';')
        self.file_encoding = cij["file_encoding"]

        if self.scene_object.request != None:
            self.filenames = ff.snip_filenames_from_request_session(self.scene_object.request.session["list_csv_uploads"])
            self.filepaths = self.scene_object.request.session["list_csv_uploads"]
        elif config_input_object.grouping_algorithm != "group-by-directory":
            "group-by-text, group-by-spreadsheet, group-by-json"
            self.filetype_allowed_list = self.extract_filetypes_allowed_list_from_import_plugin() # rather than the cij, which is already known
            self.filenames = ff.get_filelist_filetyped(self.filetype_allowed_list,Directories.get_import_dir()) # this is non-modular for the group-by-directory algorithm, becase it assumes all raw data files are in the same directory # get away from that assumption
            
            # Assume all file are in the same directory
            self.filepaths = [Directories.get_import_dir() + x for x in self.filenames]
            # we should be starting with filepaths then trimming to filenames.
            # all processes should use the whole filepath where possible, to modularize for either group-by-text and group-by-directory
        elif config_input_object.grouping_algorithm == "group-by-directory":

            if False:
                # explore first and second level directories in the projects/{project_name}/"imports" folder
                # migrate this to user_input_config 
                # old, works: self.group_names, self.subgroup_names, file_paths, file_names = src.grouping_by_directory.get_group_names_and_subgroup_names_and_file_names_from_import_directory_hierarchy(directory = Directories.get_import_dir())
                #keep: self.group_names, self.subgroup_names, file_paths, file_names = src.grouping_by_directory.get_group_names_and_subgroup_names_and_file_names_from_group_by_directory_intermediate_export_json_file()
                #toss: self.group_names, self.subgroup_names, file_paths, file_names = src.config_input.get_group_names_and_subgroup_names_and_file_names_from_group_by_directory_cij_loaded_grouping()
                self.group_names, self.subgroup_names, file_paths, file_names = src.config_input.get_three_tier_group_names_and_subgroup_names_and_file_names_from_group_by_directory_cij_loaded_grouping(data = config_input_object.loaded_grouping)
                # for now don't check filetypes, assume all are good
                #self.filepaths,self.filenames = foo(config_input_object.loaded_grouping) 
                self.filenames = file_names
                self.filepaths = file_paths
                print(f"self.group_names = {self.group_names}")
                print(f"self.subgroup_names = {self.subgroup_names}")
            else:
                pass

        #print(f"self.filepaths = {self.filepaths}")
        if False:
            print(f"self.filenames = {self.filenames}")

        if config_input_object.grouping_algorithm == "group-by-text":
        # this is a misnomer, because all algorithms can be fed this way. It will generate empties, and then destroy them. Non-ideal, but. 
            self.dict_groups_tiers = src.grouping_by_string.define_groups(self.group_names,self.subgroup_names)
        elif config_input_object.grouping_algorithm == "group-by-directory":
            root_group = self.dict_groups_tiers = src.grouping_by_directory.define_groups(loaded_grouping = config_input_object.loaded_grouping)
            print(f"root_group = {root_group}")
        else:
            sys.exit()

            # hosanna, no. refactor.

    def extract_filetypes_allowed_list_from_import_plugin(self):
        #import_function = self._check_import_plugin()
        plugin = self.import_style_plugin[0]
        plugin = "plugins."+plugin
        PluginClass = self.style_object.assign_plugin_dynamically(plugin)
        import_function_object = PluginClass()
        #import_function_object = self.style_object.prepare_import_module()
        #print(f"import_function_object.__dict__ = {import_function_object.__dict__}")
        self.import_filetype_list = import_function_object.filetype_allowed_list 
        return self.import_filetype_list

    def pull_values_from_export_control_object(self,export_control_object):

        # you should be employing dictionaries for this kind of thing
        self.set_export_control_object(export_control_object)
        self.axis_rotation_degrees_THD_CCW_time = self.export_control_object.axis_rotation_degrees_THD_CCW_time
        self.axis_rotation_degrees_THD_CCW_height = self.export_control_object.axis_rotation_degrees_THD_CCW_height
        self.axis_rotation_degrees_THD_CCW_depth = self.export_control_object.axis_rotation_degrees_THD_CCW_depth
        self.tick_numbering_rotation_degrees_THD_CCW_time = self.export_control_object.tick_numbering_rotation_degrees_THD_CCW_time
        self.tick_numbering_rotation_degrees_THD_CCW_height = self.export_control_object.tick_numbering_rotation_degrees_THD_CCW_height
        self.tick_numbering_rotation_degrees_THD_CCW_depth = self.export_control_object.tick_numbering_rotation_degrees_THD_CCW_depth
        try:#garbage
            self.override_export_control_object_values_with_gui_values() # not the best way. let the water flow downhill+++++++++ not the best way?
        except:
            False

    def set_export_control_object(self,export_control_object):
        self.export_control_object = export_control_object
    
    # messy, but not terrible
    def override_export_control_object_values_with_gui_values(self):
        if self.interface_object.export_control_override is True:
            self.axis_rotation_degrees_THD_CCW_time = self.interface_object.export_control_window_object.axis_rotation_degrees_THD_CCW_time
            self.axis_rotation_degrees_THD_CCW_height = self.interface_object.export_control_window_object.axis_rotation_degrees_THD_CCW_height
            self.axis_rotation_degrees_THD_CCW_depth = self.interface_object.export_control_window_object.axis_rotation_degrees_THD_CCW_depth

    def determine_which_plugins_to_use_no_gui(self):
        print('user_input.determine_which_plugins_to_use_no_gui(), pre add ref')
        print(f'self.import_style_plugin = {self.import_style_plugin}')
        print(f'self.export_style_plugin = {self.export_style_plugin}')
        print(f'self.color_style_plugin = {self.color_style_plugin}')
        print(f'self.import_style_plugin.type() = {type(self.import_style_plugin)}')
        print(f'self.export_style_plugin.type() = {type(self.export_style_plugin)}')
        print(f'self.color_style_plugin.type() = {type(self.color_style_plugin)}')

        self.import_style_plugin = self.add_plugins_reference(self.import_style_plugin)
        self.export_style_plugin = self.add_plugins_reference(self.export_style_plugin)
        self.color_style_plugin = self.add_plugins_reference(self.color_style_plugin)
        print(f'self.import_style_plugin = {self.import_style_plugin}')
        print(f'self.export_style_plugin = {self.export_style_plugin}')
        print(f'self.color_style_plugin = {self.color_style_plugin}')

    
    def determine_which_plugins_to_use_gui(self):
        # called in gui # actually called in main, evil

        self.import_style_plugin = self.add_plugins_reference(self.import_style_plugin)
        self.export_style_plugin = self.add_plugins_reference(self.export_style_plugin)
        self.color_style_plugin = self.add_plugins_reference(self.color_style_plugin)
        self._check_plugins()
        print(f'self.import_style_plugin = {self.import_style_plugin}')
        print(f'self.export_style_plugin = {self.export_style_plugin}')
        print(f'self.color_style_plugin = {self.color_style_plugin}')

    def _check_plugins(self):
        # need to improve these to skip the self.interface_object if it is none
        self.export_function = self._check_export_plugin()
        self.export_function_list = self._check_export_plugin_list()
        self.import_function = self._check_import_plugin()
        self.color_function = self._check_color_plugin_list()
        print(f'_check_plugins(): self.import_function = {self.import_function}')

    def _check_import_plugin(self):
        # this logic is hideous, fix it
        # ah this needs to work for gui and non gui, if dropdown does not exist
        print(f'user_input_object.import_style_plugin = {self.import_style_plugin}')
        plugin = self.import_style_plugin[0] # kinda dumb - remove from list, assuming only one entry
        #dropdown = self.import_style_dropdown[0]
        try:
            dropdown = self.color_style_dropdown[0]
        except:
            False
        if plugin == '' or plugin is None:
            try: # check if gui object was never assigned or the dro    pdown menu item doesnt exist
                self.import_function= self.interface_object.import_style_dictionary[dropdown]
            except:
                self.import_function = self.style_object.default_import_function
        else:
            if self._check_plugin_full_path(plugin):
                self.import_function= plugin
                print(f'Import plugin assigned:{plugin}')
            elif self.check_if_plugin_is_in_plugin_directory(plugin):
                self.import_function= plugin
                print(f'Import plugin assigned:{plugin}')
            else:
                try: # check if gui object was never assigned or the dropdown menu item doesnt exist
                    print(f'Override plugin not found in plugin directory, dropdown selection used instead')
                    self.import_function= self.interface_object.import_style_dictionary[dropdown]
                except:
                    self.import_function = self.style_object.default_import_function
        #self._push_import_plugin(self.style)
        return self.import_function

    def _check_export_plugin(self):
        # this logic is hideous, fix it
        self.export_function = []
        if False:#isinstance(self.export_style_plugin,list):
            plugin = self.export_style_plugin[0] # kinda dumb - remove from list, assuming only one entry
        else:
            plugin = self.export_style_plugin
            #print(F"pluing={plugin}")

        try:
            dropdown = self.export_style_dropdown[0]
        except:
            False
        for i,plugin in enumerate(self.export_style_plugin):
            if plugin == '' or plugin is None:
                try: # check if gui object was never assigned or the dropdown menu item doesnt exist
                    print(self.interface_object.export_style_dictionary[dropdown])
                    #self.export_function= self.interface_object.export_style_dictionary[dropdown]
                    self.export_function.append(self.interface_object.export_style_dictionary[dropdown])
                except:
                    self.export_function = self.style_object.default_export_function
            else:
                if self._check_plugin_full_path(plugin):
                    #self.export_function= plugin
                    self.export_function.append(plugin)
                    print(f'Export plugin assigned:{plugin}')
                elif self.check_if_plugin_is_in_plugin_directory(plugin):
                    #self.export_function= plugin
                    self.export_function.append(plugin)
                    print(f'Export plugin assigned:{plugin}')
                else:
                    try: # if gui object was never assigned or the dropdown menu item doesnt exist
                        #self.export_function= self.interface_object.export_style_dictionary[dropdown]
                        self.export_function.append(self.interface_object.export_style_dictionary[dropdown])
                    except:
                        self.export_function = self.style_object.default_export_function
        #print(f'self.export_function = {self.export_function}')
        if environment.pyinstaller()==False or environment.pyinstaller()==True: #24 Dec 24
            self.export_function = self.remove_duplicates(self.export_function)
        print(f'self.export_function = {self.export_function}')
        return self.export_function
        
    def _check_color_plugin_list(self):
        # this logic is hideous, fix it
        # need a way to split up into a comma separated list
        # need a way to add "plugin"
        # assumec color plugin is a single item (string) list  or multi item (string) list
        self.color_function = [] # is list
        #dropdown = self.color_style_dropdown[0]# convert list to first instance: drop down only allows for one style
        try:
            dropdown = self.color_style_dropdown[0]
        except:
            False
        for i,plugin in enumerate(self.color_style_plugin):
            if plugin == '' or plugin is None:
                try: # check if gui object was never assigned or the dropdown menu item doesnt exist
                    self.color_function.append(self.interface_object.color_style_dictionary[dropdown])
                except:
                    self.color_function = self.style_object.default_color_function
            else:
                if self._check_plugin_full_path(plugin):
                    self.color_function.append(plugin)
                    print(f'Color plugin assigned:{plugin}')
                elif self.check_if_plugin_is_in_plugin_directory(plugin):
                    self.color_function.append(plugin)
                    print(f'Color plugin assigned:{plugin}')
                else:
                    try: # check if gui object was never assigned or the dropdown menu item doesnt exist
                        self.color_function.append(self.interface_object.color_style_dictionary[dropdown]) # send to gui
                    except:
                        self.color_function = self.style_object.default_color_function
        #remove duplicates
        # this is a non ideal approach.
        self.color_function = self.remove_duplicates(self.color_function) # or make it so they don't add in the first place
        return self.color_function
    
    def _check_export_plugin_list(self):
        self.export_function_list = []
        try:
            dropdown = self.color_style_dropdown[0]
        except:
            False

        for i,plugin in enumerate(self.export_style_plugin):
            if plugin == '' or plugin is None:
                try: # check if gui object was never assigned or the dropdown menu item doesnt exist
                    self.export_function_list.append(self.interface_object.color_style_dictionary[dropdown])
                except:
                    self.export_function_list = self.style_object.default_export_function
            else:
                if self._check_plugin_full_path(plugin):
                    self.export_function_list.append(plugin)
                    print(f'Export plugin assigned:{plugin}')
                elif self.check_if_plugin_is_in_plugin_directory(plugin):
                    self.export_function_list.append(plugin)
                    print(f'Export plugin assigned:{plugin}')
                    

    def remove_duplicates(self,old_list):
        #print(f'with duplicates: {old_list}')
        fresh_list = []
        for i,entry in enumerate(old_list):
            if entry not in fresh_list:
                fresh_list.append(entry)
        #print(f'without duplicates: {fresh_list}')

        return fresh_list

    """ def check_or_make_as_list(self,color_style_plugin):# unused
        if isinstance(color_style_plugin,list):
            leave_it_as_a_list=1  
        elif isinstance(color_style_plugin,str):
            self.user_input_object.color_function=[color_style_plugin] """

    def check_if_plugin_is_in_plugin_directory(self,plugin_filename):
        #print(f"environment.pyinstaller() = {environment.pyinstaller()}")
        if environment.pyinstaller()==False:
            # allows dev to put plugin in python project directory, as a python file
            if plugin_filename.endswith('.py'):
                plugin_filename=plugin_filename
            else:
                plugin_filename = plugin_filename+'.py'

            if plugin_filename.startswith('plugins.'):
                plugin_filename = plugin_filename.replace('plugins.','')
            
            

            plugins_directory = Directories.get_core_dir()+'/plugins/' # for pavlov_exe # shit is not right
            
            #print(f'plugins_directory = {plugins_directory}')
            dir_list = os.listdir(plugins_directory)

            py_files = [file for file in dir_list if file.endswith('.py')]
            #if plugin_filename in dir_list: # any filetype, reckless
            return plugin_filename in py_files # boolean #means you must leave the extension. should really be using json 
        
        if environment.pyinstaller()==True:
            return True

    @staticmethod
    def _check_plugin_full_path(plugin_filepath):
        # allows dev to paste in full path
        if plugin_filepath.endswith('.py'):
            plugin_filepath=plugin_filepath
        else:
            plugin_filepath = plugin_filepath+'.py'
        return os.path.isfile(os.path.normpath(plugin_filepath))
    
    def add_plugins_reference(self,plugin_list):
        # checks names of plugins manually typed in developer gui and converts to a list, once checking that they exist
        if not(plugin_list is None):
            for i,plugin in enumerate(plugin_list):
                if plugin.startswith('plugins.'):
                    #plugin=plugin # no change
                    pass
                elif plugin.startswith('color_plugin_') or plugin.startswith('import_plugin_') or plugin.startswith('export_plugin_'):#***typical prefixes***
                    plugin_list[i] = 'plugins.'+plugin
                elif plugin == '' or plugin is None:
                    plugin = None
                else:
                    print(f'plugin:{plugin}')
                    print('Error, unexpected plugin name')
                    print('\nSee if files exist when the ***typical prefixes*** are added to the names')
        return plugin_list
    

        

        