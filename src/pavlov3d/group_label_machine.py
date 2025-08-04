'''
Author: Clayton Bennett
Created: 06 March 2024
Title: group_label_machine.py

If this is run from main, it infers that everything need not be known at curve_object instantiation. Ergo, there needs to be an expansion method.
Or, the middle road is that the driving characterstics of title are known, so that the dimensions are known before it is built. But that sounds risky.
'''
#translation_expression not found here

import os
from src.pavlov3d.text_label import TextLabel
class GroupLabelMachine:
    scene_object=None
    style_object=None
    user_input_object=None
    
    @classmethod
    def assign_scene_object_etc(cls, scene_object):
        cls.style_object = scene_object.style_object
        cls.scene_object = scene_object
        cls.user_input_object = scene_object.user_input_object
        TextLabel.assign_class_variables(scene_object)

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py')
        
    def generate_group_label_for_each_group(self):
        #for group_object in reversed(self.hierarchy_object.dict_group_objects_all.values()):
        for group_object in reversed(self.hierarchy_object.dict_group_objects_most.values()):
            #if group_object.type!='scene_object':
            #    self.add_group_label(group_object)
            self.add_group_label(group_object)
        print(f'span of group fence does not need to be the same as the group span')
        print(f'span of group fence does not need include the label')
        print(f'calculate the fence span before adding the label, and then calulate it again after, if a boolean in settings says so.')
        print(f'or use a setting flag, rather than a boolean')

    def add_group_label(self, group_object):
        #group_object.dict_text_labels = dict() # Assuming these are the first group labels created
        group_object.group_label_object = TextLabel()
        #try:
        
        group_object.group_label_object = group_object.group_label_object.run_with_details(label_type='group_label_',
                                                        parent_object=group_object,
                                                        text_string=group_object.simple_name,
                                                        text_length = group_object.title_length)
        ##except Exception: 
        ##    print(f'If this fails, it is likely because a provided group names matches a provided subgroup name.')
        #text_length = group_object.max_time
