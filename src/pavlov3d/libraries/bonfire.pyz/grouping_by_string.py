"""
Title: grouping_by_string.py
Author: Clayton Bennett
Created: 20 January 2024

Purpose:
Classic Pavlov grouping
""" 

from grouping_by_string import GBS
def assign_group_membership_for_complete_hierarchy(hierarchy_object):
    # fix this.
    # add objects to groups
    # do it at conception, inside the GUI process?
    
    #c_key: curve_object_key
    #g_key: group_object_key
    tally_of_curve_objects_assigned_to_a_group = 0
    # Starting with the curve_objects and then working up allows max and min values to be passed upward,like a classroom champion game of rock-paper-scissors
    # This relies on a naming convention grouping paradigm: groups are based on text flags that are present in filenames
    for t_key,tier_object in reversed(hierarchy_object.dict_tier_objects.items()):
        for g_key,group in tier_object.dict_group_objects.items():
            for c_key,curve_object in hierarchy_object.dict_curve_objects_all.items():
                if t_key+1 in hierarchy_object.dict_tier_objects and len(hierarchy_object.dict_tier_objects[t_key+1].dict_curve_objects)>0:
                    # are you at the bottom tier? Yes with the highest t_key value and with curve_objects in it.
                    # if data objects are in the tier, we assume it is the bottom tier (with the highest t_key value)
                    # to keep this true, subgroups with key 'none' will need to be created to hold data objects that are in a (higher)supergroup but have no relevant provided (immediate)super/group
                    #if g_key.lower() in c_key.lower():
                    #if group.simple_name.lower() in c_key.lower():
                    if group.simple_name.lower() in c_key.lower() and group.compound_subgroup_name.split(GBS.comp_char)[0].lower() in c_key.lower() and group.compound_subgroup_name.split(GBS.comp_char)[-1].lower() in c_key.lower():
                        group.add_curve_object(curve_object,c_key)
                        tally_of_curve_objects_assigned_to_a_group += 1 # once complete, will equal len(hierarchy_object.dict_curve_object_all.keys()). If it doesn't, there are 'none' type subgroups, where a curve_object fits into a stated group but none of its stated subgroups
                        # develop further how subgroups are added for 'none'. Add a 'none' to every group, then remove it later?
                    else:
                        pass
                        
                elif t_key+1 in hierarchy_object.dict_tier_objects and len(hierarchy_object.dict_tier_objects[t_key+1].dict_group_objects)>0:
                    # you are not at the bottom tier, and there are more groups to explore
                    for s_key,subgroup in hierarchy_object.dict_tier_objects[t_key+1].dict_group_objects.items():
                        #if s_key.lower() in c_key.lower() and g_key.lower() in c_key.lower(): # stable for simple-name
                        #if subgroup.simple_name.lower() in c_key.lower() and group.simple_name.lower() in c_key.lower() and subgroup.simple_name.lower() in group.name.lower(): # attempt at complex names
                        if subgroup.compound_subgroup_name.split(GBS.comp_char)[0].lower() in c_key.lower() and subgroup.compound_subgroup_name.split(GBS.comp_char)[-1].lower() in c_key.lower() and group.simple_name.lower() in c_key.lower():
                            #print(f"\ngroup.simple_name: {group.simple_name}, subgroup.simple_name: {subgroup.simple_name}")
                            #print(f"group.compound_subgroup_name: {group.compound_subgroup_name}, subgroup.compound_subgroup_name: {subgroup.compound_subgroup_name}")
                            #print(f"g_key: {g_key}, s_key: {s_key}, c_key: {c_key}")
                            group.add_subgroup(subgroup,s_key)
                            #print(f's_key in c_key and g_key in c_key: {g_key},{s_key},{c_key}')
                            #subgroup.add_supergroup(group,g_key) # redundant, done in group.add_subgroup()
                        #elif s_key.lower() in c_key.lower() and g_key=="scene_object":# the one exception to the rule of the group name needing to be in the file name
                        elif subgroup.simple_name.lower() in c_key.lower() and g_key=="scene_object":#
                            #print(f'c_key:{c_key}')
                            group.add_subgroup(subgroup,s_key)
                        #    #subgroup.add_supergroup(group,g_key) # redundant, done in group.add_subgroup()
                        
                    #if curve_object.parent is None and :
                    #    hierarchy_object._add_curve_object_to_ungrouped(curve_object,group)     
                else:              
                    print('problem==True')
    
    # check for curve_objects that have not been assigned a supergroup

def define_groups(group_names,subgroup_names):
    
    ## Leverage: Make subgroup names redundant for each group using the compound_subgroup_name
    #self.secret_full_name = "null0-null1-null2-null3" # scene-Stiles-June, scene-Stiles, etc. number of hyphens should equal tier of group, ideally. scene-Maxson-June is different from scene-Stiles-June. Any dictionary keys athat need a name should use the group_object.secret_full_name. No keys might be better.
    #self.compound_subgroup_name = "supergroupname-selfsubgroupname"
    try:
        group_names = group_names.split(',') # only works for loaded json - need to do this further upsteam
        subgroup_names = subgroup_names.split(',')
    except:
        pass


    for i,group in enumerate(group_names):
        group_names[i] = group.strip().lower()
    for i,group in enumerate(subgroup_names):
        subgroup_names[i] = group.strip().lower()

    subgroup_compound_names = []
    for group_name in group_names:
        for subgroup_name in subgroup_names:
            subgroup_compound_name = group_name+"-"+subgroup_name
            subgroup_compound_names.append(subgroup_compound_name)

    group_compound_names = []
    for group_name in group_names:
        group_compound_name = "scene-"+group_name
        group_compound_names.append(group_compound_name)

    dict_groups_tiers = dict()
    #dict_groups_tiers[2] = subgroup_names
    dict_groups_tiers[2] = subgroup_compound_names
    #dict_groups_tiers[1] = group_names
    dict_groups_tiers[1] = group_compound_names
    
    return dict_groups_tiers