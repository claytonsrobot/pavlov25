'''
Title: translation.py
Created: 24 January 2024, taken from other existing code
Author: Clayton Bennett

Purpose: Generalize translation methods shared by scene_object, group_objects, and curve_objects

Runs in the proper order because it is called by the defactor order-caller in scene.step_through_hierarchy()

Buffer and diameter interact innaccurately somewhere.
Add data origin to every group_object. At the height and depth perimeter of the first child, at shared 0 height.

Sections: 
1) Bottom Up Code
2) Top Down Code

Assumptions:
The data origin of a group is equivalent to the data origin of its first child.
'''
import numpy as np
import copy
import logging # active_object.grandfather_place_cousins

from group_label_machine import GroupLabelMachine
from stack import StackControl
stackcontrol_object = StackControl()

'''Start Bottom Up Code'''
def calculate_placement_bottom_up(active_object):
    #print(f"transation.calculate_placement_bottom_up(): active_object.name = {active_object.name}")
    # called in main after all elements have been generated (and thus diameters, point clouds, and rotation of elements will not change)
    if active_object.type == 'curve_object':
        calculate_curve_object_minimum_edge_at_zero_height_plane(active_object)
        calculate_data_retaining_origins_bottom_up_zero_plane_only(active_object) #chezest13506
        wrap_curve_span(active_object)
        check_and_wrap_supergroup(active_object)   

    elif active_object.type == 'group_object':
        calculate_data_retaining_origins_bottom_up_zero_plane_only(active_object)
        check_and_wrap_supergroup(active_object) # wrap the scene_object      

    elif active_object.type == 'scene_object':   
        without_text(active_object)
    
def calculate_curve_object_minimum_edge_at_zero_height_plane(active_object):# really only applies to curve_object, unless things change
    active_object.minimum_edge_at_zero_height_plane_relative_to_self_minimum_corner_origin = [0,
                                                                                                active_object.data_origin_relative_to_self_minimum_corner_origin[1],
                                                                                                0]
    active_object.minimum_corner_origin_relative_to_self_minimum_edge_at_zero_height_plane = np.multiply(-1,active_object.minimum_edge_at_zero_height_plane_relative_to_self_minimum_corner_origin)

    # preexisting calculations in curves.set_minimum_edge_at_zero_height_plane_relative_to_self_data_origin()


