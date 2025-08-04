'''
Author: Clayton Bennett
Title: group
Created: 21 September 2023
Purpose: Create class that functions in Pavlov grouping hierarchy

Scale, translation, data object diameter, get, set

Fences should exist relative to the origin of the group
'''
import numpy as np

""" convert all group and curves dictionaries to sets. This way, keys will not confound names"""
class Group:

    #def __init__(self,scene_object=None,name="",tier_object=None):
    def __init__(self,scene_object=None,simple_name="",compound_subgroup_name="",tier_object=None):
        self.scene_object = scene_object
        self.style_object = self.scene_object.style_object 
        self.hierarchy_object = self.scene_object.hierarchy_object
        
        self.name = compound_subgroup_name
        
        self.secret_full_name = "null0-null1-null2-null3" # scene-Stiles-June, scene-Stiles, etc. number of hyphens should equal tier of group, ideally. scene-Maxson-June is different from scene-Stiles-June. Any dictionary keys athat need a name should use the group_object.secret_full_name. No keys might be better.
        #self.compound_subgroup_name = "supergroupname-selfsubgroupname"
        self.compound_subgroup_name = compound_subgroup_name
        self.simple_name = simple_name
        self.type = 'group_object'  
        self.translation_vector=[0,0,0] # 3 value list # relative to parentNode origin # not used as of 15 December 2023
        self.scale_vector=[1,1,1] # 3 value list
        self.rotation_vector = [0,0,0]
        self.supergroup = None
        self.dict_children=None
        self.dict_curve_objects = dict()
        self.dict_subgroups = dict()
        self.grand_cousin_flights_curves = dict()
        self.great_grand_cousin_flights_curves = dict()
        self.grand_cousin_flights_subgroups = dict()
        self.previous_sibling = None
        #self.dict_text_labels=None
        self.dict_text_labels = dict()
        self.fence_lines=None

        self.characteristic_length = None

        self.title_height_placement = 'floor'#'floating'#'floor' # floating
        self.shape_rectangular_or_radial = 'rectangular' # default

        self.max_raw_data = None #[0,0,0] # None is paradigm agnostic, escaping the 0-0-0 data origin paradigm
        self.min_raw_data = None #[0,0,0] # None is paradigm agnostic, escaping the 0-0-0 data origin paradigm
        self.min_time = None
        self.max_time = None
        self.min_height = None
        self.max_height = None
        self.min_depth = None
        self.max_depth = None

        self.tier_level = None # input from tier
        self.tier_object = None
        self.padding = [0,0,0]
        self.span_relative_to_scene_minimum_edge_at_zero_height_plane = [[None,None],[None,None],[None,None]] # set in translation, to be used in fences
        self.span = [[0,0],[0,0],[0,0]]
        #self.span_relative_to_supergroup_minimum_edge_at_zero_height_plane
        self.diameter = [0,0,0]

        self.dict_text_labels = dict()

        self.span_relative_to_self_data_origin = [[None,None],[None,None],[None,None]] 
        self.span_relative_to_self_minimum_edge_at_zero_height_plane = [[None,None],[None,None],[None,None]] 
        self.fence_span_relative_to_self_minimum_edge_at_zero_height_plane = [[None,None],[None,None],[None,None]] 
        self.span_relative_to_scene_minimum_edge_at_zero_height_plane = [[None,None],[None,None],[None,None]] 
        self.fence_span_relative_to_scene_minimum_edge_at_zero_height_plane = [[None,None],[None,None],[None,None]] 

        self.data_origin_relative_to_previous_sibling_data_origin = [None,None,None]
        self.data_origin_relative_to_supergroup_data_origin = [None,None,None]
        
    def add_subgroup(self, subgroup_object,key):
        
        self.dict_subgroups[key]=subgroup_object
        self.dict_children = {**self.dict_subgroups,**self.dict_curve_objects}
        subgroup_object.add_supergroup(self)
        self.secret_full_name = self.secret_full_name.replace("-null2-",f"-{subgroup_object.name}-")
        
    
    def apply_subgroup_object_span(self,subgroup_object):
        self.add_subgroup_values(subgroup_object)
    def add_subgroup_values(self,subgroup_object):
        # investigate max_values
        if self.max_raw_data is None:
            self.max_raw_data = subgroup_object.max_raw_data
        else:
            for i in range(3):
                if subgroup_object.max_raw_data[i]>self.max_raw_data[i]:
                    self.max_raw_data[i] = subgroup_object.max_raw_data[i]
                else:
                    print(f"subgroup_object.name = {subgroup_object.name}")
                    print(f"subgroup_object.max_raw_data = {subgroup_object.max_raw_data}")
                    print("UNEXPECTED-CONDITION:group.py,subgroup-has-no-maxrawdata")
                    
        # investigate min_values
        if self.min_raw_data is None:
            self.min_raw_data = subgroup_object.min_raw_data
        else:
            for i in range(3):
                #
                
                if subgroup_object.max_raw_data[i]<self.min_raw_data[i]:
                    self.min_raw_data[i] = subgroup_object.max_raw_data[i]

    def add_supergroup(self, supergroup_object):
        self.supergroup=supergroup_object
        #self.secret_full_name = self.secret_full_name.replace("-null1-",f"-{supergroup_object.name}-")
        self.compound_subgroup_name = self.compound_subgroup_name.replace("supergroupname",str(supergroup_object.name))
        self.compound_subgroup_name = self.compound_subgroup_name.replace("selfsubgroupname",str(self.name))


    def add_curve_object(self,curve_object,key):
        print("4.1: Group.add_curve_object(self,curve_object,key)")
        print(f"curve_object.key = {key}")
        self.secret_full_name = self.secret_full_name.replace("-null3",f"-{curve_object.name}") #
        self.dict_curve_objects[key]=curve_object
        self.dict_curve_objects[key].group = self
        self.dict_children = {**self.dict_subgroups,**self.dict_curve_objects}
        curve_object.add_supergroup(self)
        #self.hierarchy_object.dict_curve_objects_all[key.lower()]=curve_object #check use 30Jan
        self.hierarchy_object.dict_curve_objects_all.update({key.lower():curve_object})
        print(f"curve object {key} added to group {self.secret_full_name}")
    
    
    
    
    
    """APPLY THIS PATTERN BELOW ..... """
    def apply_curve_object_span(self, curve_object):
        # investigate max_values
        print(f"curve_object = {curve_object}")
        if self.max_raw_data is None:
            self.max_raw_data = [curve_object.raw.data_span[0][1],
                             curve_object.raw.data_span[1][1],
                             curve_object.raw.data_span[2][1]]
        else:
            for i in range(3):
                #expand the max_raw_data as necessary
                if curve_object.raw.data_span[i][1]>self.max_raw_data[i]:
                    self.max_raw_data[i] = curve_object.raw.data_span[i][1]
                else:
                    pass
                    #print("UNEXPECTED-CONDITION:group.py,curve-has-no-raw-data-span:")
                    #print("group, max raw data expanded")
                    #print(f"curve_object.name = {curve_object.name}")
                    #print(f"curve_object.max_raw_data = {curve_object.max_raw_data}")
        # investigate min_values
        if self.min_raw_data is None:
            self.min_raw_data = [curve_object.raw.data_span[0][0],
                             curve_object.raw.data_span[1][0],
                             curve_object.raw.data_span[2][0]]
        else:
            for i in range(3):
                if curve_object.raw.data_span[i][0]<self.min_raw_data[i]:
                    self.min_raw_data[i] = curve_object.raw.data_span[i][0]




    """ .... TO THIS FUNCION ...."""
    # ever called? No, apply_subgroup_object_span
    def apply_group_object_span(self,group_object):
        #self.dict_groups[key]=group_object
        self.dict_children = {**self.dict_subgroups,**self.dict_curve_objects}
        group_object.add_supergroup() # THIS
    def add_group_values(self,group_object):
        # investigate max_values
        if self.max_raw_data is None:
            self.max_raw_data = group_object.max_raw_data
        else:
            for i in range(3):
                if group_object.max_raw_data[i]>self.max_raw_data[i]:
                    self.max_raw_data[i] = group_object.max_raw_data[i]
                else:
                    print(f"group_object.name = {group_object.name}")
                    print(f"group_object.max_raw_data = {group_object.max_raw_data}")
                    print("UNEXPECTED-CONDITION:group.py,group-has-no-maxrawdata") 
        # investigate min_values
        if self.min_raw_data is None:
            self.min_raw_data = group_object.min_raw_data
        else:
            pass
            for i in range(3):
                if group_object.raw.data_span[i][0]<self.min_raw_data[i]:
                    self.min_raw_data[i] = group_object.raw.data_span[i][0]
        print("CRIPPLED SOCKET group.apply_group_object_span()")

        #problem: the tier 2 groups have a feaure that the tier 1 groups do not
        #tier 1 groups do not have .span_relative_to_self_data_origin

    """....Using the section below as reference."""
    """Start Section"""
    # #COPIED, FOR PATTERN RECOGNITION
    # def add_subgroup(self, subgroup_object,key):
    #     self.dict_subgroups[key]=subgroup_object
    #     self.dict_children = {**self.dict_subgroups,**self.dict_curve_objects}
    #     subgroup_object.add_supergroup()
    # def add_subgroup_values(self,subgroup_object):
    #     # investigate max_values
    #     if self.max_raw_data is None:
    #         self.max_raw_data = subgroup_object.max_raw_data
    #     else:
    #         for i in range(3):
    #             if subgroup_object.max_raw_data[i]>self.max_raw_data[i]:
    #                 self.max_raw_data[i] = subgroup_object.max_raw_data[i]
    #             else:
    #                 print(f"subgroup_object.name = {subgroup_object.name}")
    #                 print(f"subgroup_object.max_raw_data = {subgroup_object.max_raw_data}")
    #                 print("UNEXPECTED-CONDITION:group.py,subgroup-has-no-maxrawdata") 
    #     # investigate min_values
    #     if self.min_raw_data is None:
    #         self.min_raw_data = subgroup_object.min_raw_data
    #     else:
    #         pass
    #         #for i in range(3):
    """ END Section """

    def padding_assignment(self):
        # the padding for the supergroup matters more
        # called in scene.build_groups_and_tiers_etc()
        # maybe use diameter instead of data...
        if self.style_object.redundant_padding is True:
            self.padding = [max(self.max_raw_data)*self.style_object.padding_coefficient,# where is padding coefficient calculated? manually set to 0.3 in scene_object. could be a userInput_element
                            max(self.max_raw_data)*self.style_object.padding_coefficient,
                            max(self.max_raw_data)*self.style_object.padding_coefficient]
        elif self.style_object.redundant_padding is False:
            self.padding = [self.max_raw_data[0]*self.style_object.padding_coefficient,
                            self.max_raw_data[1]*self.style_object.padding_coefficient,
                            self.max_raw_data[2]*self.style_object.padding_coefficient]
        # override
        if self.style_object.group_padding_supressed is True:
            self.padding = [0,0,0]
        
        if self.style_object.universally_consistent_padding is True:
            self.padding = self.style_object.padding

        
        return True        

    def set_diameter(self,diameter):
        # diameter for the group comes from the diameters of each curve, plus the padding. 
        # this is handled in translation.py
        # how are label elements factored in?
        self.diameter = diameter
        #print(self.name,self.diameter)


    def calculate_span_13April24(self,span_relative_to_self_stage1_minimum_edge_at_zero_height_plane,vector_data_origin_relative_to_stage1_minimum_edge_at_zero_height_plane):
        #vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane = np.array([0,0,0])
        # thhis shit is incompatible with transition_data_sligned.py
        # this is where i build my church
        # "lighten up while you still can. don't even try to understand. just find a place to make your stand, and take it easy"
        
        # pick up where we left off. things get wonky, we'll  ned to updte

        """ for key,element in self.dict_text_labels.items():
        #for key,text_label in self.dict_text_labels:
            #element.characters_array
            #chart_element = chart_element_class(name=key ,coords = None)
            #chart_element.convert_text_label_to_a_chart_element(text_label)
            #text_label.element_span_relative_to_parent_data_origin # assessed in text_label.py
            # problem, changes every time in the loop
            span_relative_to_self_stage2_minimum_edge_at_zero_height_plane,\
            vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane = \
                self.update_group_span_based_on_element_span_relative_to_parent_stage1_minimum_edge_at_zero_height_plane
                
                (span_relative_to_self_stage1_minimum_edge_at_zero_height_plane,
            vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane,
            element_span_relative_to_parent_minimum_edge_at_zero_height_plane = element.element_span_relative_to_parent_minimum_edge_at_zero_height_plane)
            """
        # update these:::::::::::: WORK HERE
        # diameter
        #span_relative_to_self_minimum_edge_at_zero_height_plane
        # minimum_corner_origin_relative_to_self_minimum_edge_at_zero_height_plane
        
        span_relative_to_self_stage2_minimum_edge_at_zero_height_plane,\
        vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane =\
              self.update_group_span_based_on_padding(span_relative_to_self_stage2_minimum_edge_at_zero_height_plane,
                vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane)
        

        """  #self.calculate_diameter()
        #self.set_relative_vectors_data_aligned(span_relative_to_self_data_origin = self.span)
        self.set_relative_vectors(span_relative_to_self_stage2_minimum_edge_at_zero_height_plane,
                                  vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane,
                                  vector_data_origin_relative_to_stage1_minimum_edge_at_zero_height_plane) 
        self.calculate_diameter(span_relative_to_self_stage2_minimum_edge_at_zero_height_plane)
        print(self.name,self.span_relative_to_self_minimum_edge_at_zero_height_plane)
        return vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane """
 
    def update_group_span_based_on_element_span_relative_to_parent_stage1_minimum_edge_at_zero_height_plane(self,span_relative_to_self_stage1_minimum_edge_at_zero_height_plane,
                                                                                                            vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane,
                                                                                                     element_span_relative_to_parent_minimum_edge_at_zero_height_plane):

        # we need stage of reference points for expansion. after each expansion, the span relative to the data origin, span relative to the minimum edge at zero height plane,and the span relative to minimum corener origin should all be updated 
        
        # element_span_relative_to_parent_data_origin means something different for groups...
        #called in group.calculate_span...
        #span = self.span
        span = span_relative_to_self_stage1_minimum_edge_at_zero_height_plane
        for i in range(3):

            # This first half, j=0, looks at the negative side of span.
            j=0
            if span[i][j]>element_span_relative_to_parent_minimum_edge_at_zero_height_plane[i][j]:
                span[i][j]=element_span_relative_to_parent_minimum_edge_at_zero_height_plane[i][j]
                
                
            # This second half, j=1, looks at the positive side of span.
            j=1
            if span[i][j]<element_span_relative_to_parent_minimum_edge_at_zero_height_plane[i][j]:
                span[i][j]=element_span_relative_to_parent_minimum_edge_at_zero_height_plane[i][j]

        span_relative_to_self_stage2_minimum_edge_at_zero_height_plane,vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane = self.convert_negative_span_for_minimum_edge_at_zero_height_plane(span,vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane)
        
        return span_relative_to_self_stage2_minimum_edge_at_zero_height_plane,vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane

    def update_group_span_based_on_padding(self,span):
        if all(self.padding != np.array([0,0,0])):
            outer_buffer = [[-self.padding[0],self.padding[0]],
                            [-self.padding[1],self.padding[1]],
                            [-self.padding[2],self.padding[2]]] # stays zero, because padding is [0,0,0]

            self.span = self.span + outer_buffer # zer
            span = span + outer_buffer # zer
        
        return span

    """ def set_relative_vectors(self,span_relative_to_self_minimum_edge_at_zero_height_plane,
                             vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane,
                             vector_data_origin_relative_to_stage1_minimum_edge_at_zero_height_plane):
        print(f'span_relative_to_self_minimum_edge_at_zero_height_plane = {span_relative_to_self_minimum_edge_at_zero_height_plane}')
        print(f'vector_data_origin_relative_to_stage1_minimum_edge_at_zero_height_plane = {vector_data_origin_relative_to_stage1_minimum_edge_at_zero_height_plane}')
        print(f'vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane = {vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane}')

        # change all this! for groups to win, big
        vector_data_origin_relative_to_stage2_minimum_edge_at_zero_height_plane =\
            vector_data_origin_relative_to_stage1_minimum_edge_at_zero_height_plane + vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane
        self.span_relative_to_self_minimum_edge_at_zero_height_plane = span_relative_to_self_minimum_edge_at_zero_height_plane
        
        # wrong
        #self.minimum_corner_origin_relative_to_self_data_origin = np.array([span_relative_to_self_minimum_edge_at_zero_height_plane[0][0],span_relative_to_self_minimum_edge_at_zero_height_plane[1][0],span_relative_to_self_minimum_edge_at_zero_height_plane[2][0]])
        ##self.minimum_edge_at_zero_height_plane_relative_to_self_data_origin = np.array([span_relative_to_self_minimum_edge_at_zero_height_plane[0][0],
        ##                                                                                0,
        ##                                                                                span_relative_to_self_minimum_edge_at_zero_height_plane[2][0]])
        
        #self.data_origin_relative_to_self_minimum_edge_at_zero_height_plane = np.multiply(-1,self.minimum_edge_at_zero_height_plane_relative_to_self_data_origin)
        #self.data_origin_relative_to_self_minimum_corner_origin = np.multiply(-1,self.minimum_corner_origin_relative_to_self_data_origin)
            
        self.data_origin_relative_to_self_minimum_edge_at_zero_height_plane = vector_data_origin_relative_to_stage2_minimum_edge_at_zero_height_plane
        # self.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane # set in translation.py

        self.minimum_edge_at_zero_height_plane_relative_to_self_minimum_corner_origin = -np.multiply(-1,[self.span_relative_to_self_minimum_edge_at_zero_height_plane[0][0],self.span_relative_to_self_minimum_edge_at_zero_height_plane[1][0],self.span_relative_to_self_minimum_edge_at_zero_height_plane[2][0]])

        self.calculate_diameter(span_relative_to_self_minimum_edge_at_zero_height_plane) """


    def calculate_diameter(self,span_relative_to_some_origin):
        self.diameter[0]=span_relative_to_some_origin[0][1]-span_relative_to_some_origin[0][0]
        self.diameter[1]=span_relative_to_some_origin[1][1]-span_relative_to_some_origin[1][0]
        self.diameter[2]=span_relative_to_some_origin[2][1]-span_relative_to_some_origin[2][0]
        #print(self.name,self.diameter)
        return True#self._diameter
    
    def convert_negative_span_for_minimum_corner_origin(self,span_relative_to_some_origin):#filthy monkey patch
        span_relative_to_self_minimum_corner_origin = np.array([[None,None],
                                                                            [None,None],
                                                                            [None,None]])
        for i in range(3):
            #for j in range(2):
            span_relative_to_self_minimum_corner_origin[i][0] = 0   
            span_relative_to_self_minimum_corner_origin[i][1] = span_relative_to_some_origin[i][1]-span_relative_to_some_origin[i][0]

        return span_relative_to_self_minimum_corner_origin
    
    def convert_negative_span_for_minimum_edge_at_zero_height_plane(self,span_relative_to_some_origin,
                                                                    vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane):#filthy monkey patch
        span_relative_to_self_minimum_edge_at_zero_height_plane = np.array([[None,None],
                                                                            [None,None],
                                                                            [None,None]])
        i=0 # time
        #for j in range(2):
        vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane[i] = span_relative_to_some_origin[i][0]

        span_relative_to_self_minimum_edge_at_zero_height_plane[i][0] = 0   
        span_relative_to_self_minimum_edge_at_zero_height_plane[i][1] = span_relative_to_some_origin[i][1]-span_relative_to_some_origin[i][0]

        i=1 # height
        #for j in range(2):
        span_relative_to_self_minimum_edge_at_zero_height_plane[i][0] = span_relative_to_some_origin[i][0]
        span_relative_to_self_minimum_edge_at_zero_height_plane[i][1] = span_relative_to_some_origin[i][1]

        i=2 # depth
        #for j in range(2):
        vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane[i] = span_relative_to_some_origin[i][0]

        span_relative_to_self_minimum_edge_at_zero_height_plane[i][0] = 0   
        span_relative_to_self_minimum_edge_at_zero_height_plane[i][1] = span_relative_to_some_origin[i][1]-span_relative_to_some_origin[i][0]

        return span_relative_to_self_minimum_edge_at_zero_height_plane,vector_stage1_minimum_edge_at_zero_height_plane_relative_to_stage2_minimum_edge_at_zero_height_plane

