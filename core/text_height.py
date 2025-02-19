'''
Title: TextHeight.py
Author: Clayton Bennett
Created: 16 June 2024

16 June 2024:　　　＃
Text labels for curves should all be consistent by height
First, it should be determined what shortest necessaru letter height is:
This is for the longest relative label with the shortest characteristic length
Character count can be a stand in for relative label length
Axis length can be a stand in for characteristic length (see what is already done)
(Recall that currently all axis labels are in the positive spectrum, but it doesn't need to be this way)
Before determining the point cloud of characters for each label, 
find the largest ratio of character count divided by characteristic length.
Then, determine the height for this text label, and use it for everything else

The group tier 1 and tier2 labels will be made to be 33% or 50% larger than the curve text height
- this could be a problem, but we'll let it arise on its own

Ideally, all of this can be dealt with after scaling the axes,  to limit size problems.

axes labels, title label, group label
'''
from text_control_points import text_control_points_machine as text_control_points_machine_class
from text_label import TextLabel

class TextHeight:
    
    def __init__(self):
        True
        self.text_control_points_machine = text_control_points_machine_class()
        self.text_height_minimum = None # text_height_curves
        #self.text_height_curves = 0 # unused
        #self.text_height_groups_tier1 = 0
        #self.text_height_groups_tier2 = 0
        
        self.curve_object_key_srg = None# small ratio guide, applies to titles for curves which have one known characteristic length
        self.ratio_srg = 1000.0 # initialized at an unreasonably large number
    

    def check_characteristic_length_over_character_count_ratio(self,characteristic_length,text_string,curve_object):
        # must be run for all curve objects in scene object before text height can be determined
        character_count = len(text_string)
        ratio = characteristic_length/character_count
        if ratio < self.ratio_srg:
            #print(f'ratio = {ratio}')
            self.ratio_srg = ratio
            self.curve_object_key_srg = curve_object.name.lower() # assumesname serves as the key to hierarchy_object.dict_curve_objects_all
        elif self.curve_object_key_srg is None:
            self.curve_object_key_srg = curve_object.name.lower()

    def determine_text_height_for_curve_object_srg(self,curve_object_srg,title_machine):
        #curve_object_srg
        #text_length
        #text_length = curve_object_srg.max_time
        text_length = max(curve_object_srg.dict_data_vectors_scaled["time"])
        print(f'text_height: text_length: {text_length}')
        text_label_object = TextLabel()
        text_label_object.text_string = curve_object_srg.name
        text_label_object.label_type = 'title_'
        text_height = text_label_object.build_title_label_by_length(curve_object_srg,text_length)
        #text_label_object
        #curve_object_srg.title_object = title_machine.build_title(curve_object_srg)
        #print(f'curve_object_srg.title_object.text_height = {curve_object_srg.title_object.text_height}')
        #characters_array,text_height = self.text_control_points_machine.text_string_control_points(text_label_object = self,# self is the problem
        #                                                                                         label_type=label_type)
        # do not need characters_array here
        self.text_height_minimum = text_height
        print(f'text_height.text_height_minimum = {self.text_height_minimum}')
        return self.text_height_minimum