def calculate_data_retaining_origins_bottom_up_zero_plane_only(active_object):#28Jannuary2024

    intermediate_wrap(active_object)

    #if active_object.place_in_supergroup == 0 
    bool_secondary_alignment_is_pointless = stackcontrol_object.check_for_diagonal_supergroup_and_diagonal_supergroup_supergroup(active_object)

    if active_object.place_in_supergroup == 0:
        condition_met = True
        #if active_object.place_in_supergroup == 0 or bool_secondary_alignment_is_pointless:
        #if active_object.place_in_supergroup == 0 and (active_object.supergroup.place_in_supergroup == 0 or active_object.supergroup.supergroup.place_in_supergroup == 0): # this won't really work anymore, for seconary alighnment. The 
        if False: #test #undo
            active_object.data_origin_relative_to_previous_sibling_data_origin = None # no previous sibling
        active_object.data_origin_relative_to_supergroup_data_origin = np.array([0,0,0])
        active_object.data_origin_relative_to_first_sibling_data_origin = np.array([0,0,0]) # it is its own first sibling
        active_object.span_relative_to_first_sibling_data_origin = active_object.span_relative_to_self_data_origin # it is its own first sibling
        # it is its own first sibling    
        #print(f"active_object.data_origin_relative_to_supergroup_data_origin = {active_object.data_origin_relative_to_supergroup_data_origin}")

    else:
        condition_met = True
        #elif active_object.place_in_supergroup > 0:
        # a child that is not the first child

        active_object.previous_sibling.maximum_corner_origin_relative_to_data_origin = np.array([active_object.previous_sibling.span_relative_to_self_data_origin[0][1],active_object.previous_sibling.span_relative_to_self_data_origin[1][1],active_object.previous_sibling.span_relative_to_self_data_origin[2][1]])
        
        # at this point, add alternative data_origin_relative_to_previous_sibling_data_origin, to allow for alignment of secondary siblings
        # ....might have to chnage order, each  
        # iterate over place in supergroup
        '''NEXT! Data sligned all cousins, rather than sibling direct stacking. Leave option.'''
        # or! we do an after the fact adjustment, rather than a restart
        

        ## should include a call to style for choice between grantfather and greatgranfather cousining
        if bool_secondary_alignment_is_pointless:
            active_object.data_origin_relative_to_previous_sibling_data_origin = stackcontrol_object.primary_stack(active_object)
        else:
            if active_object.type=='curve_object': #active_object.tier_object.tier_level == 3
                #if active_object.hierarchy_object.dict_tier_objects[1].stack_vector[2]==0: # if the variety level (tier 1, sub scene 0 tier) is not depth stacked, then ignore the need for greatgratherfather cousin matching 
                active_object.data_origin_relative_to_previous_sibling_data_origin = stackcontrol_object.secondary_stack_shared_grandfather(active_object)
                
            elif active_object.tier_object.tier_level == 2:
                
                # suppressed:
                active_object.data_origin_relative_to_previous_sibling_data_origin = stackcontrol_object.subgroup_secondary_stack_shared_grandfather(active_object)
            else: # work to include higher eschelons for greatgrantfather_mate_cousins
                    active_object.data_origin_relative_to_previous_sibling_data_origin = stackcontrol_object.primary_stack(active_object)
            

        try:
            # this code is failing to run for the previous sibling
            active_object.data_origin_relative_to_supergroup_data_origin = active_object.previous_sibling.data_origin_relative_to_supergroup_data_origin\
                                                                    + active_object.data_origin_relative_to_previous_sibling_data_origin
        except Exception as e:
            print(f"active_object.name = {active_object.name}")
            print("IF YOU ERROR HERE IT IS LIKELY BECAUSE YOUR SUBGROUPS ARE NON-EXCLUSIVE MAJOR BUG")
            active_object.data_origin_relative_to_supergroup_data_origin = active_object.previous_sibling.data_origin_relative_to_supergroup_data_origin\
                                                                    + active_object.data_origin_relative_to_previous_sibling_data_origin
        active_object.data_origin_relative_to_first_sibling_data_origin = active_object.data_origin_relative_to_supergroup_data_origin

        # this is the most important part of calculating supergroup span
        #print(f'active_object.span_relative_to_self_data_origin = {active_object.span_relative_to_self_data_origin}')
        #   print(f'active_object.data_origin_relative_to_first_sibling_data_origin = {active_object.data_origin_relative_to_first_sibling_data_origin}')
    
    if condition_met == True:
        active_object.span_relative_to_first_sibling_data_origin  =  active_object.span_relative_to_self_data_origin\
                                        + np.transpose([active_object.data_origin_relative_to_first_sibling_data_origin,
                                        active_object.data_origin_relative_to_first_sibling_data_origin])
        


        
def wrap_curve_span(curve_object):
    if curve_object.type == 'curve_object':# not adding text, embedded
        curve_object.span_relative_to_self_minimum_edge_at_zero_height_plane = np.array([[0,curve_object.diameter[0]],
                                                                            [curve_object.minimum_corner_origin_relative_to_self_minimum_edge_at_zero_height_plane[1],curve_object.diameter[1]+curve_object.minimum_corner_origin_relative_to_self_minimum_edge_at_zero_height_plane[1]],
                                                                            [0,curve_object.diameter[2]]])

def add_padding_to_supergroup(active_object):
    return active_object.supergroup.update_group_span_based_on_padding(active_object.supergroup.span_relative_to_self_data_origin)
    

def without_text(active_object):
    active_object.data_origin_relative_to_self_minimum_edge_at_zero_height_plane = np.multiply(-1,\
                                                                                        np.array([active_object.span_relative_to_self_minimum_edge_at_zero_height_plane[0][0],\
                                                                                        0,\
                                                                                        active_object.span_relative_to_self_minimum_edge_at_zero_height_plane[2][0]])\
                                                                                    )
