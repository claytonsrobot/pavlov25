'''
Author: Clayton Bennett
Created: 17 January 2024
Title: style.py

Purpose: Not exactly sure yet,but we need logic to control how styles appear.
This logic has up to this point been in individual element  (ex. title) scripts and in main.py.
It is time to improve :)
'''

'''
GUI should generate a settings file, json, for setttings values, both default and controlled
values:
    FBX_conversion_limit
    styleChoice_depth00
    choke values
    alignment/translation_scheme: 'diagonal' or 'grouped',
    file_encoding: 'bin' or 'ascii'
    plotting_style: 'triangleColumns' or 'bars'
    n_ticks = 5
    tick_length_ratio = 0.05
    tick_length_ratio_redundantAxis = 0.06
    # add option for axis label size, as percentage of axis length
    axisLabel_alignment = 'center'
    delete_FBX_manualOverride = False
    point_size
    title/label rotation
    overlapping data or isolated data
    embed graphs
    local fences or distant fences
    local title or distant titles (especially for temperature and for top view)

style factors: #the variables automatically adjusted based on style selection, with opportunity for custom control
    Title orientation
    translation of objects within groups (diagonal vs tempterature vs overlap)
    axis label orientation
    far or close fences / labels
    '''
#import inspect # to check that the export plugin was pulled properly
#import logging 
import numpy as np
#import os
import importlib
from src import environmental 
from src import deltaList 
from src import arrayMath
from src.createFBX import CreateFBX
#from createDXF_ import CreateDXF
#import plugins # like this, for pyinstaller

"""pyinstaller work around"""
# i hate this
if environmental.pyinstaller()==True:
    from plugins import color_plugin_per_curve
    from plugins import color_plugin_per_group
    from plugins import color_plugin_per_subgroup
    from plugins import color_plugin_singular_keys_barchart
    from plugins import color_plugin_true_gradient
    from plugins import color_plugin_binned_gradient
    from plugins import export_plugin_createFBX_bar_3D
    from plugins import export_plugin_createFBX_bar_3Dvert
    from plugins import export_plugin_createFBX_bar_3Dvert_heavy 
    from plugins import export_plugin_createFBX_bar_gratzer_USGS 
    from plugins import export_plugin_createFBX_line_2D
    from plugins import export_plugin_createFBX_line_3D
    from plugins import export_plugin_createFBX_plus
    from plugins import export_plugin_createFBX_square_columns_2D
    from plugins import export_plugin_createFBX_square_columns_3D
    from plugins import export_plugin_createFBX_square_depth
    from plugins import export_plugin_createFBX_square_depth_gratzer_USGS 
    from plugins import export_plugin_createFBX_triangle_columns_2D
    from plugins import export_plugin_createFBX_triangle_columns_3D
    from plugins import import_plugin_CSV_2D
    from plugins import import_plugin_CSV_3D
    from plugins import import_plugin_GPX_3D
    #from core.plugins import import_plugin_CSV_singleSheet_multiRow # evil SOB

def fill_list_with_value(length,value):
    vector = [value] * length
    return vector
    
