'''
Title: stack.py
Author: Clayton Bennett
Created: 29 June 2024

Purpose: Stack control for translation, namely for grandfather and great grandfather cousin alignment
'''
import numpy as np
import logging

class StackControl:
    def __init__(self):
        True

    @staticmethod
    def primary_stack(active_object):
        
        active_object.data_origin_relative_to_previous_sibling_data_origin = np.multiply(active_object.tier_object.stack_vector,
                                                                                np.array(active_object.previous_sibling.maximum_corner_origin_relative_to_data_origin+\
                                                                                        active_object.supergroup.padding+\
                                                                                        active_object.data_origin_relative_to_self_minimum_corner_origin))
        #print(f"stack.primary_stack()")
        #print(f"active_object.data_origin_relative_to_previous_sibling_data_origin = {active_object.data_origin_relative_to_previous_sibling_data_origin}")
        return active_object.data_origin_relative_to_previous_sibling_data_origin
    
    @staticmethod
    def secondary_stack_shared_grandfather(active_object):
        #print("stack.secondary_stack_shared_grandfather()")
        #print(f"active_object.name: {active_object.name}")
        # broken when style_object.group_padding_supressed == False. Good when true.
        """ arms_length_3D_sibling_to_sibling = np.array(\
                                active_object.previous_sibling.maximum_corner_origin_relative_to_data_origin\
                                + active_object.supergroup.padding\
                                + active_object.data_origin_relative_to_self_minimum_corner_origin\
                                )
        active_object.data_origin_relative_to_previous_sibling_data_origin = np.multiply(active_object.tier_object.stack_vector,
                                                                                        arms_length_3D_sibling_to_sibling) """
        
        #active_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_corner_origin_T = 0
        active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_T = active_object.span_relative_to_self_data_origin[0][0]
        active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_H = active_object.span_relative_to_self_data_origin[1][0]
        active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_D = active_object.span_relative_to_self_data_origin[2][0]

        #print(f'active_object.name = {active_object.name}')
        active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_T = active_object.previous_sibling.span_relative_to_self_data_origin[0][1]
        active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_H = active_object.previous_sibling.span_relative_to_self_data_origin[1][1]
        active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_D = active_object.previous_sibling.span_relative_to_self_data_origin[2][1]
        try:
            #active_object.grandfather_place_cousins
            active_object.cousins_extended.values()
            #print(f'active_object.grandfather_place_cousins = {active_object.grandfather_place_cousins}')
        except Exception:
            logging.exception('\nLikely: Missing valid tier 1 group for some curve.\n')
        #for cousin in active_object.grandfather_place_cousins.values():
        
        for cousin in active_object.cousins_extended.values(): # .grandfather_place_cousins values are set in scene.py
            if cousin.span_relative_to_self_data_origin[0][0] < active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_T:
                active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_T = cousin.span_relative_to_self_data_origin[0][0]
            if cousin.span_relative_to_self_data_origin[1][0] < active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_H:
                active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_H = cousin.span_relative_to_self_data_origin[1][0]
            if cousin.span_relative_to_self_data_origin[2][0] < active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_D:
                active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_D = cousin.span_relative_to_self_data_origin[2][0]
            
        #for cousin in active_object.previous_sibling.grandfather_place_cousins:
        for cousin in active_object.previous_sibling.cousins_extended.values():
            if cousin.span_relative_to_self_data_origin[0][1] > active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_T:
                active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_T = cousin.span_relative_to_self_data_origin[0][1]
            if cousin.span_relative_to_self_data_origin[1][1] > active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_H:
                active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_H = cousin.span_relative_to_self_data_origin[1][1]
            if cousin.span_relative_to_self_data_origin[2][1] > active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_D:
                active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_D = cousin.span_relative_to_self_data_origin[2][1]
        
        active_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_T = np.multiply(-1,active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_T)
        active_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_H = np.multiply(-1,active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_H)
        active_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_D = np.multiply(-1,active_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_D)

        active_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_corner_origin = np.array([\
            active_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_T,
            active_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_H,
            active_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_D])
        
        active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin = np.array([\
            active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_T,
            active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_H,
            active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_D])

        arms_length_3D_sibling_to_sibling_with_previous_and_current_cousin_flight = np.array(\
                                active_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin\
                                + active_object.supergroup.padding\
                                + active_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_corner_origin\
                                )

        active_object.data_origin_relative_to_previous_sibling_data_origin = np.multiply(active_object.tier_object.stack_vector,
                                                                                                        arms_length_3D_sibling_to_sibling_with_previous_and_current_cousin_flight)
        
        #print(f"stack.secondary_stack_shared_grandfather()")
        #print(f"active_object.data_origin_relative_to_previous_sibling_data_origin = {active_object.data_origin_relative_to_previous_sibling_data_origin}")
        return active_object.data_origin_relative_to_previous_sibling_data_origin

    
    def subgroup_secondary_stack_shared_grandfather(self,subgroup_object):
        # broken when style_object.group_padding_supressed == False. Good when true.
        """ arms_length_3D_sibling_to_sibling = np.array(\
                                active_object.previous_sibling.maximum_corner_origin_relative_to_data_origin\
                                + active_object.supergroup.padding\
                                + active_object.data_origin_relative_to_self_minimum_corner_origin\
                                )
        active_object.data_origin_relative_to_previous_sibling_data_origin = np.multiply(active_object.tier_object.stack_vector,
                                                                                        arms_length_3D_sibling_to_sibling) """
        
        #subgroup_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_corner_origin_T = 0
        subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_T = subgroup_object.span_relative_to_self_data_origin[0][0]
        subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_H = subgroup_object.span_relative_to_self_data_origin[1][0]
        subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_D = subgroup_object.span_relative_to_self_data_origin[2][0]

        subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_T = subgroup_object.previous_sibling.span_relative_to_self_data_origin[0][1]
        subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_H = subgroup_object.previous_sibling.span_relative_to_self_data_origin[1][1]
        subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_D = subgroup_object.previous_sibling.span_relative_to_self_data_origin[2][1]
        try:
            subgroup_object.grandfather_place_cousins
            #print(f'subgroup_object.grandfather_place_cousins = {subgroup_object.grandfather_place_cousins}')
        except Exception:
            logging.exception('\nLikely: Missing valid tier 1 group for some curve.\n')
        
        for cousin in subgroup_object.grandfather_place_cousins.values(): # .grandfather_place_cousins values are set in scene.py
            #print(f'cousin = {cousin.name}')
            #try:
            
            if cousin.span_relative_to_self_data_origin[0][0] < subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_T:
                subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_T = cousin.span_relative_to_self_data_origin[0][0]
            if cousin.span_relative_to_self_data_origin[1][0] < subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_H:
                subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_H = cousin.span_relative_to_self_data_origin[1][0]
            if cousin.span_relative_to_self_data_origin[2][0] < subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_D:
                subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_D = cousin.span_relative_to_self_data_origin[2][0]
            #except:
            #    False
            #print('cousin_group_not_yet_wrapped: problem')
            # which direction are the stacked relative to each other
            # actually, you should be able to wrap these first, before the subgroup data origin relative to its supergroup is set (for subgroups where place_in_supergroup is not 0)
        for cousin in subgroup_object.previous_sibling.grandfather_place_cousins.values():
            #try:
            if cousin.span_relative_to_self_data_origin[0][1] > subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_T:
                subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_T = cousin.span_relative_to_self_data_origin[0][1]
            if cousin.span_relative_to_self_data_origin[1][1] > subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_H:
                subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_H = cousin.span_relative_to_self_data_origin[1][1]
            if cousin.span_relative_to_self_data_origin[2][1] > subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_D:
                subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_D = cousin.span_relative_to_self_data_origin[2][1]
            #except:
            #False
            #print('cousin_group_not_yet_wrapped: problem')
        subgroup_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_T = np.multiply(-1,subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_T)
        subgroup_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_H = np.multiply(-1,subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_H)
        subgroup_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_D = np.multiply(-1,subgroup_object.grandfather_place_cousins__minimum_corner_origin_relative_to_self_data_origin_D)

        subgroup_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_corner_origin = np.array([\
            subgroup_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_T,
            subgroup_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_H,
            subgroup_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_D])
        
        subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin = np.array([\
            subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_T,
            subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_H,
            subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin_D])

        arms_length_3D_sibling_to_sibling_with_previous_and_current_cousin_flight = np.array(\
                                subgroup_object.previous_sibling.grandfather_place_cousins__maximum_corner_origin_relative_to_data_origin\
                                + subgroup_object.supergroup.padding\
                                + subgroup_object.grandfather_place_cousins__data_origin_relative_to_self_minimum_corner_origin\
                                )

        subgroup_object.data_origin_relative_to_previous_sibling_data_origin = np.multiply(subgroup_object.tier_object.stack_vector,
                                                                                                        arms_length_3D_sibling_to_sibling_with_previous_and_current_cousin_flight)
        #print(f"\nstack.subgroup_secondary_stack_shared_grandfather()")
        #print(f"subgroup_object.data_origin_relative_to_previous_sibling_data_origin = {subgroup_object.data_origin_relative_to_previous_sibling_data_origin}")
        return subgroup_object.data_origin_relative_to_previous_sibling_data_origin
    
    def check_for_diagonal_supergroup_and_diagonal_supergroup_supergroup(self,active_object):

        #print(f'If a cellhive were used, with intersection addresses,this would not be necessary, to check for narrative')

        bool_super_pointless_groups_diagonal = all(active_object.hierarchy_object.dict_tier_objects[1].stack_vector == np.array([1,0,1])) # if all diagonal
        bool_super_pointless_subgroups_diagonal = all(active_object.hierarchy_object.dict_tier_objects[2].stack_vector == np.array([1,0,1]))
        bool_secondary_alignment_is_pointless_all_diagonal_stacks = bool_super_pointless_groups_diagonal and bool_super_pointless_subgroups_diagonal

        bool_super_pointless_groups_diagonal = all(active_object.hierarchy_object.dict_tier_objects[1].stack_vector == np.array([1,0,1])) # if all diagonal
        bool_super_pointless_subgroups_diagonal = all(active_object.hierarchy_object.dict_tier_objects[2].stack_vector == np.array([1,0,1]))
        
        first_stack_same_as_second_stack = all(active_object.hierarchy_object.dict_tier_objects[1].stack_vector == active_object.hierarchy_object.dict_tier_objects[2].stack_vector)
        first_stack_same_as_third_stack = all(active_object.hierarchy_object.dict_tier_objects[1].stack_vector == active_object.hierarchy_object.dict_tier_objects[3].stack_vector)
        bool_secondary_alignment_is_pointless_all_same_stacks = first_stack_same_as_second_stack and first_stack_same_as_third_stack
        #print(f'bool_secondary_alignment_is_pointless_all_same_stacks = {bool_secondary_alignment_is_pointless_all_same_stacks}')
        bool_secondary_alignment_is_pointless = bool_secondary_alignment_is_pointless_all_diagonal_stacks or bool_secondary_alignment_is_pointless_all_same_stacks
        #print(f"bool_secondary_alignment_is_pointless = {bool_secondary_alignment_is_pointless}")
        return bool_secondary_alignment_is_pointless