def check_and_wrap_supergroup(active_object): 
    #print(f"\ntranslation.check_and_wrap_supergroup()")
    #print(f"active_object.place_in_supergroup = {active_object.place_in_supergroup}") 
    if active_object.place_in_supergroup == len(list(active_object.supergroup.dict_children.keys()))-1:#last item
        # the last subgroup, i.e. diameter can be known
        # the diameter of the lower subgroups would of course have to be known at this point
        # this will become a problem if children are ever a mix of curve_objects and group_objects, which it should not be
        

        # use: active_object.span_relative_to_first_sibling_data_origin
        # ASSIGNMENT OF #span_relative_to_self_data_origin
        active_object.supergroup.span_relative_to_self_data_origin = check_children_span_relative_to_first_sibling_data_origin(active_object.supergroup)
        # this is the magic right here. Be explicit.
        intermediate_wrap(active_object.supergroup)
        # label time, let's go baby
        # label, then wrap

        if active_object.supergroup.type=='group_object':
            active_object.supergroup.span_relative_to_self_data_origin_without_text_label = copy.deepcopy(active_object.supergroup.span_relative_to_self_data_origin)
            
            group_label_machine = GroupLabelMachine() # this should be somewhere else, like main
            group_label_machine.add_group_label(group_object=active_object.supergroup)
            
            active_object.supergroup.span_relative_to_self_data_origin = check_group_label_span_relative_to_first_sibling_data_origin(active_object.supergroup)

        intermediate_wrap(active_object.supergroup)
        _set_supergroup_diameter(active_object.supergroup) 
        ##minimum_edge_at_zero_height_plane_relative_to_self_data_origin
        # once expanded, you don't really need the group data origin anymore?
        active_object.supergroup.minimum_corner_origin_relative_to_self_minimum_edge_at_zero_height_plane = np.array([0,
                                                                                                                        active_object.supergroup.span_relative_to_self_data_origin[1][0],
                                                                                                                        0]) # needs to be calculated again if you expand the supergroup text stage 2

        active_object.supergroup.span_relative_to_self_minimum_edge_at_zero_height_plane =\
            np.array([[0,active_object.supergroup.diameter[0]],
                        [active_object.supergroup.minimum_corner_origin_relative_to_self_minimum_edge_at_zero_height_plane[1],\
                        active_object.supergroup.diameter[1]+active_object.supergroup.minimum_corner_origin_relative_to_self_minimum_edge_at_zero_height_plane[1]],\
                        [0,active_object.supergroup.diameter[2]]])
        if active_object.supergroup.type =='group_object':
            
            active_object.supergroup.span_relative_to_self_data_origin = add_padding_to_supergroup(active_object)
    else:
        pass
        #print(f"\nactive_object.name:{active_object.name}")
        #print(f"active_object.place_in_supergroup:{active_object.place_in_supergroup}")
        #print(f"len(list(active_object.supergroup.dict_children.keys())) = {len(list(active_object.supergroup.dict_children.keys()))}")
        #print("end:else\n")



def _set_supergroup_diameter(supergroup):
    # this is only called (and only works properly) if you're looking at the last object in a group
    #print(f'active_object.name = {active_object.name}')
    #print(f'active_object.diameter = {active_object.diameter}')
    
    # why are all of these necessary, especially if youre talking about the last child, not the super group?
    #active_object.minimum_corner_origin_relative_to_self_data_origin = np.multiply(1,[active_object.span_relative_to_self_data_origin[0][0],active_object.span_relative_to_self_data_origin[1][0],active_object.span_relative_to_self_data_origin[2][0]])
    #active_object.minimum_corner_origin_relative_to_self_minimum_edge_at_zero_height_plane = np.array([0,active_object.minimum_corner_origin_relative_to_self_data_origin[1],0])

    diameter = np.array([supergroup.span_relative_to_self_data_origin[0][1]-supergroup.span_relative_to_self_data_origin[0][0],
                        supergroup.span_relative_to_self_data_origin[1][1]-supergroup.span_relative_to_self_data_origin[1][0],
                        supergroup.span_relative_to_self_data_origin[2][1]-supergroup.span_relative_to_self_data_origin[2][0]])

    supergroup.set_diameter(diameter) 

