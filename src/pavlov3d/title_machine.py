'''
Author: Clayton Bennett
Created: 06 March 2024
Title: title_machine.py

If this is run from main, it infers that everything need not be known at curve_object instantiation. Ergo, there needs to be an expansion method.
Or, the middle road is that the driving characterstics of title are known, so that the dimensions are known before it is built. But that sounds risky.
'''
#import numpy as np
#import math
#import copy
import os
from src.pavlov3d.text_label import TextLabel
from src.pavlov3d.text_height import TextHeight
from src.pavlov3d.text_translation import TranslationKit
#import title
class TitleMachine:
    # last i checked this title machine is only used for curve titles, not group titles
    scene_object=None
    style_object=None
    user_input_object=None
    hierarchy_object = None
    
    @classmethod
    def assign_scene_object_etc(cls, scene_object):
        cls.style_object = scene_object.style_object
        cls.scene_object = scene_object
        cls.user_input_object = scene_object.user_input_object
        cls.hierarchy_object = scene_object.hierarchy_object
        TextLabel.assign_class_variables(scene_object)

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py')
        self.friendly_name = 'title'
        self.text_height_machine = TextHeight()

    def determine_best_text_height(self):
        # called in main
        #print('title_machine.determine_best_text_height() ...')
        print('\nIf you have a curve with a very short time length \n\
            relative to your other curves, \n\
            your text and axis ticks will probably be very small.\n')

        # labels should be made in bulk, run by text height rather than length
        # find the curve_object with the smallest ratio of length divided by letter count
        # use that length to generate a point cloud of letters, identify the height of that point cloud
        # and save the text height to be used for all other curve_object titles, in bulk
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            #text_length = curve_object.max_time
            text_length = max(curve_object.dict_data_vectors_scaled["time"])
            text_string=curve_object.name
            self.text_height_machine.check_characteristic_length_over_character_count_ratio(text_length,text_string,curve_object)
        print(f"self.text_height_machine.curve_object_key_srg = {self.text_height_machine.curve_object_key_srg}")
        curve_object_srg = self.hierarchy_object.dict_curve_objects_all[self.text_height_machine.curve_object_key_srg]
        print(f'curve_object_srg.name = {curve_object_srg.name}')
        text_height_minimum = self.text_height_machine.determine_text_height_for_curve_object_srg(curve_object_srg,title_machine = self)*1.7 # hacky garbage, forced, to appear proper even though it isnt, Feb 2025
        self.style_object.text_height_minimum_for_curve_objects = text_height_minimum
        return text_height_minimum # returns to main, if you wannt

    def generate_title_for_each_curve(self,text_height):
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            self.build_title(curve_object,text_height)

    def build_title(self,curve_object,text_height):
        curve_object.title_object=TextLabel()
        curve_object.title_object.assign_parent_object(curve_object)
        curve_object.title_object.trk = TranslationKit()
        if False:#'depth_stack' in self.user_input_object.stack_direction_list:
        # it would be far better to instead have a list of which counsins share the stack column and row in the 'cell hive'. This would be illucidated in scene.py, in the cousin determination.
            curve_object.title_object.trk.translation_expression = "[0,0,-1.2*text_height]"
            curve_object.title_object.trk.rotation_expression = "[0,0,0]"

        else:
            curve_object.title_object.trk.translation_expression = "[0,-2.3*text_height,-1.2*text_height]"
            curve_object.title_object.trk.rotation_expression = "[-45,0,0]" 
        

        max_time = max(curve_object.dict_data_vectors_scaled["time"])
        curve_object.title_object.run_with_details(label_type='title_',
                                                parent_object=curve_object,
                                                text_string=curve_object.name,
                                                text_height = text_height,
                                                text_length = max_time)
    
        return True