#print(color_plugin_binned_gradient)
#print(plugins)
#from plugins import *
class Style:
    
    scene_object = None
    user_input_object = None

    allowed_keys = set(['text_color','coefficient_deltaTime','maxTime','createFBX_model_color'])

    @classmethod
    def assign_user_input_object(cls,user_input_object):
        cls.user_input_object = user_input_object
    
    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object=scene_object


    def __init__(self):
        self.__dict__.update((key, None) for key in self.allowed_keys)
        self.name = 'style_object'
        self.environmental = environmental

        #list_plugins = self.pre_import_all_plugins()


        #self.file_encoding = 'bin'
        self.point_size=0.2
        self.point_size=0.002
        self.depthByHeight_coeff = 0.5# 0.5 looks nice: it makes sense because the height direction typically requires no stacking, each item has the whole vertical screen. But this isn't true from top view, so compression is useful.
        self.coefficient_deltaTime = 1 # coefficient compared to width of bar in time direction
        self.text_size_coeff    = 1.0 # the title takes up the whole length of the time axis
        self.axis_stacked_redundancy = ['make_redundant_and_non_redundant', 'only_largest_stacked','place_only_largest_stacked_at_extremity','exploded_and_non_redundant']

        # make only the longest axis in shortest in stack direction and grandfather stack
        # make all axess
        # make them supressible
        # put curve axes at top of tree
        # put axes in at extremity

        self.group_labels_outside_fences = True


        #self.power_user = False
        self.use_CLI = False # fix location
        self.use_GUI = False# False#True
        self.developer_mode_gui = False
        interface_list = ['json','gui_simple','gui_developer','control_cli']
        self.interface_choice  = 'json'

        self.curve_positive_axes_only = True
        # This is the current paradigm. It does NOT have to stay the paradigm.
        # The primary benefit of this paradigm is that it allows all data to be aligned on the 0-height plane. 0-depth and 0-time plane alignment for the initial relevant groups is interesting as well.
        # It is much easier to continue with the project using the current 0-0-0 origin paradigm. There are significant drawbacks, namely a lack of scalability (or rather translationability) to axis lines that are not of 0 value. 
        # fuck this noise

        self.createFBX_model_color = None # initialization, used in color plugins

        self.text_color = 'black'
        self.text_color = 'green_contrast_text' # shows up white
        #self.text_color = 'blue_contrast_text' # shows up white
        #self.text_color = 'custom_RGB' # shows up yellow
        
        '''Key plot element controls, should be accessible by user'''
        self.createFBX_embed_ticks_in_curve_object_at_scene_level_or_curve_level_or_none = 'scene'
        self.createFBX_embed_tick_numbering_at_scene_level_or_curve_level_or_none = 'scene'
        self.createFBX_embed_exploded_tick_numbering_at_scene_level_or_curve_level_or_none = 'scene'
        self.createFBX_embed_axes_in_curve_object_at_scene_level_or_curve_level_or_none='scene'#'curve'
        self.createFBX_embed_text_axes_labels_in_curve_object_at_scene_level_or_curve_level_or_none='curve'
        self.createFBX_embed_text_in_curve_object_at_scene_level_or_curve_level_or_none='scene'#'curve'#True
        self.createFBX_embed_fence_in_curve_object_at_scene_level_or_curve_level_or_none='none'#'scene'#'curve'# None
        self.group_fences_embedded_at_scene_level_or_group_level = 'scene'#'scene'#'group'#'scene'
        self.group_texts_embedded_at_scene_level_or_group_level = 'scene'#'group'#'scene'

        self.color_function_list = None
        self.export_function_list = None

        self.include_curve_object_axis_labels =True# False# True
        self.consistent_tick_size = True

        self.group_padding_supressed = True#  if false, secondary cousin alignment will break, 09 June 2024
        self.padding_coefficient = 0.2#0
        self.redundant_padding = False#True
        self.universally_consistent_padding = True
        self.padding = np.array([1,1,1])
        self.add_bottom_fence_only =  True#False#True

        self.styleChoice_depth00 = 'depthByHeight_coeff'
        #self.plotting_style = 'temperature'
        #self.plotting_style = 'lineGraph_2D' # can reference name of export_plugin_object. name

        self.default_import_function = 'plugins.import_plugin_CSV_2D'
        self.default_export_function = 'plugins.export_plugin_createFBX_lineGraph_3D'
        self.default_color_function = 'plugins.color_plugin_per_curve'

        self.paradigm ='0-0-0 axes origin'
        #self.fences_embedded_in_model_hierarchy = False # False is good, it means you can suppress fences easily fromwithin the model, for your viewing pleasure.
        #self.groupLabels_embedded_in_model_hierarchy = False#True #False 
        
        self.find_numbers_in_filenames_and_equalize_digits=True # this currently only works to add a preceding 0 to the last single-digit numeric entry, and ignores items that have less than the highest count of numeric entries
        
        self.n_numeric_island_size_target_after_leading_zero_insertion=3 # 2 
        self.calculate_FBX_normal_and_material_layers = False # if True, file will be 50% larger, with no apparent useful improvements


        # DEADLINE- MAKE THIS EXIST BY APRIL 10 OR DEStrOY CONCEPT
        self.group_label_axis_high_or_low_or_zero = 'zero' # 'high' # 'low'

        # kb # 150,000 is too high, 20,000 is great. There's a sweet spot somewhere in between. Make graph, including number of data points and time to completion.
        #FBX_conversion_limit =40000
        self.FBX_conversion_limit = 16000 # kb



    def use_consistent_tick_size_as_consistent_padding(self,size):
        self.padding = np.array([size,size,size])
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            curve_object.padding = self.padding
        for group_object in self.hierarchy_object.dict_group_objects_all.values():
            group_object.padding = self.padding

    def prepare_color_modules(self):
        color_plugin_list = []
        for color_function in self.user_input_object.color_function:# assumes color_function is a list # this is different than the export and import versions, which are assumed to only ever have one entry (for the time being)
            color_plugin_class=self.assign_plugin_dynamically(module_name = color_function) # type is function
            color_plugin_object = color_plugin_class()
            color_plugin_object.assign_scene_object(self.scene_object)
            color_plugin_object.prepare_color_style()   
            color_plugin_list.append(color_plugin_object)
        return color_plugin_list
    
    def prepare_export_modules(self):
        export_plugin_list = []
        for export_function in self.user_input_object.export_function:
        #for export_function in self.user_input_object.export_function_list:
        #for color_function in self.user_input_object.color_function:# assumes color_function is a list # this is different than the export and import versions, which are assumed to only ever have one entry (for the time being)
            ExportPlugin=self.assign_plugin_dynamically(module_name = export_function) # type is function
            export_plugin_object = ExportPlugin()
            export_plugin_object.assign_style_object(style_object = self)
            #export_plugin_object.prepare_color_style()   
            export_plugin_list.append(export_plugin_object)
        self.set_export_function_list(export_plugin_list)
        return export_plugin_list

    def load_export_control_object(self,export_function):# called in main # is it?
        # 
        ExportPlugin=self.assign_plugin_dynamically(module_name = export_function) # type is function
        ExportPlugin.assign_style_object(style_object = self) # and vice versa
        export_control_object = ExportPlugin()
        return export_control_object

    def prepare_publishing_module(self,export_control_object):# called in main
        # modularize Beyond FBX 
        CreateFBX.assign_scene_variabes(scene_object = self.scene_object)
        createFBX_object = CreateFBX(self.scene_object.filename_FBX,self.user_input_object.file_encoding)
        createFBX_object.assign_export_control_object(export_control_object) # instead, make the export object here,then pass it to createFBX_object
        createFBX_object.assign_color_function_list(self.color_function_list)
        return createFBX_object
    
    def prepare_curve_and_group_elements_from_export_style(self,export_function):#export_control_object
        def _check_for_characteristic_length(group_object):
            if group_object.characteristic_length is None:
                print("\ngroup_object.characteristic_length is None")
                print('ERROR: You probably failed to include a proper group, tier 1.\n')
        export_plugin_object = self.load_export_control_object(export_function[0]) # why reload? the alterative it to input the export control object from main, or to store it in this class instance.
        
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            export_plugin_object.run_per_curve(curve_object)
        #for group_object in self.hierarchy_object.dict_group_objects_all.values():
        for group_object in self.hierarchy_object.dict_group_objects_most.values():
            _check_for_characteristic_length(group_object)
            export_plugin_object.run_per_group(group_object) # bruh its just geometry, why does it have to be this hard
            # literally just title tilt, whichwill only appear once

    def prepare_import_module(self):
        print(f"self.user_input_object.import_function = {self.user_input_object.import_function}")
        DynamicImportPlugin=self.assign_plugin_dynamically(module_name = self.user_input_object.import_function) # type is function
        import_function_object = DynamicImportPlugin()
        return import_function_object
    
    def set_color_function_list(self,color_function_list):
        self.color_function_list = color_function_list

    def set_export_function_list(self,export_function_list):
        self.export_function_list = export_function_list
        #print(f'Do me later')

    def assign_hierarchy_object(self,hierarchy_object):
        self.hierarchy_object = hierarchy_object
    
    def assign_plugin_dynamically(self,module_name):
        # https://stackoverflow.com/questions/41678073/import-class-from-module-dynamically
        print(f'assign_plugin_dynamically, module_name: {module_name}') # showing as None, crap
        #print(f"environmental.pyinstaller() = {environmental.pyinstaller()}")
        if environmental.pyinstaller()==False:
            module = importlib.import_module(module_name)
        elif environmental.pyinstaller()==True: # for pyinstaller, pre imported using self.pre_import_all_plugins
            module = eval(module_name.replace("plugins.",""))
            #print(plugins.__dict__)
            #module = eval(module_name) # if import plugins worked. possibly eval
            # print(f"module = {module}") # securirty risk, exposes the temp directory
            #print(f"module.__dict__ = {module.__dict__}")
        plugin_class = module.Plugin # each of the plugin files describe some class plugin. Here, plugin in the class name.
        return plugin_class
              
    """
    def pre_import_all_plugins(self): # not used, as aof 25 Dec 2024 and prior, listed manually
        list_plugins = []
        cwd = os.getcwd()
        cfd = os.path.dirname(__file__)
        os.chdir(cfd+"\\plugins\\")
        print(f"here: {os.getcwd()}")
        all_plugins = os.listdir()
        for module_name in all_plugins:
            module = importlib.import_module(module_name)
            list_plugins.append(module)
        os.chdir(cwd)
        return list_plugins
    """
    

    def prepare_missing_depth(self,vectorArray_time,vectorArray_height):
        n_datapoints = len(vectorArray_height)
        # this shit is outdated.
        # also now that we are intializing curve_object in import, we do not have the luxury of knowing the entire dataset before we set missing values. 
        # that might be okay. But it is also okay to come up with a scheme to revisit once all is known.
        width_coefficient_perBar = 300 #
        width_coefficient_byMaxTime = 0.2
        standardWidth=4
        depthByHeight_coeff = 0.5
        self.depthByHeight_coeff = depthByHeight_coeff

        i=0
        halfdepth_list = [[]]
        while i<len(vectorArray_time):
            j=0
            halfwidthtime_min = deltaList.halfdelta_min(vectorArray_time[i]) # find minimum difference between all points in a vector
            while j<len(vectorArray_time[i]):
                if self.styleChoice_depth00 == 'perBar': # based on 
                    halfdepth_list[i].append(width_coefficient_perBar*self.coefficient_deltaTime*halfwidthtime_min)
                elif self.styleChoice_depth00 == 'depthByHeight_coeff':
                    halfdepth_list[i].append(depthByHeight_coeff*vectorArray_height[i][j])
                elif self.styleChoice_depth00 == 'byMaxTime':
                    halfdepth_list[i].append(width_coefficient_byMaxTime*self.maxTime)
                elif self.styleChoice_depth00 == 'square_depthEqualHeight':
                    halfdepth_list[i].append(vectorArray_height[i][j]/2)
                elif self.styleChoice_depth00 == 'depth20Height':
                    halfdepth_list[i].append(0.2*vectorArray_height[i][j]/2)
                elif self.styleChoice_depth00 == 'depth10Height':
                    halfdepth_list[i].append(0.1*vectorArray_height[i][j]/2)
                elif self.styleChoice_depth00 == 'depth05Height':
                    halfdepth_list[i].append(0.05*vectorArray_height[i][j]/2)
                elif self.styleChoice_depth00 == 'standardDepth':
                    halfdepth_list[i].append(standardWidth)
                elif self.styleChoice_depth00 == 'standardDepth_perObjectMax10':
                    halfdepth_list[i].append(0.1*max(vectorArray_height[i])/2)
                elif self.styleChoice_depth00 == 'temperature': # don't actually need this, because point size is assigned anyways in the export plugin
                    halfdepth_list[i].append(self.point_size)
                elif self.styleChoice_depth00 == 'depth10Height_plusThisMaxWidth':
                    objectMax10 = 0.1*max(vectorArray_height[i])/2
                    halfdepth_list[i].append(0.1*vectorArray_height[i][j]/2+objectMax10)
                else: #as if self.styleChoice_depth00 == 'depth10Height'
                    halfdepth_list[i].append(0.1*vectorArray_height[i][j]/2)
                j=j+1
            i=i+1
            if i<len(vectorArray_time): # only do this if there is going to be another round (don't do it on the last round)
                halfdepth_list.append([]) 

        # convert to tuples
        halfdepth_list = tuple(tuple(i) for x,i in enumerate(halfdepth_list))
        vectorArray_depth = halfdepth_list # double name for now, until a full shift is made to the standard of vectorArray_depth # naming convention is based on the original bar style, where the origin was the center of the bar, with a halfdepth positive and then negative on each side from the origin
        return vectorArray_depth
    
    def prepare_missing_halfwidth_vector_general(self,vector):
        halfwidth_min_reasonable_i = deltaList.halfdelta_min_reasonable_finder(vector) # find minimum difference between all points in a vector
        halfwidth_list = fill_list_with_value(len(vector),halfwidth_min_reasonable_i)
        return halfwidth_list


    def prepare_missing_direction_vectorArray(self,vectorArray_time,vectorArray_height,vectorArray_depth):#oh baby
        # for domino style, or from GPX files of any kinda
        # or for just a cool style:
        # calculat direction of each point as parallel to the lines drawn between the point before it and the point after it
        vectorArray_direction = None
        return vectorArray_direction

    
    def override_style_with_cij(self):
        
        for key,value in self.user_input_object.cij.items():
            if key in self.__dict__.keys():
                self.__dict__[key] =  value

    def calculate_halfwidths_and_directions(self):
        for curve_object in self.scene_object.hierarchy_object.dict_curve_objects_all.values():
            curve_object.dict_data_vectors_scaled["halfwidth_time"] = self.prepare_missing_halfwidth_vector_general(curve_object.dict_data_vectors_scaled["time"])
            curve_object.dict_data_vectors_scaled["halfwidth_height"] = self.prepare_missing_halfwidth_vector_general(curve_object.dict_data_vectors_scaled["height"])
            curve_object.dict_data_vectors_scaled["halfwidth_depth"] = self.prepare_missing_halfwidth_vector_general(curve_object.dict_data_vectors_scaled["depth"])

            for j,datapoint_object in enumerate(curve_object.dict_datapoints.values()):
                datapoint_object.dict_data_scaled["halfwidth_time"] = curve_object.dict_data_vectors_scaled["halfwidth_time"][j]
                datapoint_object.dict_data_scaled["halfwidth_height"] = curve_object.dict_data_vectors_scaled["halfwidth_height"][j]
                datapoint_object.dict_data_scaled["halfwidth_depth"] = curve_object.dict_data_vectors_scaled["halfwidth_depth"][j]

