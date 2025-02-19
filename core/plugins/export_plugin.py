'''
Author: Clayton Bennett
Date Created: 18 July 2023, converted to plugin in mid February 2024
Old name: createFBX_triangleColumns # wow, artifact up in here
Purpose:
Apply basic flow of FBX generation and export,
to create a minimalist column style.

This is the where the export plugin object is instantiated and then the specific export plugin function is hosted by it.

08 February 2025 notes:
    Look, we were aiming for modularity here.
    But frankly text angle control isn't something I'm trying to offer my customers at this point.

    On 08 February 2025, curve_object.title_rotation_degrees_THD_CCWwas set to [45,0,0], compared to the long-standing [90,0,0] value.
    There reason for this was to allow  curve names to be visible from the front view as well as the top view.
    Before it was just the top, which happens to be the direction in which there is practically never a stack.
    This is not a coincident - If there is a depth stack, the now visible front view curve title will overlap.
    Which is unsightly, but it's more useful than not.

    Now I need to find where to compensate with the transaltion. So children, the lesson is, don't work too hard to offer control, and never develop the gui panel first.

    yo, this is the sarting place, and is handled by translaton kit now, in title_machine.py. What garbage.

Onward:
    Hold fast.
'''

import os
#from arrayMath import fbx4_convert
#import arrayMath

class ExportPlugin:
    style_object = None
    scene_object = None
    user_input_object = None

    @classmethod
    def assign_style_object(cls,style_object):
        cls.style_object=style_object

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py')
        self.point_size =2  
        #self.point_size = self.style_object.point_size
        self.set_axis_rotation_angles()
    
    def set_axis_rotation_angles(self):
        self.axis_rotation_degrees_THD_CCW_time = [45,0,0]
        self.axis_rotation_degrees_THD_CCW_height = [45,0,90]
        self.axis_rotation_degrees_THD_CCW_depth = [45,90,0]
        # these values are used in the translation kit evaluation
        # why? because they must be translated then have the rotation injected
        # take it up with the text creation code
        self.tick_numbering_rotation_degrees_THD_CCW_time = [0,0,0] 
        self.tick_numbering_rotation_degrees_THD_CCW_height = [90,90,0]
        self.tick_numbering_rotation_degrees_THD_CCW_depth = [0,90,90]

    def run_per_group(self,group_object):
        group_object.title_rotation_degrees_THD_CCW = [45,0,0]
        group_object.title_length = self.style_object.text_size_coeff*group_object.characteristic_length

    def run_per_curve(self,curve_object):
        curve_object.title_rotation_degrees_THD_CCW = [90,0,0] # long standing # yo, this is the sarting place, and is handled by translaton kit now, in title_machine.py. What garbage.
        #curve_object.title_rotation_degrees_THD_CCW = [45,0,0] # 08 February 2025  # actually never mind
        curve_object.title_length = self.style_object.text_size_coeff*curve_object.characteristic_length#characteristic_length=axis_length_list_THD[0], set in scene.build_groups

    # unused for now
    def determine_point_size(self):
        self.point_size = abs(self.style_object.scene_object.max_height - self.style_object.scene_object.min_height)/20
        #self.style_object.scene_object.average_halfwidth_time

        # there is a scaling thing here
        # It would be better to base it on average_halftime
        # how are vectorArray_time, and the other collections handled in scene_object? 
        # style_object.prepare_missing....etc

    # unused for now
    def metadata_assignment(self,datapoint_object):
        # uh
        # you can add more? Maybe from the dataObject
        # this is basic, not necessary, but interesting to see for dev, as an opportunity
        # can process it into text or whatever. currently still a df slice
        #metadata.UserProperties
        #DefaultAttributeIndex
        ###Pavlov_active.metadata_sandbox()
        # https://stackoverflow.com/questions/31327674/fbx-sdk-accessing-custom-attributes
        return datapoint_object.metadata