# if this all gets fucked, dial back to version 18-19/4/2024
def check_children_span_relative_to_first_sibling_data_origin(group_object):
    
    #group_object.span_relative_to_self_data_origin = copy.deepcopy(group_object.first_child.span_relative_to_self_data_origin)
    span_relative_to_self_data_origin = copy.deepcopy(group_object.first_child.span_relative_to_self_data_origin)
    # intialize, then stretch
    if group_object.first_child.type == 'curve_object' or group_object.first_child.type == 'group_object':#as opposed to what...
        for child in group_object.dict_children.values():
            child.span_relative_to_first_sibling_data_origin
            for i in range(3):     
                if child.span_relative_to_first_sibling_data_origin[i][0] < span_relative_to_self_data_origin[i][0]:
                    span_relative_to_self_data_origin[i][0] = child.span_relative_to_first_sibling_data_origin[i][0]
                if child.span_relative_to_first_sibling_data_origin[i][1] > span_relative_to_self_data_origin[i][1]:
                    span_relative_to_self_data_origin[i][1] = child.span_relative_to_first_sibling_data_origin[i][1]
    else:
        print("\nPlease remove this if statement? translation.check_children_span_relative_to_first_sibling_data_origin()\n")
    
    #print(f'group_object.span_relative_to_self_data_origin = {group_object.span_relative_to_self_data_origin}')
    #return np.array(group_object.span_relative_to_self_data_origin)
    return np.array(span_relative_to_self_data_origin)

def check_group_label_span_relative_to_first_sibling_data_origin(group_object):

    # the dawn
    # relate back the current minium edge at zero height span (which will not be retained) to the current data origin (which will be retained)
    # this way, the text can be placed relative to the group corner origin (thought the vector is also availebl in the text_label_object to relate to the data origin)
    span_relative_to_self_data_origin = copy.deepcopy(group_object.span_relative_to_self_data_origin)

    group_object__group_label_object__element_span_relative_to_parent_data_origin =\
        group_object.group_label_object.element_span_relative_to_parent_minimum_edge_at_zero_height_plane
    
    for i in range(3):     
        if group_object__group_label_object__element_span_relative_to_parent_data_origin[i][0] < span_relative_to_self_data_origin[i][0]:
            span_relative_to_self_data_origin[i][0] = group_object__group_label_object__element_span_relative_to_parent_data_origin[i][0]
        if group_object__group_label_object__element_span_relative_to_parent_data_origin[i][1] > span_relative_to_self_data_origin[i][1]:
            span_relative_to_self_data_origin[i][1] = group_object__group_label_object__element_span_relative_to_parent_data_origin[i][1]
    
    return span_relative_to_self_data_origin

def intermediate_wrap(active_object):
        #print(f"active_object.name = {active_object.name}")
        #print(f"active_object.span_relative_to_self_data_origin = {active_object.span_relative_to_self_data_origin}")
        #print(f"active_object.padding = {active_object.padding}")
        active_object.minimum_edge_at_zero_height_plane_relative_to_self_data_origin = np.array([active_object.span_relative_to_self_data_origin[0][0],0,active_object.span_relative_to_self_data_origin[2][0]])-np.array(active_object.padding)
        active_object.data_origin_relative_to_self_minimum_corner_origin = np.multiply(-1,np.array([active_object.span_relative_to_self_data_origin[0][0],active_object.span_relative_to_self_data_origin[1][0],active_object.span_relative_to_self_data_origin[2][0]]))
        active_object.data_origin_relative_to_self_minimum_edge_at_zero_height_plane = np.multiply(-1,active_object.minimum_edge_at_zero_height_plane_relative_to_self_data_origin)
        #return active_object.minimum_edge_at_zero_height_plane_relative_to_self_data_origin
'''End Bottom Up Code'''

