'''
Author: Clayton Bennett
Created: 14 October 2023
Title: ticks.py

Purpose: Provide tick marks to axes, based on number of ticks (n_ticks) as an input.
Inputs: n_ticks, max(vector)

for now, use 0 as the datum
set length of ticks to be 5% the length of the axis - subject to change, other scalability algorithms, and possibly (deep) preferences, but not now

axis_coords is comprised of three vectors
example: time_axis_coords = [0,max(vectorArray_time[i])],[0,0],[0,0]

for now abandon the generalize ticks module, develop ticks_time and ticks_height. ignore depth for the time being, though it should work with the current algorithm.

# place a tick at each extreme, if n_ticks is more than 1
# if n_ticks == 1, place a single tick at the average
# if n_ticks < 1, return an empty list for ticks

should we aim for whole number ticks?

Add modules for identical yet orthogonal ticks.
Naming convention for tick coordinate modules:
ticks_depth_coords_T are ticks along the depth axis that have their endpoints at two different values in the time direction.
ticks_time_coords_H are ticks along the time axis that have their endpoints at two different values in the height direction.

ticks_depth_2D_redundant should not have tick marks, because they will be innacurate...or, it should feed in the percentage multiplier by which the force (Height) dimension is copied to the depth dimension.

Generalize the module - because, the basic input for every axis should be the same, and the outputs should be in the same format and order
# should be able to feed and generate with partial data? some curve_objects being 5D and some curve_objects being 3D...
Inputs: axis_length_Time, axis_length_Height, axis_length_Depth, number of ticks (inherent to class), tick_length (inherent to class)

Use column swapping to create all three directions of control points
a = [[0,1,2],[3,4,5],[6,7,8]]
a=np.array(a)
a[:, [1, 0]] = a[:, [0, 1]]
a[:, [1, 2]] = a[:, [2, 1]]

# move this to a class/module!!! 24 January 2024

[text_name,time_coords,height_coords,depth_coords] = line_array
# example: line_array = ['Axis, Time',[0,1],[2,3],[4,5]]
text_name will generally be either 'Axis' or 'Tick'
n_ticks = number of tick marks along axis
create all axes first, then create all ticks, then combine these lists for a general line list
These lists cannot be appended as single chunks - each indexed array must be combined, so that they can be referenced

what if the line name is not simply str(line_array) = "['Axis, Time',[0,1],[2,3],[4,5]]", but rather has a dedicated presentation name, whcih references only the prevailing value, i.e. "1.23 seconds". This is less general, but it is good for ticks. What if the mesh name is str(line_array), and the node name is the presentation version. That way the user has access to the pretty version and the raw version.



For now, give me Axes, then add ticks.
Then, text library, then text lines, with word nodes.
As of 14 October 2023, this will be deigned to work prior to rotation, in the basic THD orientation, and rotation may be applied later

# axis and ticks should really be made in a module, not in main

26 June 2024
style_object.only_longest_axes_ticks_siblings_and_cousins
based on curve_object.siblings, etc
curve_object.grandfather_place_cousins
'''

#texts_array = [] # totally separate, refeed, add input to createFBX_ modules for text.

#['Axis, Example',[0,0],[0,0],[0,0]]
#['Tick, Example',[0,0],[0,0],[0,0]]

import numpy as np
from src.chart_element import ChartElement

