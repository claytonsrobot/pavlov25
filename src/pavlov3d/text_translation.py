'''
Title: text_translation.py (formerly translation_kit.py)
Author: Clayton Bennett
Created: 04 July 2024
Purpose:
Variable relationships can be assigned (at reasonable easy to find places) before the values themselves can be assigned (deep in the weeds)

Example:
In tick_numbering_machine, assign the translation vector values before they exist. 
They will exist once the character array point cloud exists, 
but before it is translated and packed, before it is then registered as a as chart elemenet which contributes to span. 

I like the word "kit" better than "pack". Either way, its meant to be a portable thing you can prepare for the journey ahead.

leverages eval()

object abbreviation: trk
'''
import numpy as np
from pavlov3d import arrayMath

class TranslationFinal:
    def final_group_label_translation_relative_to_scene_fence(group_object):
        # This deals with the height direction only
        # Where is the depth diretion managed?
        translation_vector = group_object.data_origin_relative_to_scene_data_origin # what has been done.
        #postive_height_of_group = group_object.scene_object.span_relative_to_self_data_origin[1][1] 
        negative_height_of_group = group_object.scene_object.span_relative_to_self_data_origin[1][0] # this is saying to please prepare to put the text outside of the scene fence
        # this translation should instead be handled in text_control_points.text_translate()
        # the dawn # blashemy
        if group_object.tier_level == 1:
            #vertical_change = postive_height_of_group+2*group_object.padding[1] # this is where the tier 1 group labels are set to float above, documented on 03 February 2025, written about a year prior 
            vertical_change = negative_height_of_group - 2*group_object.padding[1] # put tier 1 group labels under the scene
            # This should not be here. But it makes sense tht it's called after everything is set in?
            translation_vector = np.array([translation_vector[0],vertical_change,translation_vector[2]])
        elif group_object.tier_level == 2:
            #vertical_change = negative_height_of_group - 2*group_object.padding[1] # HACKY GARBAGE
            vertical_change = negative_height_of_group - 5*group_object.padding[1] # HACKY GARBAGE # put tier 2 group labels under the scene and under the tier 1 group labels
            translation_vector = np.array([translation_vector[0],vertical_change,translation_vector[2]])
        return translation_vector
    


