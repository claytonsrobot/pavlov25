'''
Author: Clayton Bennett
Created: 06 March 2024
Title: axis_labels_machine.py

If this is run from main, it infers that everything need not be known at curve_object instantiation. Ergo, there needs to be an expansion method.
Or, the middle road is that the driving characterstics of title are known, so that the dimensions are known before it is built. But that sounds risky.
'''
#import numpy as np
#import math
import os
from pathlib import Path
from pavlov3d.text_label import TextLabel
from pavlov3d.text_translation import TranslationKit

class AxesLabelsMachine:
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
        self.name = Path(__file__).name.lower().removesuffix('.py')
    def determine_best_text_height(self):
        print('\naxis label machine.determine_best_text_height()\n')

    def generate_axes_labels_for_each_curve(self):
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            self.build_axes_labels(curve_object)

    def build_axes_labels(self,curve_object):
        curve_object.axis_label_object_time = TextLabel()
        curve_object.axis_label_object_height = TextLabel()
        curve_object.axis_label_object_depth = TextLabel()
        
        curve_object.axis_label_object_time.assign_parent_object(curve_object)
        curve_object.axis_label_object_height.assign_parent_object(curve_object)
        curve_object.axis_label_object_depth.assign_parent_object(curve_object)

        
        curve_object.axis_label_object_time.trk = TranslationKit()
        curve_object.axis_label_object_time.trk.translation_expression = "[0,0,-text_height-1*tick_size]"
        
        curve_object.axis_label_object_height.trk = TranslationKit()
        curve_object.axis_label_object_height.trk.translation_expression = "[-0.2*text_height,0,-0.2*text_height]"
        #curve_object.axis_label_object_time.trk.rotation_expression = None
        
        max_time = max(curve_object.dict_data_vectors_scaled["time"])
        max_height = max(curve_object.dict_data_vectors_scaled["height"])
        max_depth = max(curve_object.dict_data_vectors_scaled["depth"])
        curve_object.axis_label_object_time.run_with_details(label_type='axis_time_',
                                                parent_object=curve_object,
                                                text_string=curve_object.header_time,
                                                text_length = max_time)  # wrong text length  - you dont need this here it gets overwritten
        curve_object.axis_label_object_height.run_with_details(label_type='axis_height_',
                                                parent_object=curve_object,
                                                text_string=curve_object.header_height,
                                                text_length = max_height)
        curve_object.axis_label_object_depth.run_with_details(label_type='axis_depth_',
                                                parent_object=curve_object,
                                                text_string=curve_object.header_depth,
                                                text_length = max_depth)
