'''
Author: Clayton Bennett
Title: curve
Created: 21 September 2023
Purpose: Create class that functions in Pavlov grouping hierarchy

Scale, translation, data object diameter, get, set

classes:
https://www.geeksforgeeks.org/getter-and-setter-in-python/
https://docs.python.org/3/tutorial/classes.html

primitives:
https://www.codingdojo.com/blog/top-python-data-structures#:~:text=The%20four%20primitive%20data%20structures,tuples%2C%20dictionaries%2C%20and%20sets.


new origin paradigm, useful guidance
#_supergroup_data_origin  does not exist
#scene_data_origin  does not exist
#scene_radial_origin  is the same as scene_minimum_corner_origin, and both are referred to as scene_origin
# "radial_origin" means center of the span, wherever it is determined
# "minimum_corner_origin" means the corner of the span with the values closest the scene origin
# "data_origin" means the 0,0,0 point of the imported data that belongs to curve_object. The data_origin may or may not be "on your screen".

'''
import numpy as np
#from chart_element import chart_element as chart_element_class 

class Curve:
    
    scene_object = None
    style_object = None
    user_input_object = None
    hierarchy_object = None

    @classmethod
    def pass_in_scene_object(cls, scene_object):
        cls.style_object = scene_object.style_object
        cls.scene_object = scene_object
        cls.user_input_object = scene_object.user_input_object
        cls.hierarchy_object = scene_object.hierarchy_object


    def __init__(self,name=""):
        print(f"Generating curve object: {name}")
        self.name = name.lower()
        self.secret_full_name = "null0-null1-null2-null3"
        self.span = np.array([[0.0,0.0],[0.0,0.0],[0.0,0.0]])

        self.dict_chart_elements = dict()

        self.tier_object = None
        self.diameter = [0,0,0] # for now
        self.place_in_supergroup = None
        self.previous_object = None
        self.title_height_placement = 'floor'

        self.tick_halflength_THD = [0,0,0]
        
        #self.axis_origin_relative_to_self_minimum_edge_at_zero_height_plane = None

        self.supergroup = None
        self.type = 'curve_object'

        self.shape_rectangular_or_radial = 'rectangular' # default
        self.header_time = None
        self.header_height = None
        self.header_depth = None
        self.df_metadata = None

        self.axis_array = None
        self.axes_arrays = None
        self.ticks_arrays = None
        
        
        self.dict_children = None # should stay this way
        self.i_ = None
        self.title_object = None
        self.dict_text_labels = dict()
        self.dict_tick_numbering = dict()
        self.fence_lines = None
        self.dict_datapoints = dict()
        self.dict_data_vectors_raw = dict()
        self.dict_data_vectors_scaled = dict()
        self.dict_color_coeff = None # will be initialized to dict() later

        self.axis_length_list_THD = None
        self.characteristic_length = None

        self.scale_vector = [1,1,1] # 3 value vector/list # should be the same for all objects. Just transmits to data_vectors
        self.translation_vector = [0,0,0] # applies relative to scene origin, as opposed to object origin?
        self.span_relative_to_self_data_origin = None # sam as self.span, once it is set 
        self.span_relative_to_scene_minimum_edge_at_zero_height_plane = None # set in translation.py after stacking
        # this is all for the classic 6-element span approach
        # this stuff isn't currently used to impact or control the title_labels
        # is is included in the vectors/spacing/padding/translation of the curve objects?
        # do they impact span? fence location? diameter?
        # THey should only impact something when they also control something.
        self.data_thickness = [[0,0],[0,0],[0,0]]
        self.title_thickness = [[0,0],[0,0],[0,0]]
        self.ticks_thickness = [[0,0],[0,0],[0,0]]         
        self.pre_title_buffer = [[0,0],[0,0],[0,0]] # before the title
        self.title_translation_vector = [0,0,0] # this is here so that the title can be generated relative to its own origin, and then the origin relative to the 0-0-0 data center can be added later.

        self.axisLabels_thickness = [[0,0],[0,0],[0,0]] # stays zero
        self.ticks_buffer = [[0,0],[0,0],[0,0]] # stays zero
        self.pre_axisLabels_buffer = [[0,0],[0,0],[0,0]] # stays zero
        self.outer_buffer = [[0,0],[0,0],[0,0]] # stays zero
        #self.padding = np.array([0.0,0.0,0.0]) # stays zero
        self.padding = np.array([0,0,0]) # stays zero

        self.plane_alignment_padding = [0,0,0] # for aligning planes for analsis based on stack direction, applied to the non-stacked direction that isn't height.
        # deal with this in translation, or so. make it an (prefered align_plane = True) option in style_object
        self.first_child = None # stays None
        self.previous_sibling = None

        self.max_raw_data = None # 01 January 2025 CB
        self.min_raw_data = None # 01 January 2025 CB

        self.data_origin_relative_to_previous_sibling_data_origin = [None,None,None]

    def add_headers(self,
                 header_time='',
                 header_height='',
                 header_depth = ''):
        self.header_time = header_time
        self.header_height = header_height
        self.header_depth = header_depth

    def add_curve_object_to_hierarchy_object(self): #check use 30Jan
        self.hierarchy_object.dict_curve_objects_all.update({self.name.lower():self}) 

    def add_raw_data(self,raw_time,
                    raw_height,
                    raw_depth):
        self.min_time = min(raw_time)
        self.max_time = max(raw_time)
        self.min_height = min(raw_height)
        self.max_height = max(raw_height)
        self.min_depth= min(raw_depth)
        self.max_depth = max(raw_depth)
        self.min_data = [self.min_time,self.min_height,self.min_depth]

        self.raw = self.Raw(raw_time, raw_height, raw_depth)
        # these vectors are for scaling
        self.time = raw_time
        self.height = raw_height
        self.depth = raw_depth
        self.halfwidth_time = None

        self.tick_numbering = None

        ###self.calculate_span() # this thing matters
        if self.style_object.curve_positive_axes_only is True:# only current approach
            self.axis_length_list_THD = [abs(self.max_time),abs(self.max_height),abs(self.max_depth)] # assumes 0-0-0 data paradigm
            self.characteristic_length = self.axis_length_list_THD[0]
        else:
            print('Negative coordinate region not planned for')
            # This logic is not meant to run
            # It is here to demonstrate a key assumption, which could hypothetically be superceded
            # 
            # This will be superceded with the rise of multiple access scaling for homogenous curve spatialz size

        self.padding_assignment()
        return

    def update_ticks_thickness(self,span_adjust): # is there a way to generalize this to any span/buffer/tickness array?
        # set the most negative values to the defacto
        # used! in ticks.py. Not to set a buffer but just to ticks.
        # This refers to ticks_thickness beyond the previous span, i.e. doesn't include the side of the tick which enter the plot region which are already within the span

        # Ah! this says, there is no need to increase the span due to ticks, IF it is already larger because of data.
        # Wait. That's what i want it to do. But it doesn't. It just chucks in an additonal span increase, regardless.
        # It only works out fine because the data has already contributed. But span doesn't need to contribute if it expands beyond the ticks.
        # There was a version of code in the past that handled this, but it was probably phased out and has since been removed in a culling of outdated comment.
        # Look back at old versions from October 2023 to December 2023
        for i in range(3):
            # This first half, j=0, looks at the negative side of span, which is 6-value array, with positive and negative values for each dimension.
            j=0
            if self.ticks_thickness[i][j]>span_adjust[i][j]:
                self.ticks_thickness[i][j]=span_adjust[i][j]
                
            # This second half, j=1, looks at the positive side of span.
            # This probably never has an impact. But, shit, it just adds it without checking.
            # This should be improved. Look at old versions.
            j=1
            if self.ticks_thickness[i][j]<span_adjust[i][j]:
                self.ticks_thickness[i][j]=span_adjust[i][j]
                

    """ def update_pre_axisLabel_buffer(self,span_adjust):
        # Set the most extreme values to the defacto
        # basically, this is checking if the value has already been assigned to the pre_axisLabel_buffer, which is initialized as [[0,0],[0,0],[0,0]]
        # Check into the pLB values and the character_factor_span calculation and usage.
        # Those were from the wild west pre-OOP days.
        for i in range(3):

            # This first half, j=0, looks at the negative side of span.
            j=0
            if self.pre_axisLabels_buffer[i][j]>span_adjust[i][j]:
                self.pre_axisLabels_buffer[i][j]=span_adjust[i][j]
            # This second half, j=1, looks at the positive side of span.
            j=1
            if self.pre_axisLabels_buffer[i][j]<span_adjust[i][j]:
                self.pre_axisLabels_buffer[i][j]=span_adjust[i][j] """

    def update_curve_span_based_on_element_span(self,element_span_relative_to_parent_data_origin):
        #called in curve.calculate_span...

        # Set the most extreme values to the defacto
        # basically, this is checking if the value has already been assigned to the pre_axisLabel_buffer, which is initialized as [[0,0],[0,0],[0,0]]
        # Check into the pLB values and the character_factor_span calculation and usage.
        # Those were from the wild west pre-OOP days.

        for i in range(3):

            # This first half, j=0, looks at the negative side of span.
            j=0
            if self.span[i][j]>element_span_relative_to_parent_data_origin[i][j]:
                self.span[i][j]=element_span_relative_to_parent_data_origin[i][j]
            # This second half, j=1, looks at the positive side of span.
            j=1
            if self.span[i][j]<element_span_relative_to_parent_data_origin[i][j]:
                self.span[i][j]=element_span_relative_to_parent_data_origin[i][j]

    def update_curve_span_based_on_padding(self):
        #print(f'self.padding = {self.padding}')
        if all(self.padding != np.array([0,0,0])):
        #print(f'sum(self.padding) = {sum(self.padding)}')
        #if sum(self.padding) == 0.0:
            
            outer_buffer = [[-self.padding[0],self.padding[0]],
                            [-self.padding[1],self.padding[1]],
                            [-self.padding[2],self.padding[2]]] # stays zero, because padding is [0,0,0]

            self.span = self.span + outer_buffer # zer

    def padding_assignment(self):
        # the padding for the supergroup matters more
        # called in scene.build_groups_and_tiers_etc()
        # maybe use diameter instead of data...
        
        if self.style_object.universally_consistent_padding is True:
            self.padding = self.style_object.padding
        return True

    def calculate_diameter(self):
        # in data objects, span is set first and then diameter 
        # in groups, maybe it is the other way around?
        # how (and when) do you add labels and buffers to groups?
        self.diameter[0]=self.span[0][1]-self.span[0][0]
        self.diameter[1]=self.span[1][1]-self.span[1][0]
        self.diameter[2]=self.span[2][1]-self.span[2][0]
        return True#self._diameter

    def get_span(self):
        return self.span
        #return [[self.min_time,self.max_time],[self.min_height,self.max_height],[self.min_depth,self.max_depth]]


    
    def calculate_span_10April24(self):
        # this is where i build my church
        # "lighten up while you still can. don't even try to understand. just find a place to make your stand, and take it easy"

        # create pointcloud or pointcloud_coords as a shared variabvle, rahter than ".characters_array" and ".coords"
        # with this in mind, consider adding an embedded hierachy label to the axis coords.
        # how can we incorportation padding and curve data into this scheme? give them their own loops for now, but ultimately we want them all (well maybe not padding) included as equal members in a dictionary: "dict_chart_elements", or whatever 
        for key,element in self.dict_text_labels.items():
            #element.characters_array
            #chart_element = chart_element_class(name=key ,coords = None)
            #chart_element.convert_text_label_to_a_chart_element(text_label)
            #text_label.element_span_relative_to_parent_data_origin # assessed in text_label.py
            self.update_curve_span_based_on_element_span(element_span_relative_to_parent_data_origin = element.element_span_relative_to_parent_data_origin)

        for key,element in self.dict_chart_elements.items():
            #element.coords
            #element.element_span_relative_to_parent_data_origin
            self.update_curve_span_based_on_element_span(element_span_relative_to_parent_data_origin = element.element_span_relative_to_parent_data_origin)

        # update based on data 
        #self.update_curve_span_based_on_element_span(element_span_relative_to_parent_data_origin = self.raw.data_span)
        if False:
            span = self.raw.data_span
        else:
            span = [[self.min_time,self.max_time],
            [self.min_height,self.max_height],  
            [self.min_depth,self.max_depth]] 
             

        self.update_curve_span_based_on_element_span(element_span_relative_to_parent_data_origin = span)


        self.update_curve_span_based_on_padding()

        self.calculate_diameter()
        self.set_minimum_edge_at_zero_height_plane_relative_to_self_data_origin(span_relative_to_self_data_origin = self.span)
        return True
        
    def add_supergroup(self, group_object):
        self.supergroup=group_object

    def set_axis_array(self,axis_array):
        self.axis_array = axis_array

    def set_axes_array(self,axes_arrays):
        self.axes_arrays = axes_arrays

    def set_ticks_arrays(self,ticks_arrays):
        self.ticks_arrays = ticks_arrays

    def set_minimum_edge_at_zero_height_plane_relative_to_self_data_origin(self,span_relative_to_self_data_origin):
        
        self.span_relative_to_self_data_origin = np.array(span_relative_to_self_data_origin)

        self.minimum_corner_origin_relative_to_self_data_origin = np.array([span_relative_to_self_data_origin[0][0],span_relative_to_self_data_origin[1][0],span_relative_to_self_data_origin[2][0]])
        self.minimum_edge_at_zero_height_plane_relative_to_self_data_origin = np.array([span_relative_to_self_data_origin[0][0],
                                                                                        0,
                                                                                        span_relative_to_self_data_origin[2][0]])
        self.data_origin_relative_to_self_minimum_edge_at_zero_height_plane = np.multiply(-1,self.minimum_edge_at_zero_height_plane_relative_to_self_data_origin)
        self.data_origin_relative_to_self_minimum_corner_origin = np.multiply(-1,self.minimum_corner_origin_relative_to_self_data_origin)
        # self.minimum_edge_at_zero_height_plane_relative_to_scene_minimum_edge_at_zero_height_plane # set in translation.py
        
    ''' inner classes'''
    class Raw:
        # the purpose of this is to protect raw values from migration
        # "metadata" is a misnomer. This call could be called "protect" or "raw"
        def __init__(self,raw_time, raw_height, raw_depth):
            self.length = [None,None,None]
            self.data_span = [[],[],[]]
            self._raw_time = None
            self._raw_height = None
            self._raw_depth = None
            self.set_metadata(raw_time,raw_height,raw_depth)

        def set_metadata(self,raw_time,raw_height,raw_depth):
            self._raw_time = raw_time
            self._raw_height = raw_height
            self._raw_depth = raw_depth
            self.data_span = [[min(raw_time),max(raw_time)],
                    [min(raw_height),max(raw_height)],
                    [min(raw_depth),max(raw_depth)]]
            return
        @property
        def raw_time(self):
            return self._raw_time
        @raw_time.setter
        def raw_time(self,vector):  
            if self._raw_time is not None:
                raise Exception("metadata.raw_time can only be set once")
            else:
                self._raw_time = vector
                self.length[0] = len(vector)
        @property
        def raw_height(self):
            return self._raw_height
        @raw_height.setter
        def raw_height(self,vector):
            if self._raw_height is not None:
                raise Exception("metadata.raw_height can only be set once")
            else:
                self._raw_height = vector
                self.length[2] = len(vector)
        @property
        def raw_depth(self):
            return self._raw_depth
        @raw_depth.setter
        def raw_depth(self,vector):
            if self._raw_depth is not None:
                raise Exception("metadata.raw_depth can only be set once")
            else:
                self._raw_depth = vector
                self.length[2] = len(vector)
