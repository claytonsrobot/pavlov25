'''
Author: Clayton Bennett
Title: scene
Created: 17 November 2023
Purpose: Create class that functions in Pavlov grouping hierarchy

Scale, translation, data object diameter, get, set
'''
from src.group import Group
from src.tier import tier as Tier
from src import arrayMath
#import text_label
import numpy as np
#import inspect
#import os # oof, barely needed


class Scene:
    style_object=None
    user_input_object=None
    allowed_keys = set(['padding','padding_coefficient',
                        'names','vectorArray_time','vectorArray_height','headers_time','headers_height',
                        'max_depth','min_depth','desciption_textbox','legend','group_hierarchy_tree','color_palette',
                        'axes_shared','text_box','title','max_raw_data','min_raw_data'])
    @classmethod
    def assign_user_input_object(cls,user_input_object):
        cls.user_input_object = user_input_object

    @classmethod
    def assign_style_object(cls,style_object):
        cls.style_object = style_object
        #style_object.assign_scene_object(cls) # nope. this assigns the class, not the instance

    @classmethod
    def assign_request(cls,request):
        cls.request = request
    
        
    def __init__(self,name="scene"):
        
        self.scene_object = self # good for copying and pasting and rigor
        self.name = name
        self.simple_name = name
        self.secret_full_name = "null0-null1-null2-null3"
        #self.place_in_supergroup=0
         
        self.blob_dir = 'https://6wuanrrsyel9ave8.public.blob.vercel-storage.com/'# you dont need this, it already knows and is not reduncdant
        self.__dict__.update((key, None) for key in self.allowed_keys)
        self.unix_start = None
        self.name = 'scene_object'
        self.type = 'scene_object'
        self.supergroup=None # this should stay this way # explicit. 
        self.minimum_corner_origin_relative_to_supergroup_minimum_corner_origin = None #explicit
        #self.export_filename_FBX = ""
        #self.export_filename_GLB = ""
        #self.export_control_object = None
        #self.import_control_object = None
        #self.color_control_object = None

        self.average_halftime = None

        self.padding = [0,0,0] # initialize
        self.only_longest_axes_ticks_siblings_and_cousins = True

        self.scale_vector=[1,1,1] # 3 value list

        self.dict_subgroups = dict()
        self.dict_group_objects_all = dict() # regardless of hierarchy
        self.dict_group_objects_most = dict() # regardless of hierarchy
        self.dict_curve_objects_all = dict() # regardless of hierarchy

        self.dict_curve_objects = dict() # this will ideally stay empty
        self.dict_children = dict()
        self.grand_cousin_flights_curves = dict()
        self.great_grand_cousin_flights_curves = dict()
        self.grand_cousin_flights_subgroups = dict()
        self.great_grand_cousin_flights_subgroups = dict()

        self.tier_level = 0
        #self.dict_tier_objects = dict() #migrated to hierarchy_object
        self.tier_object = None

        #self.average_halfwidth_time = None
        #self.average_halfwidth_height = None
        #self.average_halfwidth_depth = None
        #self.average_halfwidth_time = None
        #self.average_halfwidth_height = None
        #self.average_halfwidth_depth = None
        self.dict_text_labels = None

        #self.vectorArray_halfwidth_time = None
        #self.vectorArray_halfwidth_height = None
        #self.vectorArray_halfwidth_depth = None
        #self.vectorArray_direction = None
        
        self.filename_FBX = None
        self.filesize_FBX = None

        self.fence_lines = None

        self.desciption_textbox=None
        self.legend = None
        self.group_hierarchy_tree = None
        self.color_palette = None
        self.axes_shared = None
        self.text_box = None
        self.title = None
        self.max_raw_data = None 
        self.min_raw_data = None  

        self.span_relative_to_scene_data_origin = [[None,None],[None,None],[None,None]] 
        self.span_relative_to_scene_minimum_edge_at_zero_height_plane = [[None,None],[None,None],[None,None]] 
        self.span_relative_to_self_data_origin = [[None,None],[None,None],[None,None]] 
        self.span_relative_to_self_minimum_edge_at_zero_height_plane = [[None,None],[None,None],[None,None]] 
        self.diameter = np.array([0.0,0.0,0.0])

    def assign_program_start_timestamp(self,unix_start):
        self.unix_start = unix_start
        # look for filename time stamp

    def assign_export_obejct(self,export_control_object):
        self.export_control_object = export_control_object
    
    def assign_hierarchy_object(self,hierarchy_object):
        self.hierarchy_object = hierarchy_object
    
    def populate_basic_data(self,names,vectorArray_time,vectorArray_height,vectorArray_depth,
                             headers_time,headers_height,headers_depth):
        self.names = names

        self.headers_time = headers_time
        self.headers_height = headers_height
        self.headers_depth = headers_depth

        self.vectorArray_time = vectorArray_time
        self.vectorArray_height = vectorArray_height
        self.vectorArray_depth = vectorArray_depth
        self.assess_basic_data()
    
    def assess_basic_data(self):
        self.max_time = arrayMath.max_arrayMath(self.vectorArray_time)
        self.min_time = arrayMath.min_arrayMath(self.vectorArray_time)
        self.max_height = arrayMath.max_arrayMath(self.vectorArray_height)
        self.min_height = arrayMath.min_arrayMath(self.vectorArray_height)
        self.max_depth = arrayMath.max_arrayMath(self.vectorArray_depth)
        print(f"self.max_depth = {self.max_depth}")
        self.min_depth = arrayMath.min_arrayMath(self.vectorArray_depth)
        print(f"self.min_depth = {self.min_depth}")
       
    def populate_halfwidth_data(self,vectorArray_halfwidth_time,vectorArray_halfwidth_height,vectorArray_halfwidth_depth,
                                  average_halfwidth_time,average_halfwidth_height,average_halfwidth_depth):
        # the reason this exists is for explicit oversight from main.py
        self.vectorArray_halfwidth_time = vectorArray_halfwidth_time
        self.vectorArray_halfwidth_height = vectorArray_halfwidth_height
        self.vectorArray_halfwidth_depth = vectorArray_halfwidth_depth
        self.average_halfwidth_time = average_halfwidth_time
        self.average_halfwidth_height = average_halfwidth_height
        self.average_halfwidth_depth = average_halfwidth_depth

    def populate_direction_data(self,vectorArray_direction):
        self.vectorArray_direction = vectorArray_direction
    
    def add_subgroup(self, subgroup_object,key): # misnomer now, if the hierarchy is scene-groups-subgroups-curves. Is a group a subgroup of a scene? Good question. In the most rigorous sense, this leads to incorrect nomenclature, because the word "subgroup" infers the third tier.
        self.dict_subgroups[key]=subgroup_object
        self.dict_children = {**self.dict_subgroups,**self.dict_curve_objects}
        subgroup_object.add_supergroup(self)
        self.secret_full_name = self.secret_full_name.replace("null0-","scene-")
        
    def add_subgroup_values(self, subgroup_object,key):
        if self.max_raw_data is None:
            if subgroup_object.max_raw_data is None:
                print("the last level is broken") 
            else:
                self.max_raw_data = subgroup_object.max_raw_data
            
        else:
            for i in range(3):
                try:
                    if subgroup_object.max_raw_data[i]>self.max_raw_data[i]:
                        self.max_raw_data[i] = subgroup_object.max_raw_data[i]
                    
                except Exception:
                    print("SceneObject,EXCEPTION1")
                    print(f'self.name={self.name}')
                    print(f'subgroup_object={subgroup_object}')
                    print(f'subgroup_object.max_raw_data={subgroup_object.max_raw_data}')

        # investigate min_values
        if self.min_raw_data is None:
            if subgroup_object.min_raw_data is not None:
                self.min_raw_data = subgroup_object.min_raw_data # what if this is already none
            else: 
                print("UNEXPECTED-CONDITION:scene.py,subgroup_object.min_raw_data-is-none")
        else:
            for i in range(3):
                print(f"subgroup_object.max_raw_data = {subgroup_object.max_raw_data}")
                print(f"self.min_raw_data = {self.min_raw_data}")
                #if subgroup_object.max_raw_data[i]<self.min_raw_data[i]:
                #    self.min_raw_data[i] = subgroup_object.max_raw_data[i]
                if subgroup_object.min_raw_data[i]<self.min_raw_data[i]:
                    self.min_raw_data[i] = subgroup_object.min_raw_data[i]
                else:
                    pass
                    #print("EXCEPTION-2:subgroup_object-has-no-min-raw-data")

    def padding_assignment(self):
        if self.style_object.redundant_padding is True:
            self.padding = [max(self.max_raw_data)*self.style_object.padding_coefficient,
                            max(self.max_raw_data)*self.style_object.padding_coefficient,
                            max(self.max_raw_data)*self.style_object.padding_coefficient]
        elif self.style_object.redundant_padding is False:
            self.padding = [self.max_raw_data[0]*self.style_object.padding_coefficient,
                            self.max_raw_data[1]*self.style_object.padding_coefficient,
                            self.max_raw_data[2]*self.style_object.padding_coefficient]
            
        if self.style_object.group_padding_supressed is True:
            self.padding = [0,0,0]

        if self.style_object.universally_consistent_padding is True:
            self.padding = self.style_object.padding
        return True
    
    def set_diameter(self,diameter):
        self.diameter = diameter

    def calculate_diameter(self):
        # these are exciting times
        return

    def add_scene_description_textbox(self,text):
        # why does text label need user input object?
        minimum_corner_origin_relative_to_supergroup_minimum_corner_origin = [0,0,0]