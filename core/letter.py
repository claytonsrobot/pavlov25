'''
Title: letter.py
Author: Clayton Bennett
Created: 11 March 2024
'''

class letter:
    def __init__(self,phrase_object):
        self.friendly_name = None
        self.next_letter_object = None
        self.phrase_object = phrase_object

    def assign_basic_information(self,friendly_name,next_letter_object):
        self.friendly_name = friendly_name
        self.next_letter_object = next_letter_object

    def assign_phrase_object(self,phrase_object):
        self.phrase_object = phrase_object
        #first_letter_object.friendly_name = None

    def assign_raw_character_controlPoints(self,character_controlPoints_matrix):
        self.character_controlPoints_matrix = character_controlPoints_matrix

