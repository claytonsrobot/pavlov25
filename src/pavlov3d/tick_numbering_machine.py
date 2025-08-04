'''
Title: tick_numbering_machine.py
Author: Clayton Bennett
Created: 03 July 2024

Purpose:
Span expansion and tick number labeling
Exploded view - with explosion translation occuring in creatFBX_

The explosion should be the diameter of the scene in the given direction.
'''
import os
#import chart_element
from src.pavlov3d.text_label import TextLabel as text_label_class
from src.pavlov3d.text_translation import TranslationKit

class TickNumberingMachine:

    scene_object=None
    style_object=None
    user_input_object=None
    hierarchy_object=None
    
    @classmethod
    def assign_scene_object_etc(cls, scene_object):
        cls.style_object = scene_object.style_object
        cls.scene_object = scene_object
        cls.user_input_object = scene_object.user_input_object
        cls.hierarchy_object = scene_object.hierarchy_object
        text_label_class.assign_class_variables(scene_object)

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py')

    def expand_span(self):
        #emulate existing
        True
    
    def run(self):
        True
        # emulate title machine
        self.style_object.text_height_minimum_for_curve_objects

    def generate_tick_numbering_for_all_five_ticks_on_an_axis(self): # call from ticks.py
        False

    def generate_tick_numbering_for_the_highest_value_axes_in_every_stack(self,text_height):
        False
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            title_object = self.build_title(curve_object,text_height)
            #print(f'title_object.name = {title_object.name}')
    
    def generate_tick_numbering_for_the_highest_value_on_all_three_axes_for_curves_with_a_max_dimension(self): # call from main.py
        self.repair_curve_object_max_min(curve_object)
        # which curve has the maximum time?
        # which curve has the maximum height?
        # which curve has the maximum depth?
        # add these to a set
        if self.style_object.createFBX_embed_tick_numbering_at_scene_level_or_curve_level_or_none is not None:
            superlative_curves = set()
            for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
                if round(self.scene_object.max_time,2) ==  round(curve_object.max_time,2): # rounding issues?
                    superlative_curves.add(curve_object)
                if round(self.scene_object.max_height,2) ==  round(curve_object.max_height,2): # rounding issues?
                    superlative_curves.add(curve_object)
                if round(self.scene_object.max_depth,2) ==  round(curve_object.max_depth,2): # rounding issues?
                    superlative_curves.add(curve_object)
            # i need to control where it manifests, relative to the data origin of the curve object
            for curve_object in superlative_curves:
                #self.build_tick_numbering_all(curve_object)

                # resgister these in a tick_numbering dictionary
                self.build_tick_numbering_height(curve_object)
                self.build_tick_numbering_time(curve_object)   
                if False: 
                    self.build_tick_numbering_depth(curve_object)
            # still no translation
    def generate_tick_numbering_for_all_curves(self): # call from main.py
        # which curve has the maximum time?
        # which curve has the maximum height?
        # which curve has the maximum depth?
        # add these to a set
        if self.style_object.createFBX_embed_tick_numbering_at_scene_level_or_curve_level_or_none is not None:
            superlative_curves = set()
            for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
                superlative_curves.add(curve_object)
            # i need to control where it manifests, relative to the data origin of the curve object
            for curve_object in superlative_curves:
                #self.build_tick_numbering_all(curve_object)

                # resgister these in a tick_numbering dictionary
                self.build_tick_numbering_height(curve_object)
                self.build_tick_numbering_time(curve_object)   

                self.build_tick_numbering_depth(curve_object)
            # still no translation

    def build_tick_numbering_all(self,curve_object):
        self.repair_curve_object_max_min(curve_object)

        curve_object.tick_numbering_object_time = text_label_class()
        curve_object.tick_numbering_object_height = text_label_class()
        curve_object.tick_numbering_object_depth = text_label_class()

        curve_object.tick_numbering_object_time.assign_parent_object(curve_object)
        curve_object.tick_numbering_object_height.assign_parent_object(curve_object)
        curve_object.tick_numbering_object_depth.assign_parent_object(curve_object)

        curve_object.tick_numbering_object_time.run_with_details(label_type='tick_numbering_time_',
                                                parent_object=curve_object,
                                                #text_string = str(round(curve_object.max_time,2)))
                                                text_string = str(round(max(curve_object.dict_data_vectors_raw["time"]),2)))
        
        curve_object.tick_numbering_object_height.run_with_details(label_type='tick_numbering_height_',
                                                parent_object=curve_object,
                                                #text_string = str(round(curve_object.max_height,2)))
                                                text_string = str(round(max(curve_object.dict_data_vectors_raw["height"]),2)))
        
        curve_object.tick_numbering_object_depth.run_with_details(label_type='tick_numbering_depth_',
                                                parent_object=curve_object,
                                                #text_string = str(round(curve_object.max_depth,2)))
                                                text_string = str(round(max(curve_object.dict_data_vectors_raw["depth"]),2)))
    
        return True
    
    def build_tick_numbering_time(self,curve_object):
        self.repair_curve_object_max_min(curve_object)
        
        curve_object.tick_numbering_object_time = text_label_class()

        curve_object.tick_numbering_object_time.assign_parent_object(curve_object)

        curve_object.tick_numbering_object_time.trk = TranslationKit() # use eval
        curve_object.tick_numbering_object_time.trk.translation_expression = "[curve_object.max_time+ 2.0*text_height,0,-2.9*text_length]"
        curve_object.tick_numbering_object_time.trk.translation_expression = "[curve_object.max_time+ 1.1*text_height,0,-0.0*text_length]"
        #curve_object.tick_numbering_object_time.trk.translation_expression = '[0,0,0]'
        curve_object.tick_numbering_object_time.trk.rotation_expression = "[0,0,270]"

        curve_object.tick_numbering_object_time.run_with_details(label_type='tick_numbering_time_',
                                                parent_object=curve_object,
                                                #text_string = str(round(curve_object.max_time,2)))
                                                text_string = str(round(max(curve_object.dict_data_vectors_raw["time"]),2)))
        return True

    def build_tick_numbering_height(self,curve_object):
        self.repair_curve_object_max_min(curve_object)
        curve_object.tick_numbering_object_height = text_label_class()

        curve_object.tick_numbering_object_height.assign_parent_object(curve_object)
        curve_object.tick_numbering_object_height.trk = TranslationKit() # use eval
        #curve_object.tick_numbering_object_height.trk.translation_expression = "[-2.5*text_length,-curve_object.max_height+ 0.5*text_height,0]"
        curve_object.tick_numbering_object_height.trk.translation_expression = "[-2.5*text_length,-curve_object.max_height+ 0.0*text_height,0]"
        curve_object.tick_numbering_object_height.trk.translation_expression = "[-2.5*text_length,curve_object.max_height+ 2.0*text_height,0]"
        curve_object.tick_numbering_object_height.trk.translation_expression = "[-0.0*text_length,curve_object.max_height+ 1.1*text_height,0]"
        #curve_object.tick_numbering_object_height.trk.translation_expression = '[0,0,0]'
        curve_object.tick_numbering_object_height.trk.rotation_expression = None
        # this can't happen erhe because text length and height arene't known yet, not until the character array is generated.
        # shove this in after te character array is generated. probbaly in text_label.py
        
        curve_object.tick_numbering_object_height.run_with_details(label_type='tick_numbering_height_',
                                                parent_object=curve_object,
                                                #text_string = str(round(curve_object.max_height,2)))
                                                text_string = str(round(max(curve_object.dict_data_vectors_raw["height"]),2)))
        
        return True
    
    def build_tick_numbering_depth(self,curve_object):

        curve_object.tick_numbering_object_depth = text_label_class()

        curve_object.tick_numbering_object_depth.assign_parent_object(curve_object)
        curve_object.tick_numbering_object_depth.trk = TranslationKit() # use eval
        
        curve_object.tick_numbering_object_depth.trk.translation_expression = "[-2.5*text_length,-0.0*text_length,curve_object.max_depth- 0.8*text_height]"
        curve_object.tick_numbering_object_depth.trk.translation_expression = "[-0.0*text_length,-0.0*text_length,curve_object.max_depth+ 0.1*text_height]"
        #curve_object.tick_numbering_object_depth.trk.translation_expression = '[0,0,0]'
        # wrong for depth  - the number should match the max height, due to scaling
        # the same goes for tick naming on in the depth diorection , for 2D height-copied-to-depth  
        curve_object.tick_numbering_object_depth.trk.rotation_expression = None
        
        curve_object.tick_numbering_object_depth.run_with_details(label_type='tick_numbering_depth_',
                                                parent_object=curve_object,
                                                #text_string = str(round(curve_object.max_depth,2)))
                                                text_string = str(round(max(curve_object.dict_data_vectors_raw["depth"]),2)))
    
        return True
    
    def repair_curve_object_max_min(self,curve_object):

            curve_object.max_time = max(curve_object.dict_data_vectors_scaled["time"])
            curve_object.min_time = min(curve_object.dict_data_vectors_scaled["time"])
            curve_object.max_height = max(curve_object.dict_data_vectors_scaled["height"])
            curve_object.min_height = min(curve_object.dict_data_vectors_scaled["height"])
            curve_object.max_depth = max(curve_object.dict_data_vectors_scaled["depth"])
            curve_object.min_depth = min(curve_object.dict_data_vectors_scaled["depth"])
            curve_object.min_data = [curve_object.min_time,curve_object.min_height,curve_object.min_depth]
