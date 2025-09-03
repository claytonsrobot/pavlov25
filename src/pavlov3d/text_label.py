'''
Author: Clayton Bennett
Created: 15 January 2024
Title: TextLabel.py

Purpose OOP object for text Labels
Meant to define the spacial cylinder of a rotatable text label, including pre_label_buffer and post_label_buffer.
Inlude the lines_array.
Describe the vector for the cylinder direction, its center and start, the vector of the center and/or left and/or minimum_corner_origin relative to its parent object

Should also create a way to unpack and repack and edit rotation angles and scaling and padding, etc, after the fact
Which will be computationally non-optimal, but that's okay
Here, the initial rotation, scaling, and translation are embedded
The functions for unpacking, editing, and repacking those factors (rotation, scaling, and translation) should be different functions 

A part of the problem is that the curve object  (or group object) 
is the parent of all of these text_label_objects, right?
The parent object should be the thing itself - an axis is the parent of an axis label.

'''
import os
import numpy as np
from pathlib import Path

from pavlov3d.text_control_points import TextControlPointMachine 



class TextLabel:
    # these should be determined by style, raw data, and by user input and setting control
    
    scene_object = None
    user_input_object = None
    style_object = None
    
    @classmethod
    def assign_class_variables(cls, scene_object):
        cls.scene_object = scene_object
        cls.style_object = scene_object.style_object
        cls.user_input_object = scene_object.user_input_object
        TextControlPointMachine.assign_style_object(cls.style_object)
         
    def __init__(self):
        self.name = Path(__file__).name.lower().removesuffix('.py')
        self.text_control_points_machine = TextControlPointMachine()
        self.element_span_relative_to_parent_data_origin = None
    
    def assign_parent_object(self,parent_object):
        self.parent_object = parent_object 
        #if self.parent_object.dict_text_labels is None:
        #    self.parent_object.dict_text_labels = dict()

    def run_with_details(self,label_type='title_',
                         parent_object=None,# parent_object cannot stay None
                         text_string='',
                         text_height=1,
                         text_length=1,#text_length
                         direction_label_THD=[1,0,0],
                         wrap=False):
        

        #self.name = label_type+'_'+parent_object.name # override basic 'text_label' name
        self.name = label_type+parent_object.name # override basic 'text_label' name
        self.text_string = text_string #used
        #self.label_type = label_type
        self.text_length_unscaled = None
        #self.text_length_target = text_length # might include the final cursor space after the last letter, depending on how that is added
        # text_height must be determined by first generating the point cloud
        self.parent_object = parent_object
        self.parent_object.dict_text_labels.update({label_type:self})# should i super() this into different textLabel types? axisLabel, titleLabel, etc, so that they label_types are 'title', etc?
        #self.font_size=None # (mis)nomer for font size
        #self.text_height = None
        
        if label_type == 'title_':
            self.build_title_label_by_height(parent_object,text_height)
            #self.build_title_label_by_length(parent_object,text_length)
        elif label_type=='axis_time_':
            self.build_axis_label_time()
        elif label_type=='axis_height_':
            self.build_axis_label_height() 
        elif label_type=='axis_depth_':
            self.build_axis_label_depth()
        elif label_type == 'group_label_' and self.parent_object.tier_level == 1:
            self.build_tier1_group_label(parent_object)
        elif label_type == 'group_label_' and self.parent_object.tier_level == 2:
            self.build_tier2_group_label(parent_object)
        elif label_type == 'group_label_' and not(self.parent_object.tier_level == 1 or self.parent_object.tier_level == 2):
            self.build_group_label(parent_object)
            #self.check_for_max_group_label_length(text_length)
        elif label_type=='tick_numbering_time_':
            self.build_tick_numbering_time()
        elif label_type=='tick_numbering_height_':
            self.build_tick_numbering_height()
        elif label_type=='tick_numbering_depth_':
            self.build_tick_numbering_depth()
            
        elif label_type == 'textbox_':
            self._build_textbox(self.scene_object,self.user_input_object,text_string,text_length,direction_label_THD)
        else:
            # unexpected
            print('Unexpected label_type')

        return self
    
    def build_title_label_by_length(self,curve_object,text_length,label_type = 'title_'):
        # used once, in determine_text_height_for_curve_object_srg()
        self.build_text_by_height = False
        #print(f'build_title_label_by_length')
        self.label_type = label_type
        self.parent_object = curve_object
        self.label_relative_to_axis_over_or_under = 'over'
        self.size_coeff = self.style_object.text_size_coeff
        self.text_height = None
        self.text_length_target = text_length * self.style_object.text_size_coeff
        self.text_length_unscaled = text_length
        self.direction_label_THD = [1,0,0]
        self.direction_normal_THD = [0,0,1] # normal direction will actually become outdated once cylinder text labels are acheived. Actually, they can still have a three-element direction vector
        self.rot_deg_THD = curve_object.title_rotation_degrees_THD_CCW
        self.relevant_tick_length = curve_object.tick_halflength_THD[0]

        self.characters_array,text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,label_type=label_type)
        self.set_text_height(text_height)
        self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        
        self.parent_object.dict_text_labels.update({self.label_type:self})   

        return text_height
    
    def build_title_label_by_height(self,curve_object,text_height,label_type = 'title_'):
        # STANDARD, used, alternative to self.build_title_label_by_length()
        #print(f'build_title_label_by_height')
        self.build_text_by_height = True
        self.label_type = label_type
        # set control variables for text: set to default, or set to export_plugin values, or override with gui vars
        self.parent_object = curve_object
        #self.label_relative_to_axis_over_or_under = 'over' # imperfect
        self.label_relative_to_axis_over_or_under = 'under' # looks great, set 10 Feb 2024, quick and dirty way to get effectively aligned
        self.size_coeff = self.style_object.text_size_coeff # 1
        #print(f'text_length={text_length}')
        self.set_text_height(text_height * self.style_object.text_size_coeff)
        
        self.text_length_target = None
        self.text_length_unscaled = None

        self.direction_label_THD = [1,0,0]
        self.direction_normal_THD = [0,0,1] # normal direction will actually become outdated once cylinder text labels are acheived. Actually, they can still have a three-element direction vector
        self.rot_deg_THD = curve_object.title_rotation_degrees_THD_CCW

        self.relevant_tick_length = curve_object.tick_halflength_THD[0]
        self.characters_array,text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,label_type=label_type)
        # text_height is just there as a filler in this case
        self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        
        self.parent_object.dict_text_labels.update({self.label_type:self})   

        return self
    
    def build_group_label(self,group_object,text_length=None,label_type = 'group_label_'):
        self.build_text_by_height = True
        if self.build_text_by_height == True:
            if self.parent_object.tier_level == 1: 
                self.set_text_height(3*self.style_object.text_height_minimum_for_curve_objects) # 
            elif self.parent_object.tier_level == 2: 
                self.set_text_height(2*self.style_object.text_height_minimum_for_curve_objects) # this is where the relative group text value sizes are set, but the transation is separate. What a mess.
        self.label_type = label_type
        # here you can pull user_input_object values
        # currently setting axis as the time direction at the span edge of a group. Why not at the lower fence.
        # stil, that level of control is a distraction. Get span working. diameter calculation.
        self.parent_object = group_object
        self.label_relative_to_axis_over_or_under = 'over'#'under'#
        self.size_coeff = self.style_object.text_size_coeff

        self.vector_text_origin_relative_to_parent_data_origin = np.array([0,0,0])#group_object.minimum_edge_at_zero_height_plane_relative_to_self_data_origin
        # this is a possible place to change translation, but you would have to clarify betwen group and subgroup labels, if you want different outcomes
        self.direction_label_THD = [1,0,0]
        self.direction_normal_THD = [0,0,1] # normal direction will actually become outdated once cylinder text labels are acheived. Actually, they can still have a three-element direction vector
        self.rot_deg_THD = group_object.title_rotation_degrees_THD_CCW

        self.relevant_tick_length = 0
        #print(f'\nself.parent_object.group_label_object = self')
        #print(f'self.parent_object = {self.parent_object.name}')
        self.parent_object.group_label_object = self
        self.characters_array,self.text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,label_type=label_type)
        #self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        self.element_minimum_corner_origin_relative_to_group_minimum_edge_at_zero_height_plane,self.element_span_relative_to_parent_minimum_edge_at_zero_height_plane = self.assess_point_cloud_extremities(self.characters_array)
        self.parent_object.dict_text_labels.update({self.label_type:self}) 
        return True
    
    def build_tier1_group_label(self,group_object,text_length=None,label_type = 'group_label_'):
        self.build_group_label(group_object)
        # work with creae_FBX/group_texts_embedded_at_scene_level_or_group_level() - migrate to here-ish

    def build_tier2_group_label(self,group_object,text_length=None,label_type = 'group_label_'):
        self.build_group_label(group_object)
        # work with creae_FBX/group_texts_embedded_at_scene_level_or_group_level() - migrate to here-ish

    
    def build_axis_label_time(self,text_length=None,label_type='axis_time_'):
        self.build_text_by_height = True
        if self.build_text_by_height is True:
            self.set_text_height(self.style_object.text_height_minimum_for_curve_objects)
        self.label_type = label_type
        # trickle out the control of calculate_translation_vector() to here
        curve_object = self.parent_object
        self.direction_label_THD = [1,0,0]
        self.direction_normal_THD = [0,0,1] # this s actually dictate by initial over/under, akak standing/hanging, then rotation
        self.rot_deg_THD = self.user_input_object.axis_rotation_degrees_THD_CCW_time
        axis_label_size_coefficient = 0.3
        self.label_relative_to_axis_over_or_under = 'under'
        #self.label_relative_to_axis_over_or_under = 'over'
        self.size_coeff = self.style_object.text_size_coeff * axis_label_size_coefficient
        #self.text_length_target = text_length * self.size_coeff
        #self.text_length_unscaled = text_length
        self.relevant_tick_length = curve_object.tick_halflength_THD[0]
        
        self.characters_array,self.text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,label_type=label_type)
        self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        # here, element_minimum_corner_origin_relative_to_curve_data_origin is an output...it would be better if it could be an input, to control 
        self.parent_object.dict_text_labels.update({label_type:self})

        return True

    def build_axis_label_height(self,text_length=None,label_type='axis_height_'):
        self.build_text_by_height = True
        if self.build_text_by_height is True:
            self.set_text_height(self.style_object.text_height_minimum_for_curve_objects)
        self.label_type = label_type
        curve_object = self.parent_object
        self.direction_label_THD = [0,1,0]
        self.direction_normal_THD = [1,0,0] # these need to be accessed
        #self.rot_deg_THD = [45,0,90]
        self.rot_deg_THD = self.user_input_object.axis_rotation_degrees_THD_CCW_height
        
        axis_label_size_coefficient = 0.3 # get from style class
        self.label_relative_to_axis_over_or_under = "over" # or flip direction
        self.size_coeff = self.style_object.text_size_coeff * axis_label_size_coefficient
        #self.text_length_target = text_length * self.size_coeff 
        #self.text_length_unscaled = text_length

        self.relevant_tick_length = curve_object.tick_halflength_THD[1]

        self.characters_array,self.text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,label_type=label_type)
        self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        self.parent_object.dict_text_labels.update({label_type:self})

        return True

    def build_axis_label_depth(self,text_length=None,label_type='axis_depth_'):
        self.build_text_by_height = True
        if self.build_text_by_height is True:
            self.set_text_height(self.style_object.text_height_minimum_for_curve_objects)

        self.label_type = label_type
        
        curve_object = self.parent_object
        self.direction_label_THD = [0,0,1]
        self.direction_normal_THD = [1,0,0]
        #self.rot_deg_THD = [45,90,0] # set in export_plugin.py
        #self.rot_deg_THD = curve_object.axis_rotation_degrees_THD_CCW_depth
        self.rot_deg_THD = self.user_input_object.axis_rotation_degrees_THD_CCW_depth
        axis_label_size_coefficient = 0.3 # get from style class
        self.label_relative_to_axis_over_or_under = "under"

        self.size_coeff = self.style_object.text_size_coeff * axis_label_size_coefficient
        #self.text_length_target = text_length * self.size_coeff
        #self.text_length_unscaled = text_length

        self.relevant_tick_length = curve_object.tick_halflength_THD[2]

        self.characters_array,self.text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,label_type=label_type)
        self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        
        self.parent_object.dict_text_labels.update({label_type:self})

        return True

    def build_tick_numbering_time(self,text_length=None,label_type='tick_numbering_time_'):
        self.build_text_by_height = True
        if self.build_text_by_height is True:
            self.set_text_height(self.style_object.text_height_minimum_for_curve_objects/2)

        self.label_type = label_type
        
        curve_object = self.parent_object

        # does nothing
        self.direction_label_THD = [1,0,0]
        self.direction_normal_THD = [0,0,1]

        # does nothing

        #self.rot_deg_THD = [45,90,0]
        #self.rot_deg_THD = curve_object.axis_rotation_degrees_THD_CCW_depth
        self.rot_deg_THD = self.user_input_object.tick_numbering_rotation_degrees_THD_CCW_time
        self.rot_deg_THD = [0,0,0]
        self.rot_deg_THD = [0,0,90]
        self.rot_deg_THD = [90,90,0]
        #self.rot_deg_THD = [90,90,90]
        tick_numbering_label_size_coefficient = 0.1 # get from style class 
        self.label_relative_to_axis_over_or_under = "under"

        self.size_coeff = self.style_object.text_size_coeff * tick_numbering_label_size_coefficient
        #self.text_length_target = text_length * self.size_coeff
        #self.text_length_unscaled = text_length

        self.relevant_tick_length = curve_object.tick_halflength_THD[2]

        #self.translation_kit.translation_expression
        # you cant translate until you get the length and height....but you cant get the length and height until you get the character array
        # check the text_control_points_machine, intermediate steps, prior to packing.
        self.characters_array,self.text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,label_type=label_type) # you could probably break this up and call segments out here
        #print(f'ticks_numbering character array = {self.characters_array}')
        self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        
        self.parent_object.dict_text_labels.update({label_type:self})
        self.parent_object.dict_tick_numbering.update({'time':self})
        
        self.parent_object.tick_numbering_object_time.character_array = self.characters_array
        # tick_numbering_can_have_its_own_dictionary
        return True
    
    def build_tick_numbering_height(self,text_length=None,label_type='tick_numbering_height_'):
        self.build_text_by_height = True
        if self.build_text_by_height is True:
            self.set_text_height(self.style_object.text_height_minimum_for_curve_objects/2)

        self.label_type = label_type
        
        curve_object = self.parent_object
        self.direction_label_THD = [0,0,1]
        self.direction_label_THD = [0,1,0]
        self.direction_normal_THD = [1,0,0]
        #self.rot_deg_THD = [45,90,0]
        #self.rot_deg_THD = curve_object.axis_rotation_degrees_THD_CCW_depth
        #self.rot_deg_THD = self.user_input_object.tick_numbering_rotation_degrees_THD_CCW_height
        self.rot_deg_THD = [90,90,0]
        self.rot_deg_THD = [0,0,0]
        tick_numbering_label_size_coefficient = 0.1 # get from style class 
        self.label_relative_to_axis_over_or_under = "under"

        self.size_coeff = self.style_object.text_size_coeff * tick_numbering_label_size_coefficient
        #self.text_length_target = text_length * self.size_coeff
        #self.text_length_unscaled = text_length

        self.relevant_tick_length = curve_object.tick_halflength_THD[2]

        #self.translation_kit.translation_expression
        # you cant translate until you get the length and height....but you cant get the length and height until you get the character array
        # check the text_control_points_machine, intermediate steps, prior to packing.
        self.characters_array,self.text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,label_type=label_type) # you could probably break this up and call segments out here
        #print(f'ticks_numbering character array = {self.characters_array}')
        self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        
        self.parent_object.dict_text_labels.update({label_type:self})
        self.parent_object.tick_numbering_object_height.character_array = self.characters_array
        self.parent_object.dict_tick_numbering.update({'height':self})
        return True
    
    def build_tick_numbering_depth(self,text_length=None,label_type='tick_numbering_depth_'):
        self.build_text_by_height = True
        if self.build_text_by_height is True:
            self.set_text_height(self.style_object.text_height_minimum_for_curve_objects/2)

        self.label_type = label_type
        
        curve_object = self.parent_object
        self.direction_label_THD = [0,0,1] # use, wrong
        self.direction_label_THD = [0,1,0] # use, wrong
        self.direction_normal_THD = [1,0,0] # use, wrong
        #self.rot_deg_THD = [45,90,0]
        #self.rot_deg_THD = curve_object.axis_rotation_degrees_THD_CCW_depth
        #self.rot_deg_THD = self.user_input_object.tick_numbering_rotation_degrees_THD_CCW_depth
        self.rot_deg_THD = [0,90,-270]
        self.rot_deg_THD = [0,90,0]
        self.rot_deg_THD = [0,90,0]
        self.rot_deg_THD = [90,0,0]
        tick_numbering_label_size_coefficient = 0.1 # get from style class 
        self.label_relative_to_axis_over_or_under = "under"

        self.size_coeff = self.style_object.text_size_coeff * tick_numbering_label_size_coefficient
        #self.text_length_target = text_length * self.size_coeff
        #self.text_length_unscaled = text_length

        self.relevant_tick_length = curve_object.tick_halflength_THD[2]


        # you cant translate until you get the length and height....but you cant get the length and height until you get the character array
        # check the text_control_points_machine, intermediate steps, prior to packing.
        self.characters_array,self.text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,label_type=label_type) # you could probably break this up and call segments out here
        #print(f'ticks_numbering character array = {self.characters_array}')
        self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        
        self.parent_object.dict_text_labels.update({label_type:self})
        self.parent_object.tick_numbering_object_height.character_array = self.characters_array
        self.parent_object.dict_tick_numbering.update({'depth':self})
        return True

    def check_for_max_group_label_length(self,length):
        if length > self.style_object.padding[0]:
            self.style_object.padding = np.array([length,length,length])
        


    def _build_textbox(self,text_string,direction_label_THD):
        self.build_text_by_height = False
        #self.label_type = label_type
        #self.direction_label_THD = [1,0,0]
        self.direction_label_THD = direction_label_THD
        textbox_size_coefficient = 1.0
        self.size_coeff = 1
        self.label_relative_to_axis_over_or_under = "over"
        self.text_length_target = text_length * self.style_object.text_size_coeff * textbox_size_coefficient
        self.characters_array,self.text_height = self.text_control_points_machine.text_string_control_points(text_string,self.text_length,label_type=self.label_type) # wrong
        self.element_minimum_corner_origin_relative_to_curve_data_origin,self.element_span_relative_to_parent_data_origin = self.assess_point_cloud_extremities(self.characters_array)
        self.parent_object.dict_text_labels.update({self.label_type:self})
        self.text_length_unscaled = text_length

        self.relevant_tick_length = 0
        return True

    """ 
    def set_font_size(self,font_size):
        # used in 
        self.font_size = font_size """

    def assess_point_cloud_extremities(self,characters_array):
        #print(f'len(characters_array) = {len(characters_array)}')
        # assumes no word is rotated such that the first letter will have any values greater than the last letter
        first_character_array = np.array(characters_array[1][1]) # hack

        last_character_array = np.array(characters_array[len(characters_array)-2][1]) # hack

        min_time = min(first_character_array[:,0])
        min_height = min(first_character_array[:,1])
        min_depth = min(first_character_array[:,2])
        max_time = max(last_character_array[:,0])
        max_height = max(last_character_array[:,1])
        max_depth = max(last_character_array[:,2])

        element_minimum_corner_origin_relative_to_some_origin = [min_time,min_height,min_depth] # assumption that any rotation has been correct
        ##element_max_corner_relative_to_curve_data_origin = [max_time,max_height,max_depth] # assumption # no one needs this
        element_span_relative_to_some_origin =[[min_time,max_time],[min_height,max_height],[min_depth,max_depth]] # assumption

        return element_minimum_corner_origin_relative_to_some_origin,element_span_relative_to_some_origin 

    def set_text_height(self,text_height):
        self.text_height = text_height
    
    def set_text_length_scaled(self,text_length_scaled):
        self.text_length_scaled = text_length_scaled