tick_length_ratio = 0.05
class Ticks:
    style_object = None
    scene_object = None
    hierarchy_object = None
    @classmethod
    def assign_style_object(cls,style_object):
        cls.style_object = style_object
    @classmethod
    def assign_hierarchy_object(cls,hierarchy_object):
        cls.hierarchy_object = hierarchy_object
    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object = scene_object
        cls.assign_style_object(scene_object.style_object)
        cls.assign_hierarchy_object(scene_object.hierarchy_object)

    def __init__(self):
        self.name = 'ticks'
        #self.minimum_axis_length = None
        #self.minimum_axis_length_time = None   
        #self.tick_size = None

        
    def determine_consistent_tick_size(self):
        minimum = self.find_minimum_axis_length_time()
        tick_size = tick_length_ratio * minimum
        return tick_size

    def find_minimum_axis_length_time(self):
        curve_object = next(iter(self.hierarchy_object.dict_curve_objects_all.values()))
        #minimum = curve_object.max_time#initialize
        minimum = max(curve_object.dict_data_vectors_scaled["time"])
        
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            if max(curve_object.dict_data_vectors_scaled["time"]) < minimum:
                minimum = max(curve_object.dict_data_vectors_scaled["time"])
                #print(f'minimum = {minimum}')
        return minimum


    def generate_ticks(self):
        #defunct
        # these ticks vary in length

        #Inputs: axis_length_Time, axis_length_Height, axis_length_Depth, number of ticks (inherent to class), tick_length (inherent to class)

        n_ticks = 5 # tie this to preferences page in the GUI
        tick_length_ratio = 0.05 # custom setting ratio of axis length
        tick_length_ratio_redundantAxis = 0.06 # 0.09 # 0.15
        axes_arrays = [] # all line_array instances in all lines_array instances

        for i in range(len(self.scene_object.vectorArray_time)):
            curve_object = self.hierarchy_object.dict_curve_objects_all[self.scene_object.names[i]]
            # if there is an error here, it probably means that hierarchy_object.dict_curve_objects_all was non populated in the import plugin
            
            lines_array = []
            axes_arrays = []
            ticks_arrays = []

            #''Time''
            #time_axis_length = curve_object.axis_length_list_THD[0] # Paradigm agnostic,set in curve_object.__init__ constructor.
            time_axis_length = max(curve_object.dict_data_vectors_scaled["time"])
            time_axis_coords = np.array([[0,0,0],
                                [time_axis_length,0,0], # Only references positive values # There should be a paradigm agnostic way to do this, which this is not currently
                                [0,0,0]]) # Why is this like this? Answer: Remember: When defining lines or shapes, it is best practice to return to the initial point when defining control points for FBX construction.
            
            name = 'Axis: '+self.scene_object.headers_time[i]+"_"
            axis_array = [name]
            axis_array.append(time_axis_coords)
            
            
            axes_arrays.append(axis_array)
            lines_array.append(axis_array)
            chart_element_object = ChartElement(name = name,coords = time_axis_coords)
            chart_element_object.set_span_for_axis()
            curve_object.dict_chart_elements.update({name:chart_element_object})
            # work here, 2 April 2024
            
            axis_direction_THD = [1,0,0]
            ticks_array = self.ticks(curve_object,n_ticks, time_axis_length, self.scene_object.headers_time[i],axis_direction_THD,tick_length_ratio)
            ticks_arrays.extend(ticks_array)
            lines_array.extend(ticks_array)


            #'' Height''
            #height_axis_length = max(self.scene_object.vectorArray_height[i])
            height_axis_length = max(curve_object.dict_data_vectors_scaled["height"])
            height_axis_coords = np.array([[0,0,0], 
                                [0,height_axis_length,0],# Not paradigm agnostic, assumes 0-0-0 data origin.
                                [0,0,0]])
            name_axis = 'Axis: '+self.scene_object.headers_height[i]+"_"
            axis_array = [name]
            axis_array.append(height_axis_coords)
            axes_arrays.append(axis_array)
            lines_array.append(axis_array)
            
            axis_direction_THD = [0,1,0]
            ticks_array = self.ticks(curve_object,n_ticks, height_axis_length, self.scene_object.headers_height[i],axis_direction_THD,tick_length_ratio)
            ticks_arrays.extend(ticks_array)
            lines_array.extend(ticks_array)
            chart_element_object = ChartElement(name = name,coords = height_axis_coords)
            chart_element_object.set_span_for_axis()
            curve_object.dict_chart_elements.update({name:chart_element_object})
            curve_object.ticks_array

            #''Depth''
            #depth_axis_length = max(self.scene_object.vectorArray_depth[i])
            depth_axis_length = max(curve_object.dict_data_vectors_scaled["depth"])
            depth_axis_coords = np.array([[0,0,0],
                                [0,0,depth_axis_length],# Not paradigm agnostic, assumes 0-0-0 data origin.
                                [0,0,0]])
            name = 'Axis: '+self.scene_object.headers_depth[i]+"_"
            axis_array = [name]
            axis_array.append(depth_axis_coords)
            axes_arrays.append(axis_array)
            lines_array.append(axis_array)
            chart_element_object = ChartElement(name = name,coords = depth_axis_coords)
            chart_element_object.set_span_for_axis()
            curve_object.dict_chart_elements.update({name:chart_element_object})
            
            #ticks_arrays=[]
            axis_direction_THD = [0,0,1]
            # ticks are not built for styles not declared here
            if self.style_object.consistent_tick_size is True:
                ticks_array = self.ticks(curve_object,n_ticks, depth_axis_length, self.scene_object.headers_depth[i],axis_direction_THD,tick_length_ratio)
                lines_array.extend(ticks_array)
                ticks_arrays.extend(ticks_array)
            """
            elif self.style_object.styleChoice_depth00 == 'depth':
                ticks_array = self.ticks(curve_object,n_ticks, depth_axis_length, self.scene_object.headers_depth[i],axis_direction_THD,tick_length_ratio)
                lines_array.extend(ticks_array)
                ticks_arrays.extend(ticks_array)
            elif self.style_object.styleChoice_depth00 == 'depthByHeight_coeff':
                ticks_array = self.ticks_redundant(curve_object,n_ticks, depth_axis_length, self.scene_object.headers_depth[i],axis_direction_THD,tick_length_ratio_redundantAxis,self.style_object.depthByHeight_coeff)
                lines_array.extend(ticks_array)
                ticks_arrays.extend(ticks_array) """
            #elif self.style_object.styleChoice_depth00 == 'depth':
            

            # once this is done, it is hard to know the different between which entries are axis and which are ticks, without parsingthe labels. OOP would be better.
            axes_arrays.append(lines_array) # all axes for all data objects
            curve_object.set_axis_array(lines_array)
            curve_object.set_axes_array(axes_arrays)
            curve_object.set_ticks_arrays(ticks_arrays)
            ''' where lines_array_manifests'''
            #curve_object.axis_array = lines_array # leave em both, but reference this in createFBX, 04 Jan 2024
            
    # defunct, scaled inconsistent ticks
    def ticks(self,curve_object, n_ticks, axis_length, header,THD_direction,tick_length_ratio):
        #example, time: THD_direction = [1,0,0]
        # Called inside of controlPoint method, below: curve_object.update_ticks_thickness(span_adjust) & curve_object.calculate_span().
        ticks_array = []

        supergroup = ["Ticks: "+header+"_", None]
        ticks_array.append(supergroup)
        length_tick = abs(axis_length*tick_length_ratio) # should be positive anyways
        halflength_tick = length_tick/2
        if n_ticks > 1:
            values = np.linspace(0, axis_length, num=n_ticks)
            for value_n in values:
                tick_coords = self.ticks_control_points(curve_object, value_n,halflength_tick, THD_direction)
                tick_array = [str(round(value_n,2))+" "+header+"_"] # text label
                tick_array.append(tick_coords)
                ticks_array.append(tick_array)

            ticks_array.append([None,None])
        elif n_ticks == 1:
            value_n = axis_length/2
            tick_coords = self.ticks_control_points(curve_object, value_n,halflength_tick, THD_direction)
            tick_array = [str(round(value_n,2))+" "+header+"_"] # text label
            tick_array.append(tick_coords)
            ticks_array.append(tick_array)

            ticks_array.append([None,None])
        elif n_ticks < 1:
            ticks_array = []
        return ticks_array
    
    # defunct, scaled inconsistent ticks
    def ticks_redundant(self,curve_object,n_ticks, axis_length, header,THD_direction,tick_length_ratio,depthByHeight_coeff):
        # defunct: different sized ticks for special cases
        #example, time: THD_direction = [1,0,0]
        ticks_array = []

        supergroup = ["Ticks: "+header+"_", None]
        ticks_array.append(supergroup)
        length_tick = abs(axis_length*tick_length_ratio) # should be positive anyways
        halflength_tick = length_tick/2
        if n_ticks > 1:
            values = np.linspace(0, axis_length, num=n_ticks)
            for value_n in values:
                # In this ticks_redundant version, a 3 multiplier is used to increase the size of the ticks.
                # The physical tick length is larger, so that it can be seen even though the axis is small,
                # but, the assigned node name values are compensated for, so that they are accurate.
                tick_coords = self.ticks_control_points(curve_object, value_n,halflength_tick*3, THD_direction)
                tick_array = [str(round(value_n/depthByHeight_coeff,2))+" "+header+"_"] # text label
                tick_array.append(tick_coords)
                ticks_array.append(tick_array)
            ticks_array.append([None,None])
        elif n_ticks == 1:
            value_n = axis_length/2
            tick_coords = self.ticks_control_points(curve_object, value_n,halflength_tick*3, THD_direction)
            tick_array = [str(round(value_n/depthByHeight_coeff,2))+" "+header+"_"] # text label
            tick_array.append(tick_coords)
            ticks_array.append(tick_array)

            ticks_array.append([None,None])        
        elif n_ticks < 1:
            ticks_array = []
        return ticks_array


    def ticks_control_points(self,curve_object, value_n, halflength_tick, THD_direction):
        #Control points for a single closed mesh that represents both orthogonal ticks
        zero=0.01*halflength_tick# small, but still relatively scaled # this is a good solution.
        
        if THD_direction==[1,0,0]:

            curve_object.tick_halflength_THD[0] =  halflength_tick

            tick_controlPoints_matrix = \
            np.array([\
            [value_n, -zero, -zero],
            [value_n, -halflength_tick, -zero],
            [value_n, -halflength_tick, zero],

            [value_n, -zero, zero],
            [value_n, -zero, halflength_tick],
            [value_n, zero, halflength_tick],

            [value_n, zero, zero],
            [value_n, halflength_tick, zero],
            [value_n, halflength_tick, -zero],

            [value_n, zero, -zero],
            [value_n, zero, -halflength_tick],
            [value_n, -zero, -halflength_tick],
            [value_n, -zero, -zero]])
            
            span_adjust = np.array([[0,0],[-halflength_tick,halflength_tick],[-halflength_tick,halflength_tick]])
            # span_adjust is ultimately passed to curve_object.update_ticks_thickness(span_adjust)
            # test no passing out on 10 January 2024
        elif THD_direction==[0,1,0]:

            curve_object.tick_halflength_THD[1] =  halflength_tick

            tick_controlPoints_matrix = \
            np.array([\
            [-zero, value_n, -zero],
            [-zero, value_n, -halflength_tick],
            [zero, value_n, -halflength_tick],

            [zero, value_n, -zero],
            [halflength_tick, value_n, -zero],
            [halflength_tick, value_n, zero],

            [zero, value_n, zero],
            [zero, value_n, halflength_tick],
            [-zero, value_n, halflength_tick],

            [-zero, value_n, zero],
            [-halflength_tick, value_n, zero],
            [-halflength_tick, value_n, -zero],
            [-zero,value_n, -zero]])
            span_adjust = np.array([[-halflength_tick,halflength_tick],[0,0],[-halflength_tick,halflength_tick]])
        elif THD_direction==[0,0,1]:

            curve_object.tick_halflength_THD[2] =  halflength_tick

            tick_controlPoints_matrix = \
            np.array([\
            [-zero, -zero, value_n],
            [-halflength_tick, -zero, value_n],
            [-halflength_tick, zero, value_n],

            [-zero, zero, value_n],
            [-zero, halflength_tick, value_n],
            [zero, halflength_tick, value_n],

            [zero, zero, value_n],
            [halflength_tick, zero, value_n],
            [halflength_tick, -zero, value_n],

            [zero, -zero, value_n],
            [zero, -halflength_tick, value_n],
            [-zero, -halflength_tick, value_n],
            [-zero, -zero,value_n]])
            span_adjust = np.array([[-halflength_tick,halflength_tick],[-halflength_tick,halflength_tick],[0,0]])
        else:
            print("Unexpcted THD direction vector")

        curve_object.update_ticks_thickness(span_adjust)
        ###curve_object.calculate_span()
        
        return tick_controlPoints_matrix 
    
    # unused, probably won't be used
    def tick_control_points_single_direction(self):
        print('\nPlease develop tick_control_points_single_direction\n')
        # this is for curve object axis ticks, for curves which have the highest length axis in one way but not the other. 
        # do not do this. Do exploded,shared axes instead.
    
    # worthwhile. not necessary with axis labels included.
    def tick_span_expand(self):
        self.nope=0
        # change name
        # this is useful - currently span expansion does not consider ticks, only text, which is added after ticks and considers them. 
    '''
    # testing
    THD_direction = [1,0,0]
    n_ticks = 5
    axis_length = 9
    header = "Time(sec)"
    ticks_array = ticks(n_ticks, axis_length, header,THD_direction)
    '''

    # used, called in main
    def generate_consistent_ticks(self,tick_size):

        #Inputs: axis_length_Time, axis_length_Height, axis_length_Depth, number of ticks (inherent to class), tick_length (inherent to class)

        n_ticks = 5 # tie this to preferences page in the GUI
        tick_length_ratio = 0.05 # custom setting ratio of axis length
        axes_arrays = [] # all line_array instances in all lines_array instances

        for i in range(len(self.scene_object.vectorArray_time)):
            curve_object = self.hierarchy_object.dict_curve_objects_all[self.scene_object.names[i]]
            # if there is an error here, it probably means that hierarchy_object.dict_curve_objects_all was non populated in the import plugin
            
            lines_array = []

            #''Time''
            #time_axis_length = curve_object.axis_length_list_THD[0] # Paradigm agnostic,set in curve_object.__init__ constructor.
            time_axis_length = max(curve_object.dict_data_vectors_scaled["time"])
            time_axis_coords = np.array([[0,0,0],
                                [time_axis_length,0,0], # Only references positive values # There should be a paradigm agnostic way to do this, which this is not currently
                                [0,0,0]]) # Why is this like this? Answer: Remember: When defining lines or shapes, it is best practice to return to the initial point when defining control points for FBX construction.
            
            name = 'Axis: '+self.scene_object.headers_time[i]+"_"
            axis_array = [name]
            axis_array.append(time_axis_coords)
            lines_array.append(axis_array)
            chart_element_object = ChartElement(name = name,coords = time_axis_coords)
            chart_element_object.set_span_for_axis()
            curve_object.dict_chart_elements.update({name:chart_element_object})
            # work here, 2 April 2024
            
            axis_direction_THD = [1,0,0]
            ticks_array = self.ticks_consistent(curve_object,n_ticks, time_axis_length, self.scene_object.headers_time[i],axis_direction_THD,tick_size)
            lines_array.extend(ticks_array)

            #'' Height''
            #height_axis_length = max(self.scene_object.vectorArray_height[i])
            height_axis_length = max(curve_object.dict_data_vectors_scaled["height"])
            height_axis_coords = np.array([[0,0,0], 
                                [0,height_axis_length,0],# Not paradigm agnostic, assumes 0-0-0 data origin.
                                [0,0,0]])
            name = 'Axis: '+self.scene_object.headers_height[i]+"_"
            axis_array = [name]
            axis_array.append(height_axis_coords)
            lines_array.append(axis_array)
            
            axis_direction_THD = [0,1,0]
            ticks_array = self.ticks_consistent(curve_object,n_ticks, height_axis_length, self.scene_object.headers_height[i],axis_direction_THD,tick_size)
            lines_array.extend(ticks_array)
            chart_element_object = ChartElement(name = name,coords = height_axis_coords)
            chart_element_object.set_span_for_axis()
            curve_object.dict_chart_elements.update({name:chart_element_object})

            #''Depth''
            #depth_axis_length = max(self.scene_object.vectorArray_depth[i])
            depth_axis_length = max(curve_object.dict_data_vectors_scaled["depth"])
            depth_axis_coords = np.array([[0,0,0],
                                [0,0,depth_axis_length],# Not paradigm agnostic, assumes 0-0-0 data origin.
                                [0,0,0]])
            name = 'Axis: '+self.scene_object.headers_depth[i]+"_"
            axis_array = [name]
            axis_array.append(depth_axis_coords)
            lines_array.append(axis_array)
            chart_element_object = ChartElement(name = name,coords = depth_axis_coords)
            chart_element_object.set_span_for_axis()
            curve_object.dict_chart_elements.update({name:chart_element_object})
            
            axis_direction_THD = [0,0,1]
            # ticks are not built for styles not declared here
            ticks_array = self.ticks_consistent(curve_object,n_ticks, depth_axis_length, self.scene_object.headers_depth[i],axis_direction_THD,tick_size)
            lines_array.extend(ticks_array)

            

            # once this is done, it is hard to know the different between which entries are axis and which are ticks, without parsingthe labels. OOP would be better.
            axes_arrays.append(lines_array) # all axes for all data objects
            curve_object.set_axis_array(lines_array)
            #curve_object.axis_array = lines_array # leave em both, but reference this in createFBX, 04 Jan 2024
    # used, succesor to self.ticks() 
    def ticks_consistent(self,curve_object, n_ticks, axis_length, header,THD_direction,tick_size):
        #example, time: THD_direction = [1,0,0]
        # Called inside of controlPoint method, below: curve_object.update_ticks_thickness(span_adjust) & curve_object.calculate_span().
        ticks_array = []

        supergroup = ["Ticks: "+header+"_", None]
        ticks_array.append(supergroup)
        halflength_tick = tick_size/2
        if n_ticks > 1:
            values = np.linspace(0, axis_length, num=n_ticks)
            for value_n in values:
                tick_coords = self.ticks_control_points(curve_object, value_n,halflength_tick, THD_direction)
                tick_array = [str(round(value_n,2))+" "+header+"_"] # text label
                tick_array.append(tick_coords)
                ticks_array.append(tick_array)

            ticks_array.append([None,None])
        elif n_ticks == 1:
            value_n = axis_length/2
            tick_coords = self.ticks_control_points(curve_object, value_n,halflength_tick, THD_direction)
            tick_array = [str(round(value_n,2))+" "+header+"_"] # text label
            tick_array.append(tick_coords)
            ticks_array.append(tick_array)

            ticks_array.append([None,None])
        elif n_ticks < 1:
            ticks_array = []
        return ticks_array