'''Start Top Down Code''' 
def calculate_span_relative_to_scene_minimum_edge_at_zero_height_plane_top_down(active_object):
    # idealy we want to be avoiding corners and usong data origins as much as possible

    # good 
    # called in main, goes opposite directtion top down. first a bottom up call, then a top down call. Read the code in main.
    if active_object.type == 'scene_object':#and active_object.supergroup==None: # no reason for multiple booleans if this is what I really mean
        active_object.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane = np.array([0,0,0])
        active_object.minimum_edge_at_zero_height_plane_relative_to_supergroup_minimum_edge_at_zero_height_plane = None
    else:

        # possible region of error for minimum_edge_at_zero_height_plane_relative_to_supergroup_minimum_edge_at_zero_height_plane

        # changing this doesnt change the fences relative to each other.
        if active_object.supergroup.type == 'group_object':
            active_object.minimum_edge_at_zero_height_plane_relative_to_supergroup_minimum_edge_at_zero_height_plane = \
                np.multiply(1,\
                            np.multiply(-1,active_object.data_origin_relative_to_self_minimum_edge_at_zero_height_plane)\
                            + active_object.supergroup.data_origin_relative_to_self_minimum_edge_at_zero_height_plane\
                            + active_object.data_origin_relative_to_supergroup_data_origin\
                )
        elif active_object.supergroup.type == 'scene_object':
            active_object.minimum_edge_at_zero_height_plane_relative_to_supergroup_minimum_edge_at_zero_height_plane = \
                np.multiply(1,\
                    np.multiply(-1,active_object.data_origin_relative_to_self_minimum_edge_at_zero_height_plane)\
                    + active_object.supergroup.data_origin_relative_to_self_minimum_edge_at_zero_height_plane\
                    + active_object.data_origin_relative_to_supergroup_data_origin\
                )

        # problem - negatiove values
        active_object.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane = active_object.supergroup.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane\
                                                      + active_object.minimum_edge_at_zero_height_plane_relative_to_supergroup_minimum_edge_at_zero_height_plane
        # incorrect:  minimum_edge_at_zero_height_plane_relative_to_supergroup_minimum_edge_at_zero_height_plane
        # actually, the problem might not be here but rather than the scene is never sxpanded... nah, these junts need translated
        if active_object.type == 'curve_object':
            active_object.data_origin_relative_to_scene_minimum_edge_at_zero_height_plane = active_object.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane\
                                                                                + active_object.data_origin_relative_to_self_minimum_edge_at_zero_height_plane 
            active_object.data_origin_relative_to_supergroup_minimum_edge_at_zero_height_plane = active_object.data_origin_relative_to_scene_minimum_edge_at_zero_height_plane\
                                                                                             - active_object.supergroup.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane

    if active_object.name == "scene_object":
        pass
        #print(f"active_object.span_relative_to_self_minimum_edge_at_zero_height_plane {active_object.span_relative_to_self_minimum_edge_at_zero_height_plane}")
        #print(f"active_object.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane = {active_object.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane}")
    active_object.span_relative_to_scene_minimum_edge_at_zero_height_plane = active_object.span_relative_to_self_minimum_edge_at_zero_height_plane\
                                     + np.transpose([active_object.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane,
                                                     active_object.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane])
    # incorreect: minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane
    # correct: span_relative_to_self_minimum_edge_at_zero_height_plane

    #the dawn
    if active_object.type == 'scene_object':
        active_object.data_origin_relative_to_scene_data_origin = np.array([0,0,0])
    elif active_object.type == 'group_object' and active_object.tier_object.tier_level==1:
        active_object.data_origin_relative_to_scene_data_origin = active_object.data_origin_relative_to_supergroup_data_origin
        active_object.span_relative_to_scene_data_origin_without_text_label = determine_span_relative_to_scene_data_origin_without_text_label(active_object)
    elif active_object.type == 'group_object' and active_object.tier_object.tier_level>1:
        active_object.data_origin_relative_to_scene_data_origin = active_object.data_origin_relative_to_supergroup_data_origin +  active_object.supergroup.data_origin_relative_to_scene_data_origin
        active_object.span_relative_to_scene_data_origin_without_text_label = determine_span_relative_to_scene_data_origin_without_text_label(active_object)
    elif active_object.type == 'curve_object':
        active_object.data_origin_relative_to_scene_data_origin = active_object.data_origin_relative_to_supergroup_data_origin +  active_object.supergroup.data_origin_relative_to_scene_data_origin
    #print("\nSIGNPOST\n")
    active_object.span_relative_to_scene_data_origin = determine_span_relative_to_scene_data_origin(active_object)
    
    # there's a supergroup problem here, wrong level applied to first child. First child is getting infected with super span values.
    
    #print(f'me@zhp:{active_object.span_relative_to_scene_minimum_edge_at_zero_height_plane}')


def determine_span_relative_to_scene_data_origin(active_object):
    span_relative_to_scene_data_origin = active_object.span_relative_to_self_data_origin\
                                + np.transpose([active_object.data_origin_relative_to_scene_data_origin,
                                                    active_object.data_origin_relative_to_scene_data_origin])
    return span_relative_to_scene_data_origin

def determine_span_relative_to_scene_data_origin_without_text_label(active_object):
    span_relative_to_scene_data_origin_without_text_label = active_object.span_relative_to_self_data_origin_without_text_label\
                                + np.transpose([active_object.data_origin_relative_to_scene_data_origin,
                                                    active_object.data_origin_relative_to_scene_data_origin])
    return span_relative_to_scene_data_origin_without_text_label

'''End Top Down Code'''




