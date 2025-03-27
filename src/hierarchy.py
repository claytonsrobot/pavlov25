"""
Title: hierarchy.py
Author: Clayton Bennett
Created: 24 September 2024

Purpose: 
Off load functonality from scene.py, to provide oversight and opportunity for improvement
"""

from src.group import Group
from src.tier import tier as Tier
import inspect
from src import grouping_by_string
from src.grouping_by_string import GBS
from src import grouping_by_map
from src.curve_ import Curve

class Hierarchy:
    scene_object = None
    style_object=None
    user_input_object=None
    allowed_keys = set(['padding','padding_coefficient',
                        'names','vectorArray_time','vectorArray_height','headers_time','headers_height',
                        'max_depth','min_depth','desciption_textbox','legend','group_hierarchy_tree','color_palette',
                        'axes_shared','text_box','title','max_raw_data','min_raw_data'])
    @classmethod
    def assign_user_input_object(cls,user_input_object):
        cls.user_input_object = user_input_object

    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object = scene_object

    @classmethod
    def assign_style_object(cls,style_object):
        cls.style_object = style_object
        #style_object.assign_scene_object(cls) # nope. this assigns the class, not the instance
        
    def __init__(self,name="hierarchy"):
        
        self.name = name
        self.hierarchy_object = self

        self.only_longest_axes_ticks_siblings_and_cousins = True

        #self.dict_subgroups = dict()
        self.dict_group_objects_all = dict() # regardless of hierarchy
        self.dict_group_objects_most = dict() # regardless of hierarchy
        self.dict_curve_objects_all = dict() # regardless of hierarchy

        self.grand_cousin_flights_curves = dict()
        self.great_grand_cousin_flights_curves = dict()
        self.grand_cousin_flights_subgroups = dict()
        self.great_grand_cousin_flights_subgroups = dict()

        self.dict_tier_objects = dict()

    def cycle_through_filenames_intialize_curves(self):
        Curve.pass_in_scene_object(self.scene_object)
        #def add_curve_object_to_scene_object(self): #check use 30Jan
        for filename in self.user_input_object.filenames:
            curve_object = Curve(name=filename)
            curve_object.hierarchy_registration()
            #self.hierarchy_object.dict_curve_objects_all.update({filename:curve_object}) 
        

    def build_tiers_and_groups_objects(self,user_input_object):
        # user input objec is just used for stack direciton and group name dictionary
        # you could have tiers built ....somewhere else, then have them handed in, but this is fine.
        # fine, if you improve the tier instantiation.
        # Where are curve_object built not?
        # builtObjectNode()
        # these should be wholely separate: the problm is right now tier creation is not generalized enough, so each tier is explicitly l
        # formerly known as buildGroups()

        Tier.assign_hierarchy_object(self)
        
        if len(self.dict_curve_objects_all)==0:
            print('ERROR: curve_objects were not formed and/or added to hierarchy_object.dict_curve_objects_all in the import module.')
        else: 
            pass
            #print(f'self.dict_curve_objects_all.keys() = {self.dict_curve_objects_all.keys()}')

        ''' Build tiers, and assign stack direction and group names from user input text fields in GUI'''
        tier_object=Tier(0)
        """ # changed 04 Feb 2025
        try: #https://hynek.me/articles/hasattr/
            tier_object=self.tier_object
        except AttributeError:
            tier_object = Tier(0) # should have been built when the scene was built...but it can be done here
            #self.tier_object = tier_object 
        """
        #tier_object.assign_stack_direction(user_input_object.groups_tier0_stack_direction)
        tier_object.assign_stack_direction(None)
        tier_object.add_group_object(self.scene_object,'scene_object')
        
        tier_object = Tier(1) # create tier object,which adds the tier object to this scene
        #tier_object.assign_stack_direction(user_input_object.groups_tier1_stack_direction)
        tier_object.assign_stack_direction(user_input_object.stack_direction_groups)
        for i,key in enumerate(user_input_object.dict_groups_tiers[1]):
            # appy group names based on user input object, known groups for each tier
            if False:#test 4 Feb 2025
                group_object = Group(scene_object=self.scene_object,name=key) # OG, works
            else:
                group_object = Group(scene_object=self.scene_object,simple_name=key.replace(str("scene"+GBS.comp_char),""),compound_subgroup_name=key) #compound-names
            tier_object.add_group_object(group_object,key)
            self.scene_object.add_subgroup(group_object,key)

        tier_object = Tier(2)
        #tier_object.assign_stack_direction(user_input_object.groups_tier2_stack_direction)
        tier_object.assign_stack_direction(user_input_object.stack_direction_subgroups)
        for i,key in enumerate(user_input_object.dict_groups_tiers[2]):
            #group_object = Group(scene_object=self.scene_object,simple_name=key) # OG, works
            group_object = Group(scene_object=self.scene_object,simple_name=key.split(GBS.comp_char)[-1],compound_subgroup_name=key) #compound-names
            tier_object.add_group_object(group_object,key)

        # makig automatic dump group and sugroup is the biggest barrier to launch
        # and fbx push to blob
        if False: 
            self._make_empty_group_for_each_tier() # not yet functional
            # This add a group named like "-0", "-1", "-2", etc, based on the tier. It is problematic especially when grouping is based on filename, rather than a group mapping file
            #print(f'Fix: self._make_empty_group_for_each_tier()')
        #''' Assign all group objects placed in tiers into a complete dictionary of group objects'''

        # explicit is better than implicit
        # look this is very important. This is a quintessential part of the program
        # create a function and give it a real name. But also ughhhhh aesthetics. Pythonic aesthetics.
        for tier_object in self.dict_tier_objects.values():
            #print(f"tier_object.tier_level = {tier_object.tier_level}")
            #print(f"tier_object.dict_group_objects = {tier_object.dict_group_objects}")
            #for key,value in tier_object.dict_group_objects.items():
                #print(f"GRATZER, key = {key}")
                #print(f"GRATZER, value = {value}")
                #print(f"GRATZER, value.name = {value.name}")
                #print(f"GRATZER, value.dict_subgroups = {value.dict_subgroups}")
                #try:
                #    print(f"GRATZER, value.supergroup.name = {value.supergroup.name}")
                #except:
                #    pass
            self.dict_group_objects_all.update(tier_object.dict_group_objects)
        
        tier_object = Tier(3)
        #tier_object.assign_stack_direction(user_input_object.groups_tier3_stack_direction)
        tier_object.assign_stack_direction(user_input_object.stack_direction_curves)
        for key,curve_object in self.dict_curve_objects_all.items():# curve_objects built in input_plugin
            tier_object.add_curve_object(curve_object,key)
        
        #self._make_empty_group_for_each_tier() # moved up before dict_group_objects_all is generated from the groups in each tier
        self._assign_group_membership_for_complete_hierarchy(self.user_input_object.grouping_algorithm) # based on if g_key.lower() in c_key.lower():
        
        #self._check_for_unassigned_curve_objects()
        self._destroy_empty_groups()
        self.maybe_destroy_unassigned_curves()
        self._make_dict_group_object_most()
        self._tier_hierarchy_linking()
        self._explicate_siblings()
        self._determine_place_in_supergroup()
        self.diaspora_assignment()
        self.grandfather_cousin_flight_assignment_curves()
        self.great_grandfather_cousin_flight_assignment_curves()
        self.combine_cousins_levels()
        self.grandfather_cousin_flight_assignment_subgroups()
        
    def _make_empty_group_for_each_tier(self):
        
        for tier_object in self.dict_tier_objects.values():
            
            g_key = '_'+str(tier_object.tier_level)
            group_object = Group(scene_object=self.scene_object,name=g_key) 
            tier_object.add_group_object(group_object,g_key)

    def _assign_group_membership_for_complete_hierarchy(self,grouping_algorithm):
        # i think once you get to this point, you might not need logic, they all run the same?
        if grouping_algorithm == "group-by-text":
            grouping_by_string.assign_group_membership_for_complete_hierarchy(hierarchy_object = self) # stable but error prone, if you cam say that #
        elif grouping_algorithm == "group-by-map": #testing 1 February 2025
            grouping_by_map.assign_group_membership_for_complete_hierarchy(hierarchy_object = self)
        return True
    # check for curve_objects that have not been assigned a supergroup    
    def _add_curve_object_to_ungrouped(self,curve_object):
        print(f'>>> {inspect.stack()[2][3]}')
        print(f'>> {inspect.stack()[1][3]}')
        print(f'> {inspect.stack()[0][3]}')
        
        print(f'If you hit this, probably you didnt include the correct subgroup names')
        # python can i print the name of the most recently called or current function?
        bottom_tier_key = max(list(self.dict_tier_objects.keys())) # assumes numeric keys....there has to be a better way to do this
        tier_object=self.dict_tier_objects[bottom_tier_key]
        #g_key = '-'+str(tier_object.tier_level)
        g_key = '_'+str(tier_object.tier_level)
        g_key = str(tier_object.tier_level)
        print(f"tier_object.dict_group_objects.keys() = {tier_object.dict_group_objects.keys()}")
        group = tier_object.dict_group_objects[g_key].add_curve_object # override, bitches
        group.add_curve_object(curve_object,c_key=curve_object.name)
        return True
    
    def _check_for_unassigned_curve_objects(self):
        for curve_object in self.dict_curve_objects_all.values():
            if curve_object.supergroup is None:
                print(f"Unassigned:{curve_object.name}")
                self._add_curve_object_to_ungrouped(curve_object)
                
        '''for c_key,curve_object in self.dict_curve_objects_all.items():
            if curve_object.supergroup is None:
                print(f'Create ungrouped group for: curve_object.name:{curve_object.name}')
                group_object,g_key = self._make_ungrouped_group()
                group_object.add_curve_object(curve_object,c_key)
                #curve_object.add_supergroup(group_object,g_key) # happens automatically in group_object.add_curve_object'''

    """ def _make_ungrouped_group(self):
        g_key = 'ungrouped'
        if not(g_key in self.dict_subgroups): # check, does 'ungrouped' group exist yet
            # make ungrouped group, set in the first tier as a subgroup of the scene_object
            group_object = Group(scene_object=self.scene_object,name=g_key)
            tier_object = self.dict_tier_objects[1]
            tier_object.add_group_object(group_object,g_key)
            self.add_subgroup(group_object,g_key)
            group_object.add_supergroup(self,'scene_object')
        group_object = self.dict_subgroups[g_key]
        return group_object,g_key """

    def apply_curve_object_spans(self):
        # consider all groups which have curves as children
        tier_object = self.dict_tier_objects[2]
        #print(f"tier_object.key = {tier_object.key}")
        
        sorted_objects = sorted(tier_object.dict_group_objects.values(), key=lambda obj: obj.place_in_supergroup)
        for group_object in sorted_objects:
            for key,curve_object in group_object.dict_curve_objects.items():# curve_objects built in input_plugin
                group_object.apply_curve_object_span(curve_object)

    def apply_group_object_spans(self):
        # consider all groups which have other (sub)groups as children
        for tier in [1]:
            tier_object = self.dict_tier_objects[tier]
            sorted_objects = sorted(tier_object.dict_group_objects.values(), key=lambda obj: obj.place_in_supergroup)
            for group_object in sorted_objects:
            #for group_object in tier_object.dict_group_objects.values():
                for key,subgroup_object in group_object.dict_subgroups.items():# curve_objects built in input_plugin
                    group_object.apply_subgroup_object_span(group_object) # never defined

    def group_padding_assignment(self):
        # padding assignment
        # need to add curve_object.padding assignment?
        for tier in reversed(self.dict_tier_objects.values()):
            for group in tier.dict_group_objects.values():
                if group.max_raw_data != None:#would have had to have created and imported data Objects, and assigned with add_subgroup
                    group.padding_assignment() # once these junts are build and all data has propogated upwards, we can determine the padding for each group, based on the size of its contents.
                else:
                    destroy_group=1
                    
    def _tier_hierarchy_linking(self):
        # tier hierarchy linking, top down
        t_key_list = list(self.dict_tier_objects.keys())
        for t_key in t_key_list:
            if t_key+1 in self.dict_tier_objects.keys():
                self.dict_tier_objects[t_key].sub_tier_object = self.dict_tier_objects[t_key+1]
            if t_key-1 in self.dict_tier_objects.keys():
                self.dict_tier_objects[t_key].super_tier_object = self.dict_tier_objects[t_key-1]
                
    def _destroy_empty_groups(self):
        '''Work to make cleanup tier count agnostic'''
        print("hierarchy._destroy_empty_groups()")

        # Part 1: Remove empty groups from dict_group_objects_all
        group_keys_to_remove = [
            key for key, group in list(self.dict_group_objects_all.items())
            if group.dict_children is None
        ]

        for key in group_keys_to_remove:
            #print(f"remove: {key}")
            if key in self.dict_group_objects_all:
                del self.dict_group_objects_all[key]
            if key in self.scene_object.dict_children:
                #print(f"delete: {key}")
                del self.scene_object.dict_children[key]
                #print(f"deleted: {key}")

        # Part 2: Remove groups from tier dictionaries if they are missing from dict_group_objects_all
        for t_key, tier in self.dict_tier_objects.items():
            tier_group_keys = list(tier.dict_group_objects.keys())
            #if len(tier_group_keys) != 0:
            #    pass
            #    #print(f"group_key_list = {tier_group_keys}")

            keys_to_remove = [key for key in tier_group_keys if key not in self.dict_group_objects_all]
            for key in keys_to_remove:
                #print(f"remove: {key}")
                if key in tier.dict_group_objects:
                    del tier.dict_group_objects[key]

        # Part 3: Remove empty groups from scene_object.dict_subgroups
        scene_keys_to_remove = [
            key for key, group in list(self.scene_object.dict_subgroups.items())
            if group.dict_children is None or len(group.dict_children) == 0
        ]

        for key in scene_keys_to_remove:
            #print(f"del(self.scene_object.dict_subgroups[{key}])")
            if key in self.scene_object.dict_subgroups:
                del self.scene_object.dict_subgroups[key]
    def _make_dict_group_object_most(self):
        for key,group_object in self.dict_group_objects_all.items(): 
            if group_object.type!=self.scene_object.    type:
                self.dict_group_objects_most.update({key:group_object})

    
    def _explicate_siblings(self):
        for group_object in self.dict_group_objects_all.values(): 
            for child in group_object.dict_children.values():
                #child.siblings = set.union(group_object.dict_children.values())
                # set way
                #child.siblings = {group_object.dict_children[sub] for sub in group_object.dict_children}
                #child.siblings.remove(child)
                # dict way
                child.siblings = {
                sub: group_object.dict_children[sub] 
                for sub in group_object.dict_children
                    if group_object.dict_children[sub] != child
                    }

    def _determine_place_in_supergroup(self):
        # we arguably do not need last_cousin,last_nephew,or first_uncle values
        # curve_object.place_in_supergroup assignment
        # this assumes all curve_objects are on the same tier
        # a different looping apprach could find previous_object and place_in_supergroup attributes for all curve_object and group_objects, regardles of tier

        for t_key,tier_object in reversed(self.dict_tier_objects.items()):#bottom up
            # places do not exist yet
            #sorted_objects = sorted(tier_object.dict_group_objects.values(), key=lambda obj: obj.place_in_supergroup)
            #for group_object in sorted_objects:
            for group_object in tier_object.dict_group_objects.values():
                c_key_list = list(group_object.dict_children.keys())
                #for child_objects in group_object.dict_children.values():
                #for place,c_key in enumerate(c_key_list):
                for place_in_supergroup,child_object in enumerate(group_object.dict_children.values()):
                    #print(f"place_in_supergroup = {place_in_supergroup}")
                    #print(f"child_object = {child_object}")
                    #child=group_object.dict_children[c_key]
                    #child.place_in_supergroup=place
                    child_object.place_in_supergroup=place_in_supergroup
                    if place_in_supergroup>0:
                        child_object.previous_sibling = group_object.dict_children[c_key_list[place_in_supergroup-1]]
                        #child_object.previous_sibling.next_sibling = group_object # wrong?
                        child_object.previous_sibling.next_sibling = child_object # wrong?
                        child_object.last_nephew = None
                    
                    elif place_in_supergroup==0:
                        child_object.previous_sibling=None
                        group_object.first_child=child_object
                        #child.supergroup = group_object # known
                        try:
                            last_cousin.first_uncle = child_object
                            child_object.last_nephew = last_cousin
                            # this should be hit once per tier, on the first item processed in the tier
                        except:
                            #last_cousin.first_uncle = None
                            #child.last_nephew = None
                            #print("\nWHACK1,hierarchy._determine_place_in_supergroup()")
                            pass
                            last_cousin_not_yet_initialized=1
                    #finally, for both cases
                    try:
                        child_object.next_sibling = group_object.dict_children[c_key_list[place_in_supergroup+1]]
                    except:
                        child_object.next_sibling = None
                        #print("\nWHACK2,hierarchy._determine_place_in_supergroup()")
                        there_in_no_other_child_in_this_tier=1
                last_cousin = child_object # hits for the end of the for loop
            if t_key==0:# scene_object
                group_object.place_in_supergroup=None
                last_cousin.first_uncle = group_object
                group_object.last_nephew=last_cousin
                group_object.next_sibling=None
                group_object.previous_sibling=None
    
    def determine_characteristic_length_for_group(self,active_object):
        # doesnt hit for those not in hierarchy 

        # i want shared font size, ultimately.

        # don't determine height 
        # this could be full time and depth diameters....but we reallly just need this for group title length, which can be based on a few different things.
        # use the largest font or the longest axis length known or make it the full length
        # this isn't span
        if active_object.type=="curve_object":
            pass
        elif active_object.type=="group_object":
            largest=0
            #print(f"active_object.name = {active_object.name}")
            for child in active_object.dict_children.values():
                #print(f"child.name = {child.name}")
                if child.characteristic_length>largest:
                    largest = child.characteristic_length
            if len(active_object.dict_children)==0:
                print(f'\n> {inspect.stack()[0][3]}')
                print('This group has no children, you probably typed it in wrong\n') 
            else:
                pass
            active_object.characteristic_length=largest

    def print_hierarchy_by_lineage(self):
        print(f"\nscene_object.name = {self.scene_object.name}")
        for group_object in self.scene_object.dict_children.values():
            print(f"|")    
            print(f"-group_object.name = {group_object.name}")
            for subgroup_object in group_object.dict_children.values():
                print(f"|\t|")
                print(f"|\t-subgroup_object.name = {subgroup_object.name}")
                for curve_object in subgroup_object.dict_children.values():
                    print(f"|\t\t|")
                    print(f"|\t\t-curve_object.name = {curve_object.name}")
        print(f"end\n")

    def print_hierarchy_cousins_by_lineage(self):
        print(f"\nscene_object.name = {self.scene_object.name}")
        for group_object in self.scene_object.dict_children.values():
            print(f"|")    
            print(f"-group_object.name = {group_object.name}")
            print(f" group_object.data_origin_relative_to_previous_sibling_data_origin = {group_object.data_origin_relative_to_previous_sibling_data_origin}")
            for subgroup_object in group_object.dict_children.values():
                print(f"|\t|")
                print(f"|\t-subgroup_object.name = {subgroup_object.name}")
                print(f"|\t subgroup_object.data_origin_relative_to_previous_sibling_data_origin = {subgroup_object.data_origin_relative_to_previous_sibling_data_origin}")
                for curve_object in subgroup_object.dict_children.values():
                    print(f"|\t\t|")
                    print(f"|\t\t-curve_object.name = {curve_object.name}")
                    print(f"|\t\t curve_object.data_origin_relative_to_previous_sibling_data_origin = {curve_object.data_origin_relative_to_previous_sibling_data_origin}")
        print(f"end\n")


    #data_origin_relative_to_supergroup_data_origin
    def print_hierarchy_data_origins_relative_to_supergroup_by_lineage(self):
        print(f"\nscene_object.name = {self.scene_object.name}")
        for group_object in self.scene_object.dict_children.values():
            print(f"|")    
            print(f"|_group_object.name = {group_object.name}")
            print(f"| group_object.place_in_supergroup = {group_object.place_in_supergroup}")
            print(f"| group_object.data_origin_relative_to_supergroup_data_origin = {group_object.data_origin_relative_to_previous_sibling_data_origin}")
            for subgroup_object in group_object.dict_children.values():
                print(f"|\t|")
                print(f"|\t|_subgroup_object.name = {subgroup_object.name}")
                print(f"|\t subgroup_object.place_in_supergroup = {subgroup_object.place_in_supergroup}")
                print(f"|\t subgroup_object.data_origin_relative_to_supergroup_data_origin = {subgroup_object.data_origin_relative_to_previous_sibling_data_origin}")
                for curve_object in subgroup_object.dict_children.values():
                    print(f"|\t|\t|")
                    print(f"|\t|\t|_curve_object.name = {curve_object.name}")
                    print(f"|\t \t curve_object.place_in_supergroup = {curve_object.place_in_supergroup}")
                    print(f"|\t \t curve_object.data_origin_relative_to_supergroup_data_origin = {curve_object.data_origin_relative_to_previous_sibling_data_origin}")
        print(f"end\n")

    def print_hierarchy_previous_siblings_by_lineage(self):
        print(f"\nscene_object.name = {self.scene_object.name}")
        for group_object in self.scene_object.dict_children.values():
            print(f"|")    
            print(f"-group_object.name = {group_object.name}")
            try:
                print(f" group_object.previous_sibling.name = {group_object.previous_sibling.name}")
            except:
                print(f" group_object.previous_sibling = none")
            for subgroup_object in group_object.dict_children.values():
                print(f"|\t|")
                print(f"|\t-subgroup_object.name = {subgroup_object.name}")
                try:
                    print(f"|\t subgroup_object.previous_sibling.name = {subgroup_object.previous_sibling.name}")
                except:
                    print(f"|\t subgroup_object.previous_sibling = none")
                for curve_object in subgroup_object.dict_children.values():
                    print(f"|\t\t|")
                    print(f"|\t\t-curve_object.name = {curve_object.name}")
                    try:
                        print(f"|\t\t curve_object.previous_sibling.name = {curve_object.previous_sibling.name}")
                    except:
                        print(f"|\t\t curve_object.previous_sibling = none")
        print(f"end\n")

    def print_hierarchy_place_in_supergroup_by_lineage(self):
        print(f"\nscene_object.name = {self.scene_object.name}")
        for group_object in self.scene_object.dict_children.values():
            print(f"|")    
            print(f"-group_object.name = {group_object.name}")
            try:
                print(f" group_object.place_in_supergroup = {group_object.place_in_supergroup}")
            except:
                print(f" group_object.place_in_supergroup = none")
            for subgroup_object in group_object.dict_children.values():
                print(f"|\t|")
                print(f"|\t-subgroup_object.name = {subgroup_object.name}")
                try:
                    print(f"|\t subgroup_object.place_in_supergroup = {subgroup_object.place_in_supergroup}")
                except:
                    print(f"|\t subgroup_object.place_in_supergroup = none")
                for curve_object in subgroup_object.dict_children.values():
                    print(f"|\t\t|")
                    print(f"|\t\t-curve_object.name = {curve_object.name}")
                    try:
                        print(f"|\t\t curve_object.place_in_supergroup = {curve_object.place_in_supergroup}")
                    except:
                        print(f"|\t\t curve_object.place_in_supergroup = none")
        print(f"end\n")

    def step_through_hierarchy_by_lineage(self, command):
        for group_object in self.scene_object.dict_children.values():
            command(group_object)
            for subgroup_object in group_object.dict_children.values():
                command(subgroup_object)
                for curve_object in subgroup_object.dict_children.values():
                    command(curve_object)


    def step_through_hierarchy_top_down(self,command):
        # something is missing :)
        
        for tier_object in self.dict_tier_objects.values():#top down
            sorted_objects = sorted(tier_object.dict_group_objects.values(), key=lambda obj: obj.place_in_supergroup)
            for group_object in sorted_objects:
            #for group_object in tier_object.dict_group_objects.values():
                print(f"Stepping down: group_object.name = {group_object.name}")
                command(group_object)
        
        for group_object in self.dict_group_objects_all.values(): # includes scene object
            for curve_object in group_object.dict_curve_objects.values():
                command(curve_object)

    def step_through_hierarchy_bottom_up(self, command):
        #print("hierarchy.step_through_hierarchy_bottom_up()")
        # Loop through the tier objects in reverse order (bottom-up)
        for tier_object in reversed(self.dict_tier_objects.values()):
            #print(f"tier_object.tier_level = {tier_object.tier_level}")
            # Process all curve objects in the current tier
            sorted_objects = sorted(tier_object.dict_curve_objects.values(), key=lambda obj: obj.place_in_supergroup)
            for curve_object in sorted_objects:
            #for curve_object in tier_object.dict_curve_objects.values():
                #print(f"curve_object.name = {curve_object.name}")
                #print(f"curve_object.place_in_supergroup = {curve_object.place_in_supergroup}")
                #try:
                command(curve_object)
                #except Exception as e:
                #    print(f"\nFAIL: CURVE OBJECT: {curve_object.name} | Error: {e}\n")

            # Process all group objects in the current tier
            sorted_objects = sorted(tier_object.dict_group_objects.values(), key=lambda obj: obj.place_in_supergroup)
            for group_object in sorted_objects:
            #for group_object in reversed(tier_object.dict_group_objects.values()): 
                #print(f"group_object.name = {group_object.name}")
                #print(f"group_object.place_in_supergroup = {group_object.place_in_supergroup}")
                #try:
                command(group_object)
                #except Exception as e:
                #    print(f"\nFAIL: GROUP OBJECT: {group_object.name} | Error: {e}\n")

    def diaspora_assignment(self):

        # for any given tier, for each groups in that tier, step down through all children and add all curve_objects to dict_curve_object_diaspora
        # not the fastest or least redundant,  but who cares
        # add them all to the same diaspora list

        for tier_object in reversed(self.dict_tier_objects.values()):#bottom up
            sorted_objects = sorted(tier_object.dict_group_objects.values(), key=lambda obj: obj.place_in_supergroup)
            for group_object in sorted_objects:
            #for group_object in tier_object.dict_group_objects.values():
                group_object.dict_curve_object_diaspora = dict()
                #print(f'group_object = {group_object}')
                #print(group_object.name)
                #print(group_object.dict_children.keys())
                if len(group_object.dict_curve_objects)>0:
                    group_object.dict_curve_object_diaspora = group_object.dict_curve_objects
                else:
                    #print(f'list subgroups: {group_object.dict_subgroups.keys()}')
                    for subgroup_object in group_object.dict_subgroups.values():
                        #print(f'subgroup: {subgroup_object.name}')
                        #print(f'group_object__ = {group_object}')
                        group_object.dict_curve_object_diaspora.update(subgroup_object.dict_curve_object_diaspora)

    def grandfather_cousin_flight_assignment_curves(self):
        # this needs to happen iterively until the tier key is equal to zero
        # there is no need at the subgroup level, hypothetically, because there are only siblings not cousins
        # so in a four tier system (scene, groups, subgroups, curves), this needs does for tier_key 1 and tier_key 0
        ''' the first is included in the second but the second is not included in the first. check scene''' # 20 May 2024
        # secondary cousin alignment only applies to one tier up from the lowest group.
        # could actually be applied to each level hiher, but, with pros and cons - more lvels of stack alignement, vs unnecesary spacing
        lowest_tier = max(self.dict_tier_objects.keys())
        secondary_alightment_tier = lowest_tier-2 # 1, in a four tier system
        #tertiary_alightment_tier = secondary_alightment_tier - 1 
        tier_key = secondary_alightment_tier
        #while tier_key >=0: # test # better than not, but some unnecessary translation are applied, when the stack has not overlap but it is assumed that they do
        while tier_key ==1: # keep
            tier_object = self.dict_tier_objects[tier_key]
            sorted_objects = sorted(tier_object.dict_group_objects.values(), key=lambda obj: obj.place_in_supergroup)
            for group_object in sorted_objects:
            #for group_object in tier_object.dict_group_objects.values():
                #group_object.grand_cousin_flights_curves = dict() # intitialzed in constructor
                flight_key = 0
                assigned_cousins_count = 0 
                while assigned_cousins_count < len(group_object.dict_curve_object_diaspora):
                    for curve_object in group_object.dict_curve_object_diaspora.values():
                        flight_key = curve_object.place_in_supergroup
                        if flight_key in group_object.grand_cousin_flights_curves.keys(): 
                            #group_object.grand_cousin_flights_curves[flight_key].add(curve_object) # set
                            group_object.grand_cousin_flights_curves[flight_key][curve_object.name]=curve_object # dictionary

                            assigned_cousins_count+=1                 
                        else:
                            #group_object.grand_cousin_flights_curves.update({flight_key:set()}) # set
                            group_object.grand_cousin_flights_curves.update({flight_key:{}}) # dictionary
                            #group_object.grand_cousin_flights_curves[flight_key].add(curve_object) # set
                            group_object.grand_cousin_flights_curves[flight_key][curve_object.name]=curve_object # dictionary
                            
                            assigned_cousins_count+=1

                # applies to curve_objects and subgroup_objects, as cousin objects
                #print(f"group_object.grand_cousin_flights_curves = {group_object.grand_cousin_flights_curves}")
                for key,cousin_objects in group_object.grand_cousin_flights_curves.items():
                    #for cousin_object in group_object.grand_cousin_flights_curves[key]:
                    for cousin_object in cousin_objects.values():
                        #print(f"cousin_object = {cousin_object}")
                        cousin_object.cousin_flight = group_object.grand_cousin_flights_curves[key].copy()
                
                # This is here: to be able to reference cousins from the object, rather from its parents
                # .grandfather_place_cousins might be the same as .cousin_flight 
                # .grandfather_place_cousins and .cousin_flight are both not siblings
                for cousins_ in group_object.grand_cousin_flights_curves.values():
                    for cousin in cousins_.values():
                        #print(f"cousin = {cousin}, cousin.name = {cousin.name}")
                        cousin.grandfather_place_cousins = cousins_.copy()
                        if False:# False = inclusive of cousin_self
                            cousin.grandfather_place_cousins.remove(cousin) # inclusive of self or exclusive??
            tier_key = tier_key-1
        

            # we hypothetically also need a way to add great_grandfather_cousins, with a choice to accept this, for higher level alignement between top toer groups
        #flight_key = [0,1,2,3,4]
    def great_grandfather_cousin_flight_assignment_curves(self):
        # probably wrong
        # this needs to happen iterively until the tier key is equal to zero
        # there is no need at the subgroup level, hypothetically, because there are only siblings not cousins
        # so in a four tier system (scene, groups, subgroups, curves), this needs does for tier_key 1 and tier_key 0
        ''' the first is included in the second but the second is not included in the first. check scene''' # 20 May 2024
        # secondary cousin alignment only applies to one tier up from the lowest group.
        # could actually be applied to each level hiher, but, with pros and cons - more lvels of stack alignement, vs unnecesary spacing
        lowest_tier = max(self.dict_tier_objects.keys())
        secondary_alightment_tier = lowest_tier-2 # 1, in a four tier system
        tertiary_alightment_tier = secondary_alightment_tier - 1 
        tier_key = tertiary_alightment_tier
        #while tier_key >=0: # better than not, but some unnecessary translation are applied, when the stack has not overlap but it is assumed that they do
        while tier_key ==0:# secondary
            tier_object = self.dict_tier_objects[tier_key]
            sorted_objects = sorted(tier_object.dict_group_objects.values(), key=lambda obj: obj.place_in_supergroup)
            for group_object in sorted_objects:
            #for group_object in tier_object.dict_group_objects.values():
                #group_object.great_grand_cousin_flights_curves = dict() # intitialzed in constructor
                flight_key = 0
                assigned_cousins_count = 0 
                while assigned_cousins_count < len(group_object.dict_curve_object_diaspora):
                    for curve_object in group_object.dict_curve_object_diaspora.values():
                        flight_key = curve_object.place_in_supergroup
                        if flight_key in group_object.great_grand_cousin_flights_curves.keys(): 
                            #group_object.great_grand_cousin_flights_curves[flight_key].add(curve_object) #set
                            group_object.great_grand_cousin_flights_curves[flight_key][curve_object.name]=curve_object # dictionary
                            
                            assigned_cousins_count+=1                 
                        else:
                            #group_object.great_grand_cousin_flights_curves.update({flight_key:set()}) # set
                            #group_object.great_grand_cousin_flights_curves[flight_key].add(curve_object) # set
                            group_object.great_grand_cousin_flights_curves.update({flight_key:{}}) # dictionary
                            group_object.great_grand_cousin_flights_curves[flight_key][curve_object.name]=curve_object # dictionary
                           
                            assigned_cousins_count+=1

                # applies to curve_objects and subgroup_objects, as cousin objects
                for key,cousin_objects in group_object.great_grand_cousin_flights_curves.items():
                    #for cousin_object in group_object.great_grand_cousin_flights_curves[key]:
                    for cousin_object in cousin_objects.values():
                        cousin_object.cousin_flight = group_object.great_grand_cousin_flights_curves[key].copy()
                
                # This is here: to be able to reference cousins from the object, rather from its parents
                # .grandfather_place_cousins might be the same as .cousin_flight 
                # .grandfather_place_cousins and .cousin_flight are both not siblings
                for cousins_ in group_object.great_grand_cousin_flights_curves.values():
                    for cousin in cousins_.values():
                        cousin.greatgrandfather_place_cousins = cousins_.copy()
                        if False:# False = inclusive of cousin_self
                            cousin.greatgrandfather_place_cousins.remove(cousin) # inclusive of self or exclusive??
            tier_key = tier_key-1
    
    def combine_cousins_levels(self):
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            #print(f"hierarchy.combine_cousins_levels(): curve_object.name = {curve_object.name}")
            #curve_object.cousins_extended = curve_object.greatgrandfather_place_cousins.union(curve_object.grandfather_place_cousins) #set
            #curve_object.greatgrandfather_place_cousins.update(curve_object.grandfather_place_cousins) #dict
            #curve_object.cousins_extended = curve_object.greatgrandfather_place_cousins.copy()
            curve_object.cousins_extended=dict()
            try:
                curve_object.cousins_extended.update(curve_object.grandfather_place_cousins)
            except:
                print("\nIF YOU FAIL HERE IT IS LIKELY BECAUSE YOU HAVE NOT INCLUDED THE PROPER SUBGROUP NAMES\n")
                print(curve_object.name)
            curve_object.cousins_extended.update(curve_object.greatgrandfather_place_cousins)
            # there is another way to do this: these can be handled separately based on relevant stack (or cell hive), rather than combining them to be handled togather
    def grandfather_cousin_flight_assignment_subgroups(self):

        # stop trying to scale, go for the throat in a four tier paradigm
        #active_object.tier_object.tier_level == 2
    
        lowest_tier = max(self.dict_tier_objects.keys())
        secondary_alightment_tier = lowest_tier-2 # 1, in a four tier system
        tertiary_alightment_tier = secondary_alightment_tier - 1 
        #tier_key = tertiary_alightment_tier
        #tier_key = secondary_alightment_tier
        #while tier_key >=0: # better than not, but some unnecessary translation are applied, when the stack has not overlap but it is assumed that they do
        scene_object = self # hard code this junt
        tier_object = self.dict_tier_objects[1]
        sorted_objects = sorted(tier_object.dict_group_objects.values(), key=lambda obj: obj.place_in_supergroup)
        for group_object in sorted_objects:
        #for group_object in tier_object.dict_group_objects.values():
            #group_object.grand_cousin_flights_curves = dict() # intitialzed in constructor
            flight_key = 0
            assigned_cousins_count = 0 
            #dict_subgroups_diaspora mght be worth building, for scaling beyond four layers
            while assigned_cousins_count < len(group_object.dict_subgroups):
                for subgroup_object in group_object.dict_subgroups.values():
                    flight_key = subgroup_object.place_in_supergroup
                    if flight_key in scene_object.grand_cousin_flights_subgroups.keys(): 
                        #print(f'CALLED: {subgroup_object.name}')
                        #scene_object.grand_cousin_flights_subgroups[flight_key].add(subgroup_object) #set
                        scene_object.grand_cousin_flights_subgroups[flight_key][subgroup_object.name]=subgroup_object # dictionary
                        assigned_cousins_count+=1                 
                    else:
                        #print(f'ADDED: {subgroup_object.name}')
                        #scene_object.grand_cousin_flights_subgroups.update({flight_key:set()}) #set
                        #scene_object.grand_cousin_flights_subgroups[flight_key].add(subgroup_object) #set
                        scene_object.grand_cousin_flights_subgroups.update({flight_key:{}}) # dictionary
                        scene_object.grand_cousin_flights_subgroups[flight_key][subgroup_object.name]=subgroup_object # dictionary
                        assigned_cousins_count+=1

            # applies to curve_objects and subgroup_objects, as cousin objects
            for key,cousin_objects in scene_object.grand_cousin_flights_subgroups.items():
                #for cousin_object in scene_object.grand_cousin_flights_subgroups[key]:
                for cousin_object in cousin_objects.values():
                    cousin_object.cousin_flight = scene_object.grand_cousin_flights_subgroups[key].copy()
            
            # This is here: to be able to reference cousins from the object, rather from its parents
            # .grandfather_place_cousins might be the same as .cousin_flight 
            # .grandfather_place_cousins and .cousin_flight are both not siblings
            for cousins_ in scene_object.grand_cousin_flights_subgroups.values():
                for cousin in cousins_.values():
                    cousin.grandfather_place_cousins = cousins_.copy()
                    if False:# False = inclusive of cousin_self
                        cousin.grandfather_place_cousins.remove(cousin) # inclusive of self or exclusive??


    # we will also need place_cousin definitions for other levels..

    # aligning subgroups will have implications... donyt align the subgroup first, but rather find the subgroup as a stacked cousin and then align its curves
    def determine_longest_grandfather_place_cousin(self):
        #print('This is for the exploded axes')
        #print('Check stack directions, and check for relvance of cousing stack and sibling stack')
        #print('dash ticks may be needed instead of plus-ticks, in some cases.')
        #self._see_siblings_and_cousins()
        False
    
    def _see_siblings_and_cousins(self): 
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            print('\n')
            print(curve_object.name)

            print('curve_object.grandfather_place_cousins:')
            print(f'{len(curve_object.grandfather_place_cousins)}')
            for curve_object_ in curve_object.grandfather_place_cousins:
                print(curve_object_.name)
            print('curve_object.siblings:')
            print(f'{len(curve_object.siblings)}')
            for curve_object_ in curve_object.siblings:
                print(curve_object_.name)

    def print_hierarchy_tree(self):        
        self.step_through_hierarchy_by_lineage(lambda obj: print(obj.name))
    
    def print_hierarchy_tree_sibling(self):        
        self.step_through_hierarchy_by_lineage(lambda obj: print(f"object:{obj.name},{obj}; previous_sibling:{obj.previous_sibling}"))


    def charactertize_stack_for_siblings_and_cousins(self):
        # artifact from scene.py
        True

    def maybe_destroy_unassigned_curves(self):
        if self.user_input_object.keep_true_destroy_false_unassigned_curves is False:
            self.destroy_unassigned_curves()
        elif self.user_input_object.keep_true_destroy_false_unassigned_curves is True:
            self.assign_unassigned_curves_to_catchall_groups()

    def assign_unassigned_curves_to_catchall_groups(self):
        pass
    def destroy_unassigned_curves(self):
        pass