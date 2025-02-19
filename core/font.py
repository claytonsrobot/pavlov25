'''
Title: font.py
Author: Clayton Bennett
Created: 09 June 2024
'''

def find_minimum_font(scene_object):
    # initialize the min_characteristic_length variable, with the first value 
    curve_object = scene_object.curve_objects_all.values()[0]
    min_characteristic_length = curve_object.characteristic_length

    # cycle thrugh all curves to check for smaller characteristic langth
    for curve_object in scene_object.curve_objects_all.values():
        if curve_object.characteristic_length < min_characteristic_length: 
            min_characteristic_length = curve_object.characteristic_length

    #bitch, it's about height, not length
    return min_characteristic_length

def set_all_fonts_to_minimum_scene_font(scene_object,font_height):
    for curve_object in scene_object.curve_objects_all.values(): 
            curve_object.font_height = font_height 




