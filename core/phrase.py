'''
Title: phrase.py
Author: Clayton Bennett
Created: 11 March 2024
'''
from collections import OrderedDict
class phrase:
    def __init__(self,friendly_name):
        self.friendly_name = friendly_name
        self.first_letter = None
        self.all_letters_array = None # assign as the complete characters_control_points_list
        self.all_letters_dict = OrderedDict()

    def assign_first_letter(self,letter_object):
        self.first_letter = letter_object
        self.add_letter_to_letter_dictionary(letter_object)
        #first_letter_object.friendly_name = None
    
    # should we use a dictionary of letters? Or just let each letter refer to the next? both?
    def add_letter_to_letter_dictionary(self,letter_object):
        self.all_letters_dict.update({letter_object.friendly_name:letter_object}) # will this be an ordered dictionary?

    def assign_all_letters_array(self,characters_control_points_list):
        self.all_letters_array = characters_control_points_list
    