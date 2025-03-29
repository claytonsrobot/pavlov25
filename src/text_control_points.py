'''
Author: Clayton Bennett
Created: 04 November 2023
Title: text_control_points.py

Purpose: Create title, to 80% the width of the time axis. Also, create a vertical title for the depth axis. Make vertical and horizontal both style choices. 
The reason vertical axis labels are the opposite direction from book titles is because the direction of the text should match the direction of the axis.

direction should be direction of axis? or blinking cursor axis? 

Items like coefficeint and length are not availbale from the method level as inputs, they are embedded intot he text_label
'''
import numpy as np
import math
import os
import sys
import inspect

from src.directories import Directories
from src.phrase import phrase as phrase_class
from src.letter import letter as letter_class
from src import arrayMath
from src import environmental
from pathlib import Path
from src.text_translation import TextTranslationIntermediate

script_dir = Directories.get_core_dir()
script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
directory = script_dir+'/alphanumeric_character_library'
directory = os.path.normpath(directory)

buffer = 10 # space between letters in the same word, svg html units
space = 40 # space between words, svg html units

class TextControlPointMachine:
    style_object = None
    @classmethod
    def assign_style_object(cls,style_object):
        cls.style_object = style_object
        cls.scene_object = style_object.scene_object

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py') 
        if environmental.pyinstaller()==True or environmental.pyinstaller()==False:
            self.dict_characters_raw = self.build_dict_characters_raw()

    def text_string_control_points(self,text_label_object,label_type):
        #active_object = text_label_object.parent_object # used in title.py, unused here (for now) 
        text_string = text_label_object.text_string
        text_label_object.phrase_object = phrase_class(friendly_name = text_string) # initialize
        #text_length = text_label_object.text_length
        text_string = text_string.upper()
        characters_name_list = []
        characters_control_points_list = []
        cursor_position=0

        letter_object = letter_class(phrase_object = text_label_object.phrase_object) # first one
        text_label_object.phrase_object.assign_first_letter(letter_object) # 
        # use direction_label_THD and direction_normal_THD. How to incorate? lke text_rotate,but different

        for character in text_string:
            if not(character == " "):   
                character_controlPoints,cursor_position = self.letter_controlPoints(character,cursor_position) # cursor position instead of "horizontal position" infers you can go whichever way, based on THD direction
                '''Please check the maximum and minimum of all characters'''
                #print(text_string)
                #print(character_controlPoints)
                #arrayMath.max_arrayMath(character_controlPoints)
                # the outputs are indeed reasonable
                character_name = 'char: '+str(character)+'_'
                letter_object_next = letter_class(phrase_object = text_label_object.phrase_object) # second one
                letter_object.assign_basic_information(friendly_name = character_name, next_letter_object = letter_object_next)
                letter_object.assign_phrase_object(phrase_object=text_label_object.phrase_object)
                letter_object.assign_raw_character_controlPoints(character_controlPoints)
                letter_object = letter_object_next
                text_label_object.phrase_object.add_letter_to_letter_dictionary(letter_object)
                characters_name_list.append(character_name) 
                characters_control_points_list.append(character_controlPoints)
            else:
                cursor_position = cursor_position+space 
        
        characters_control_points_list = self.text_phrase_scale_in_disassembled_form(text_label_object,characters_control_points_list,cursor_position)
        self.text_height_pre_rotation = self.determine_text_height(characters_control_points_list)
        TextTranslationIntermediate.text_height_pre_rotation = self.text_height_pre_rotation
        characters_control_points_list = self.text_phrase_translate_and_rotate_in_disassembled_form(characters_control_points_list,text_label_object,cursor_position)
        text_label_object.characters_control_points_list = characters_control_points_list # troubleshooting 
        #TextControlPointMachine.characters_control_points_list = characters_control_points_list # for troubleshooting
        characters_array = self.assemble_characters_array(label_type,characters_name_list,characters_control_points_list)
        text_label_object.phrase_object.assign_all_letters_array(characters_array)
        # you should already know text height by here! June 2024. The old ways shall not be forgotten.
        #text_height = abs(arrayMath.determine_current_max_height(characters_control_points_list)-arrayMath.determine_current_min_height(characters_control_points_list))
        #text_label_object.set_font_size(text_height)
        return characters_array,self.text_height_pre_rotation
    
    def determine_text_height(self,characters_control_points_list):
        text_height = abs(arrayMath.determine_current_max_height(characters_control_points_list)-arrayMath.determine_current_min_height(characters_control_points_list))
        return text_height
    
    def text_phrase_scale_in_disassembled_form(self,text_label_object,characters_control_points_list,cursor_position):
        # Each of these operations requires a disassembled state of the text "vector array"
        # At final assembly, .AddChild in createFBX_ is where the magic happens. 

        #print(f"characters_control_points_list = {characters_control_points_list}")
        #print(f"text_label_object.name = {text_label_object.name}")
        #print(f"cursor_position = {cursor_position}")
        characters_control_points_list,text_length_scaled = self.text_scale(characters_control_points_list,text_label_object,cursor_position)
        text_label_object.set_text_length_scaled(text_length_scaled)
        return characters_control_points_list
    
    def text_phrase_translate_and_rotate_in_disassembled_form(self,characters_control_points_list,text_label_object,cursor_position):
        # All three (scale, rotate ,translate) have to happen at the same time, because, you don't want to disassemble and reassemble repeatedly.
        # Each of these operations requires a disassembled state of the text "vector array"
        # At final assembly, .AddChild in createFBX_ is where the magic happens. 

        active_object = text_label_object.parent_object

        text_translation_vector = TextTranslationIntermediate.calculate_translation_vector(characters_control_points_list,text_label_object)
        #print(f"text_label_object.label_type = {text_label_object.label_type}")
        if 'tick_numbering_' not in text_label_object.label_type:
            characters_control_points_list = TextTranslationIntermediate.text_translate(characters_control_points_list,text_translation_vector) # over by 10% of max_time
        characters_control_points_list = TextTranslationIntermediate.manage_text_hang(characters_control_points_list,text_label_object.label_relative_to_axis_over_or_under)
        characters_control_points_list = self.text_rotate_collection_of_letters(characters_control_points_list,text_label_object.rot_deg_THD)
        characters_control_points_list = self.trk_rotation(characters_control_points_list,text_label_object)
        characters_control_points_list = TextTranslationIntermediate.post_rotation_translation(characters_control_points_list,text_label_object)
        # you can do this.....or you can open and re edit...
        if active_object.type == 'group_object': # this junt must hit 
            characters_control_points_list = TextTranslationIntermediate.manage_group_wrap_translation(characters_control_points_list,active_object.minimum_edge_at_zero_height_plane_relative_to_self_data_origin)

        # when you make changes here, how is the span of each curve ultimately informed?
        return characters_control_points_list
    
    def trk_rotation(self,characters_control_points_list,text_label_object):
        True
        if text_label_object.label_type == 'title_':
            try:
                expression = text_label_object.trk.rotation_expression
                text_rotation_vector = np.array(eval(expression))
                characters_control_points_list = self.text_rotate_collection_of_letters(characters_control_points_list,text_rotation_vector)
            except:
                print("trk_rotation()")
                pass # get better
        return characters_control_points_list
    
    
    def build_dict_characters_raw(self):
        self.dict_characters_raw = dict()
        
        script_dir = Path(getattr(sys,'_MEIPASS', Path.cwd()))
        alphanumeric_character_dir = Directories.get_core_dir()+"\\alphanumeric_character_library\\"
        #alphanumeric_character_dir = str(script_dir)+"\\alphanumeric_character_library\\"

        for filename in os.listdir(alphanumeric_character_dir):
            if filename.endswith('_svg.html'):
                raw_character = self.get_character_from_file(directory = alphanumeric_character_dir,filename = filename)
                character = filename.replace('_svg.html',"")
                self.dict_characters_raw[character]=raw_character
        return self.dict_characters_raw
    
    def get_character_from_file(self,directory,filename):    
            html_file = open(directory+filename,'r', encoding = 'utf-8') # no, wrong
            raw_character = html_file.read()
            return raw_character
    
    def get_character_from_preload(self,character):
        #print(f"character = {character}")
        try:
            raw_character = self.dict_characters_raw[character]
        except:
            print("\nCharacter dictionary key missing")
            print(f"character = {character}\n")
            raw_character = "char95_svg.html" # unknown_svg.html
        return raw_character

    def letter_controlPoints(self,character, cursor_position):
        #Control points for a single closed mesh that represents both orthogonal ticks
        #The control points need to be imported from the raw HTML SVG files, then converted based on direction

        character_swap_dictionary = {'*':'char42','+':'char43',',':'char44','-':'char45','.':'char46','/':'char47',
                                        ':':'char58',';':'char59','^':'char94','_':'char95','@':'char64'}
        if character in character_swap_dictionary:
            character = character_swap_dictionary[character] 

        if False:
            raw_character = self.get_character_from_file(filename = character+'_svg.html')
        else: 
            raw_character = self.get_character_from_preload(character)
        remainder = raw_character

        start_str = '<polyline'
        stop_str = 'style'
        start_idx = remainder.find(start_str)
        stop_idx = remainder.find(stop_str,start_idx+len(start_str))
        chunk = remainder[start_idx:stop_idx]

        start_str_data = 'points = "'
        start_idx_data = chunk.find(start_str_data)+len(start_str_data) 
        stop_idx_data = chunk.find('"',start_idx_data+len(start_str_data))
        chunk = chunk[start_idx_data:stop_idx_data]

        polyline = np.array(chunk.replace(' ',',').split(','),dtype=float).reshape(-1,2)
        x_list = polyline[:, 0]
        y_list = polyline[:, 1]
        y_list = (np.array(y_list)*-1)+100

        zero=0 
        character_controlPoints = []
        for i in range(len(x_list)):
            character_controlPoints.append([x_list[i]+cursor_position,y_list[i],zero])
        #character_controlPoints = np.matrix(character_controlPoints)
        character_controlPoints = np.array(character_controlPoints)
        cursor_position = cursor_position + max(x_list) + buffer
        
        return character_controlPoints,cursor_position # fed out as np.array values rather than np.matrix values....but whatever

    def text_scale(self,characters_control_points_list,text_label_object,cursor_position):
        if text_label_object.build_text_by_height is True:
            scale_by_length = False
            scale_by_height = True
        else:
            scale_by_length = True
            scale_by_height = False
        for i,character_controlPoints in enumerate(characters_control_points_list):
            #characters_control_points_list[i] = character_controlPoints*text_label_object.text_length_unscaled/cursor_position*text_label_object.size_coefficient
            #if text_label_object.text_length_target is None:

            if scale_by_length:
                characters_control_points_list[i] = character_controlPoints*text_label_object.text_length_target/cursor_position
                text_length_scaled = text_label_object.text_length_target
                #print(f'text_length_target = {text_label_object.text_length_target}')
            else:
                # text height last set where?
                text_height_unscaled = 100 # mirrored, from HTML SVG
                characters_control_points_list[i] = character_controlPoints*text_label_object.text_height/100
                text_length_scaled = (cursor_position/2)*text_label_object.text_height/100
                #print(f'text_label_object.text_height = {text_label_object.text_height}')
                #print(f'cursor_position = {cursor_position}')
                #print(f'text_length_scaled = {text_length_scaled}')
            #characters_control_points_list[i] = character_controlPoints*text_label_object.text_length_target/cursor_position*text_label_object.size_coefficient
            # wrong. does twice the scaling,m here, somehow
            #characters_control_points_list[i] = character_controlPoints*text_label_object.text_length/cursor_position*1.0 # still small
        if len(characters_control_points_list) != 0:
            return characters_control_points_list,text_length_scaled
        else:
            return None,None
    

    
    def text_rotate_collection_of_letters(self,characters_control_points_list,rot_deg_THD):
        for i,character_controlPoints in enumerate(characters_control_points_list):
            characters_control_points_list[i] = self.text_rotate_each_letter(character_controlPoints,rot_deg_THD) # title_rotation_degrees_THD_CCW
        return characters_control_points_list
    
    def text_rotate_each_letter(self,input_array,rot_deg_THD):

        # text_label_object.direction_label_THD needs to be considered
        # and text_label_object.direction_normal_THD 

        # Need to clarify direction standards
        # time_rotation twists like a wrist, like a hanging sign
        # height_rotation swings like a door
        # use T and H not D: y,x
        sin = math.sin
        cos = math.cos

        convert_deg2rad = lambda lst: [math.radians(x) for x in lst]
        rot_rad_THD = convert_deg2rad(rot_deg_THD)

        time_rotation = [[1, 0, 0],
                [0, cos(rot_rad_THD[0]), -sin(rot_rad_THD[0])],
                [0, sin(rot_rad_THD[0]), cos(rot_rad_THD[0])]] #T

        height_rotation = [[cos(rot_rad_THD[1]), 0, sin(rot_rad_THD[1])],
                [0,1,0],
                [-sin(rot_rad_THD[1]), 0, cos(rot_rad_THD[1])]] #H

        depth_rotation = [[cos(rot_rad_THD[2]), sin(rot_rad_THD[2]),0 ],
                [-sin(rot_rad_THD[2]),cos(rot_rad_THD[2]),0],
                [0, 0, 1]] #H 
        # negative on lowercosine causes time rotation of text to go the opposite way
        # negative on upper cosine causes entire 180 flip over the depth axis
        # negative on lower sine appeas to be correct
        # negative on upper sine mirrors 180 only the hiehgt axis. 45's vision-enabling-angles seem unimpacted
        # no negative leave the height axix label neading to be rotated another 90 degrees CCW (around the original time axis and current height axis, i.e. the base of the letters) to be 

        combined_rotation = np.matmul(time_rotation,height_rotation)
        combined_rotation = np.matmul(combined_rotation,depth_rotation) # try this, maybe don't need it
        output_array = np.dot(input_array,combined_rotation) # this is correct

        return output_array 

    def set_initial_text_direction(self,direction_label_THD = [1,0,0],direction_normal_THD = [0,0,1]):
        # take the raw character coordinates and rotate
        # different from text_rotate(), which alters the text relative to this initial setting 
        # direction_label_THD is the unit vector direction of the text progression, naturally read from left to right in the English languarge
        # direction_normal_THD is the unit vector direction that the text is read from, showing outwards from the page/screen, which oriented orthogonally
        nope=True
        direction_label_THD
        direction_normal_THD

    def set_text_label_caddy_corner_out_of_plane(self):
        # this will move the text such that  it will apear above its axis in one direection and below in another
        # to accomplish this, rotate about the middle of the text - thia must be done, before padding and translation
        not_yet=1

    def assemble_characters_array(self,label_type,characters_name_list,characters_control_points_list):
        # This builds the characters_array / lines_array, which will ultimately be unpacked and build as FBX lines by lines_FBX.py, called in in create_FBX_.py

        characters_array = []
        super_flag = [label_type,None] # this takes the label_type and enters it as the parent of the enclosed constituent lines into the complete hierarchy

        characters_array.append(super_flag) # this is a hack: must go after the region assignment in order to dictate the node hierarchy in GLB output
        
        for i,character_name in enumerate(characters_name_list):
            character_controlPoints = characters_control_points_list[i]
            character_array = [character_name,character_controlPoints]
            characters_array.append(character_array)
        characters_array.append([None,None]) # step out a level

        '''
        texts_arrays[0][1][1]
        you can reference a data_matrix like this
        '''
        return characters_array

    def diassemle_characters_array_point_cloud(characters_array):
        characters_control_points_list = []
        for i in characters_array:
            for j in i:
                if isinstance(j,np.array()):
                    characters_control_points_list.append(j)
        return characters_control_points_list