class TextTranslationIntermediate:
    style_object = None

    @classmethod
    def assign_style_object(cls,style_object):
        cls.style_object = style_object 
    # these functions were historically in text_control_points.py - they were migrated here for the purpose of consolidating the arious text translation methods, with a hope for reducing complexity
    @classmethod
    def prepare_text(self):
        # buncha these are unused, big plans unlinked
        self.axis_label_size_coefficient = 0.3 #
        self.title_label_size_coefficient = 1.0
        self.textbox_size_coefficient = 1.0
        self.pre_title_buffer_coeff = 0.3 # used, here
        self.post_title_buffer_coeff = 0.2  
        self.pre_axis_label_buffer_coeff = 0#0.15
        self.post_axis_label_buffer_coeff = 0.1
        self.axisLabel_alignment = 'jerry' # 'center' # or 'left'  # you want jerry for president

    @classmethod
    def post_rotation_translation(self,characters_control_points_list,text_label_object):
        if text_label_object.label_type == 'title_':
            # do not supress  -they are using in evalutation the trk expression
            text_height = self.text_height_pre_rotation
            tick_size = self.style_object.tick_size
            try:
                
                expression = text_label_object.trk.translation_expression
                text_translation_vector = np.array(eval(expression)) # exmle: text_length,curve_object.max_height+ 2.0*text_height
                characters_control_points_list = self.text_translate(characters_control_points_list,text_translation_vector)
            except:
                print("post_rotation_translation()")
                False
                #print('This is the exploratory sizing run')
        
        elif text_label_object.label_type == 'axis_time_' or text_label_object.label_type == 'axis_height_':
            # do not supress  -they are using in evalutation the trk expression
            text_height = self.text_height_pre_rotation
            tick_size = self.style_object.tick_size
            expression = text_label_object.trk.translation_expression
            text_translation_vector = np.array(eval(expression))
            characters_control_points_list = self.text_translate(characters_control_points_list,text_translation_vector)
        #elif text_label_object.label_type == 'tick_numbering_time' or text_label_object.label_type == 'tick_numbering_height_' or text_label_object.label_type == 'tick_numbering_depth_': 
        elif 'tick_numbering_' in text_label_object.label_type:
            # do not supress  -they are using in evalutation the trk expression
            text_length = text_label_object.text_length_scaled # maybe this is correct
            text_height = self.text_height_pre_rotation
            max_height = text_label_object.parent_object.max_height
            max_depth = text_label_object.parent_object.max_depth
            curve_object = text_label_object.parent_object
            expression = text_label_object.trk.translation_expression

            #print(ex)
            text_translation_vector = np.array(eval(expression))
            characters_control_points_list = self.text_translate(characters_control_points_list,text_translation_vector)

        return characters_control_points_list
    
    # not until translation.check_and_wrap_supergroup() does this value properly exist: minimum_edge_at_zero_height_plane_relative_to_self_data_origin
    @classmethod
    def manage_group_wrap_translation(self,characters_control_points_list,minimum_edge_at_zero_height_plane_relative_to_self_data_origin):
        for i,character_controlPoints in enumerate(characters_control_points_list):
            characters_control_points_list[i] = character_controlPoints+minimum_edge_at_zero_height_plane_relative_to_self_data_origin
        return characters_control_points_list
    
    @classmethod
    def calculate_translation_vector(self,characters_control_points_list,text_label_object):

        # these values are relativve to standing unrotated letters

        active_object = text_label_object.parent_object

        current_phrase_max_height = arrayMath.determine_current_max_height(characters_control_points_list)
        #current_phrase_max_time = arrayMath.determine_current_max_time(characters_control_points_list)
        text_height = current_phrase_max_height
        text_label_object.text_height = text_height

        ''' should be informed by export_plugin, for each style''' 
        # this should incorporate all padding and centering
        #title_buffer = active_object.style_object.pre_title_buffer_coeff*text_height # fine
        title_buffer = self.pre_title_buffer_coeff*text_height # fine
        active_object.title_buffer_size = title_buffer
        #print(f"\nactive_object.name = {active_object.name}")
        #"print(f"active_object.title_height_placement = {active_object.title_height_placement}\n")
        if active_object.title_height_placement=='floating':
            translation_height_float = 1.0*active_object.max_height+title_buffer
        elif active_object.title_height_placement=='floor': 
            translation_height_float = 0
        #translation_height_padding = text_height # need to factor in tick size. How/where is minimum data overlap handled?
        translation_height_padding = active_object.title_buffer_size  # 20 April 2024

        if True:
            translation_height_padding = 0
            
        translation_height_data_overlap = 0
        translation_ticks = text_label_object.relevant_tick_length # pull this from text_label_object
        if self.axisLabel_alignment == 'center': # 
            translation_time = self.text_center_scalar(text_label_object,text_length_scaled = text_label_object.text_length_scaled)
        elif self.axisLabel_alignment == 'jerry': # 
            translation_time = self.text_jerry_scalar(text_label_object,text_length_scaled = text_label_object.text_length_scaled)
        elif self.axisLabel_alignment == 'left':
            translation_time = self.text_align_left() # returns 0

        translation_first_child_label_height = 0
        """ if active_object.type == 'group_object' or active_object.type == 'scene_object':
            #text_translation_vector = text_translation_vector + text_label_object.vector_text_origin_relative_to_parent_data_origin # [zeros]
            if active_object.first_child.type == 'group_object':
                translation_first_child_label_height = active_object.first_child.group_label_object.text_height
                text_label_object.translation_first_child_label_height = translation_first_child_label_height  """

        # you actually need to check all children, no tjust the first child, to see the depth sprawl - assuming that the group label is layed out in the depth direction
        # but, this is not the priority or the main issue. 

        translation_height = translation_first_child_label_height + translation_height_float + translation_height_padding + translation_height_data_overlap + translation_ticks
        translation_depth = 0 

        text_translation_vector = np.array([translation_time,translation_height,translation_depth])
        text_label_object.text_translation_vector = text_translation_vector

        return text_translation_vector
    
    @classmethod
    def manage_text_hang(self,characters_control_points_list,label_relative_to_axis_over_or_under):
        # mirror would be a misnomer: we don't want to mirror it, we want to translate it into the negative quadrant
        if label_relative_to_axis_over_or_under == 'under': 
            # characters_control_points_list only includeds the self.
            current_phrase_max_height = arrayMath.determine_current_max_height(characters_control_points_list)
            current_phrase_min_height = arrayMath.determine_current_min_height(characters_control_points_list)
            delta_height = 2*current_phrase_min_height + 1*current_phrase_max_height
            for i,character_controlPoints in enumerate(characters_control_points_list):
                characters_control_points_list[i] = self.text_hang_letter_over_original_time_axis(character_controlPoints,delta_height)
        else:
            True
        return characters_control_points_list
    @classmethod
    def text_hang_letter_over_original_time_axis(self,character_controlPoints,delta_height):
        character_controlPoints[:,1] = character_controlPoints[:,1] - delta_height
        return character_controlPoints

    @classmethod
    def text_translate(self,characters_control_points_list,text_translation_vector):
        # you should not be useing this: translation should be determined by a position vector, text_minimum_corner_origin_relative_to_curve_object_minimum_corner_origin
        # should be done before rotation
        for i,character_controlPoints in enumerate(characters_control_points_list):
            characters_control_points_list[i] = character_controlPoints+text_translation_vector
        return characters_control_points_list
    @classmethod
    def text_jerry_scalar(self,text_label_object,text_length_scaled):
        # not actually centered, not even close
        # _size_coefficient should be in text_scale() scaling, not here. The old way makes a parallel assumption about accuracy. Insted, just take what yo have and center it.
        # need to assess current scaled length in the time direction

        #translation_time = ((1.0-text_label_object.size_coefficient)/2)*text_label_object.text_length_unscaled # centered
        #translation_time = ((1.0-text_label_object.size_coefficient)/2)*text_label_object.text_length_scaled # centered
        translation_time = ((1.0-text_label_object.size_coeff)/2)*text_length_scaled # centered
        
        #translation_time = ((1.0-current_phrase_max_time)/2)*axis_length_time # centered
        return translation_time
    @classmethod
    def text_center_scalar_broken(self,text_label_object,text_length_scaled):
        # give a better name for _size_coefficient
        # _size_coefficient should be in text_scale() scaling, not here. The old way makes a parallel assumption about accuracy. Insted, just take what yo have and center it.
        # need to assess current scaled length in the time direction

        #translation_time = ((1.0-text_label_object.size_coefficient)/2)*text_label_object.text_length_unscaled # centered
        #translation_time = ((1.0-text_label_object.size_coefficient)/2)*text_label_object.text_length_scaled # centered
        percentage = 1
        if text_label_object.parent_object.type == 'curve_object':
            if text_label_object.label_type=='axis_height_':
                percentage = text_length_scaled/text_label_object.parent_object.max_height
            if text_label_object.label_type=='axis_depth_':
                percentage = text_length_scaled/text_label_object.parent_object.max_depth
            else:
                #print(f'text_label_object.parent_object.name = {text_label_object.parent_object.name}')
                percentage = text_length_scaled/text_label_object.parent_object.max_time# assumed axis length is time axis
        translation_time = ((1.0-percentage)/2)*text_length_scaled # centered
        
        #translation_time = ((1.0-current_phrase_max_time)/2)*axis_length_time # centered
        return translation_time
    @classmethod
    def text_align_left():
        return 0

class TranslationKit:
    def __init__(self):
        #self.text_height = None
        #self.text_length = None
        #self.translate_time = None
        #self.translate_height = None
        #self.translate_depth = None
        self.translation_vector = None
        self.translation_expression = str()
        self.rotation_expression = str()

if __name__ == '__main__':
    trk = TranslationKit()
    trk.translation_expression = "[-2*text_length,text_height+ max_height, 1/2*text_height]"

    text_length = 20
    text_height = 3
    max_height = 17
    translation_vector = np.array(eval(trk.translation_expression))
    print(f'translation_vector = {translation_vector}')