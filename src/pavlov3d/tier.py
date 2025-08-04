'''
Author: Clayton Bennett
Created 12 January 2024

Purpose: Addressing all elements in a tier with shared aspects. Most just level number.
'''
import numpy as np
import copy
from pprint import pprint
# need better instantiation of tier class, noted 12 February 2024
class tier:#Tier:
    scene_object = None
    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object = scene_object
    @classmethod
    def assign_hierarchy_object(cls,hierarchy_object):
        cls.hierarchy_object = hierarchy_object

    def __init__(self,level):
        #self.name = str()
        self.key = level
        self.tier_level = level
        self.sub_tier_object = None # object
        self.super_tier_object = None # object

        self.dict_group_objects = dict()
        self.dict_curve_objects = dict()
        self.dict_members = dict()
        #self.stack_direction = 'diagonal_stack' # default # where are these set to not the default?
        #self.stack_vector = self.render_stack_vector(self.stack_direction) # set default
        self.stack_vector = None

        self.hierarchy_object.dict_tier_objects.update({level:self})# every time a tier object is created, it is added to the existing dictionary of tier objects, which exists as an attribute of scene_object
        """
        print(f"\ntype:{type(self.hierarchy_object.dict_tier_objects)}\n")
        print(f"\nvalues:{self.hierarchy_object.dict_tier_objects.values()}\n")
        print(f"\nkeys:{self.hierarchy_object.dict_tier_objects.keys()}\n")
        key = list(self.hierarchy_object.dict_tier_objects.keys())[-1]
        value = self.hierarchy_object.dict_tier_objects[key]
        print(f"\nkey:{key}\n")
        print(f"\nvalue:{value}\n")
        pprint(value.__dict__)
        """
        #self.hierarchy_object.dict_tier_objects_most = copy.deepcopy(self.hierarchy_object.dict_tier_objects)


        #self.fence_buffer = 0
        #self.padding = # padding is based on group, not tier

    def assign_stack_direction(self,stack_direction):
        self.stack_direction = stack_direction
        self.render_stack_vector(stack_direction)

    def add_group_object(self,group_object,key):
        group_object.tier_object = self # for the group object added, also add this tier_object as an attribute of the group_object
        group_object.tier_level = self.tier_level
        self.dict_group_objects.update({key:group_object})
        self._add_member(group_object,key)
    
    def add_curve_object(self,curve_object,key):
        #print(f'curve_object:{key}')
        curve_object.tier_object = self
        curve_object.tier_level = self.tier_level
        self.dict_curve_objects.update({key:curve_object})
        self._add_member(curve_object,key)
        
    def _add_member(self,memberObject,key):
        self.dict_members.update({key:memberObject})      

    def render_stack_vector(self,stack_direction):
        """ if self.stack_direction == "time_stack":
            self.stack_vector = np.array([1,0,0])
        elif self.stack_direction == "height_stack":
            self.stack_vector = np.array([0,1,0])
        elif self.stack_direction == "depth_stack":
            self.stack_vector = np.array([0,0,1])
        elif self.stack_direction == "coincident_stack":
            self.stack_vector = np.array([0,0,0])
        elif self.stack_direction == "diagonal_stack":
            self.stack_vector = np.array([1,0,1])
        elif self.stack_direction == "diagonal_THD_stack":
            self.stack_vector = np.array([1,1,1])
        elif self.stack_direction is None:
            self.stack_vector = np.array([0,0,0]) """

        
        map_stack = {"time_stack":np.array([1,0,0]),
        "height_stack":np.array([0,1,0]),
        "depth_stack":np.array([0,0,1]),
        "coincident_stack":np.array([0,0,0]),
        "diagonal_stack":np.array([1,0,1]),
        "diagonal_THD_stack":np.array([1,1,1])}

        if isinstance(stack_direction,str):
            self.stack_vector = map_stack[stack_direction]
        elif isinstance(stack_direction,list):
            self.stack_vector = np.array(list)
        elif isinstance(stack_direction,np.ndarray):
            self.stack_vector = stack_direction
        elif stack_direction is None:
            self.stack_vector = None
            #np.array([1,1,1])


        return self.stack_vector

        
