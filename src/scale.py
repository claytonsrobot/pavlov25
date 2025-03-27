'''
title: Scale.py
Author: Clayton Bennett
Created: 14 February 2024
'''

'''
Point assignment in import needs to be scaled/sanitized later once we have all the facts
'''
from src import arrayMath

class AxisChannel:
    def __init__(self,name):
        self.name = name
        self.min = None
        self.max = None
        self.delta = None
        self.max_holder = None
        self.min_holder = None
        self.ideal_datum = None 
    def __doc__(self):
        'deals with each axes channel,header,vector,column name, column id'
class Scale:
    scene_object=None
    user_input_object = None
    style_object = None
    @classmethod
    def assign_scene_object_etc(cls,scene_object):
        cls.scene_object = scene_object
        cls.user_input_object = scene_object.user_input_object
        cls.style_object = scene_object.style_object

    def __init__(self):
        self.name = 'scale'
        self.dict_header_names = set()

    def register_vectorArray_axis_channel(self,header_name):
        self.dict_header_names.update({header_name:AxisChannel(header_name)})

    def register_vectorArray(self,header_name,vector_array):
        self.dict_header_names.update({header_name:vector_array})


    def for_vectorArray_find_min(self,header_name,vector_array):
        arrayMath.min_arrayMath(vector_array)

    def post_scaling_populate_curves_and_datapoints(self):
        self.scaled_vectorArray_dictionary
        True

    def scale_datapoints(self):
        # I will die on this hill
        # This is the real magic

        # numeric value vs labeled values
        
        #self.scene_object.min_time
        #self.scene_object.min_height
        #self.scene_object.min_depth
        #self.scene_object.max_time
        #self.scene_object.max_height
        #self.scene_object.max_depth

        for curve_object in self.scene_object.hierarchy_object.dict_curve_objects_all.values():
            curve_object.scene_latitude=None
            curve_object.scene_longitude=None
            curve_object.scene_elevation=None

            for datapoint_object in curve_object.dict_datapoints.values():
                datapoint_object.time = datapoint_object.time
                datapoint_object.height = datapoint_object.height
                datapoint_object.depth = datapoint_object.depth
                datapoint_object.halfwidth_time = datapoint_object.halfwidth_time
                datapoint_object.halfwidth_height = datapoint_object.halfwidth_height
                datapoint_object.halfwidth_depth = datapoint_object.halfwidth_depth
                datapoint_object.color_coeff = datapoint_object.color_coeff
                #datapoint_object.direction_facing = datapoint_object.direction_facing
                 # "datapoint_object.normal" doesn't sound right even to people who know what it means
    
    @staticmethod
    def define_paradigm():
        paradigm=\
        '''
        Today we conquer the last great mystery: scaling.
        We have been lucky so far to use data that does not require scaling.
        
        A good goal, iterively developed:
        eh: Find the min and max of all imported dimensions.
        eh: Find the curves that have the most extreme 
            ratios of some min to another max.
        eh: Find the curve with the most extreme ratio of 
            length of one axis to another axis.
        eh: Find the difference between min and max for 
            every imported vector, for each file, the total length of the axis.
        yes: Find the difference longest axis for the scene, 
            the difference between the scene max and the scene min for some vector.
        yes: Find the difference shortest axis for the scene, 
            the difference between the scene max and the scene min for some vector.  
        yes: Consider that curves will be data aligned.
        '''
        print(paradigm)
                

class MultipleAxesScalingAlgorithm:

    hierarchy_object = None
    @classmethod
    def assign_hierarchy_object(cls,hierarchy_object):
        cls.hierarchy_object = hierarchy_object

    def __init__(self):
        pass
    @staticmethod
    def normalize_all_curve_objects(set_curve_objects_all):
        target_axis_length = 1 # each, +10000 for the positive side, and -1000 the negative side. 
        for curve_object in set_curve_objects_all:

            MultipleAxesScalingAlgorithm.normalize_curve_object_values(curve_object,target_axis_length)
            MultipleAxesScalingAlgorithm.repair_curve_object_max_min(curve_object)

        return True
    

    def normalize_curve_object_values(curve_object,target_axis_length):
        # how are we handing these scaled values to the datapoint objects? 
        
        #for key,datapoint_object in curve_object.dict_datapoints.items():
        curve_object.dict_data_vectors_scaled["time"] = MultipleAxesScalingAlgorithm._make_target_normalized_data_vector(curve_object.dict_data_vectors_raw["time"],target_axis_length)
        curve_object.dict_data_vectors_scaled["height"] = MultipleAxesScalingAlgorithm._make_target_normalized_data_vector(curve_object.dict_data_vectors_raw["height"],target_axis_length)
        curve_object.dict_data_vectors_scaled["depth"] = MultipleAxesScalingAlgorithm._make_target_normalized_data_vector(curve_object.dict_data_vectors_raw["depth"],target_axis_length)

        j=0
        for datapoint_object in curve_object.dict_datapoints.values():

            datapoint_object.dict_data_raw["time"] = curve_object.dict_data_vectors_raw["time"][j]
            datapoint_object.dict_data_raw["height"] = curve_object.dict_data_vectors_raw["height"][j]
            datapoint_object.dict_data_raw["depth"] = curve_object.dict_data_vectors_raw["depth"][j]


            datapoint_object.dict_data_scaled["time"] = curve_object.dict_data_vectors_scaled["time"][j]
            datapoint_object.dict_data_scaled["height"] = curve_object.dict_data_vectors_scaled["height"][j]
            datapoint_object.dict_data_scaled["depth"] = curve_object.dict_data_vectors_scaled["depth"][j]
            #datapoint_object.dict_data_scaled["halfwidth_time"] = curve_object.dict_data_vectors_scaled["halfwidth_time"][j]
            #datapoint_object.dict_data_scaled["halfwidth_depth"] = curve_object.dict_data_vectors_scaled["halfwidth_depth"][j]
            #datapoint_object.dict_data_scaled["halfwidth_height"] = curve_object.dict_data_vectors_scaled["halfwidth_height"][j]

            datapoint_object.set_vars(j = j,
                            header_time = curve_object.header_time,
                            header_height = curve_object.header_height,
                            header_depth = curve_object.header_depth)
            
            #has: data_point_object.dict_raw_values()
            #will have: data_point_object.dict_scaled_values()
                        #if datapoint_object.color_coeff is None: # not none at this point, set wrong already: 3:43 PM on 12 February 2024
            #datapoint_object.set_vars(model_ID = model_ID,
            #                            color_coeff = curve_object.dict_color_coeff[model_ID][j])
            # i changed this to hack my shit together, on 29 Feb 2023.
            # this is terrible naming convention, because what the heck does color_coeff mean
            # also, model_ID is half outdated, half entirely necessary
            # a flying spaghetti monster i have build
            # it's dumb because it overwrites the value of dataoint object each time

            if j<len(curve_object.time)-1:
                time_next = curve_object.time[j+1]
                height_next = curve_object.height[j+1]
                depth_next = curve_object.depth[j+1]
                #try:
                #except:
                #    print(f'color_skipped: model_ID={model_ID},j={j}')
            else:# you are at the last item, and should make a last line of zero length
                time_next = curve_object.time[j]
                height_next = curve_object.height[j]
                depth_next = curve_object.depth[j]
        
            datapoint_object.set_vars(time_next = time_next,
                                    height_next = height_next,
                                    depth_next = depth_next)
            '''end: can be done elsewhere, earlier'''
            j+=1
        # more generically, a curve obect is a shape_object which can be considered to be scaled to a standard size - it can have attributes that belong to it that must be relative
    """
    def _make_positive_data_vector(self,raw_data_vector):
        positive_data_vector = []
        if min(raw_data_vector)<0:
            positive_data_vector = raw_data_vector + min(raw_data_vector)
        elif min(raw_data_vector)>0:
            positive_data_vector = raw_data_vector - min(raw_data_vector)
        elif min(raw_data_vector)==0:
            positive_data_vector = raw_data_vector
        return positive_data_vector
        """
    @staticmethod
    def _make_target_normalized_data_vector(data_vector,target_axis_length):
        #inputs: data_vector,target_axis_length
        #output: target_normalized_data_vector 
        target_normalized_data_vector = None
    
        min_val = min(data_vector)
        max_val = max(data_vector)
        
        # Normalize the positive_data_vector to range [0, 1]
        #print(f"data_vector = {data_vector}")
        #print(f"target_axis_length = {target_axis_length}")
        #print(f"min_val = {min_val}")
        #print(f"max_val = {max_val}")
        
        normalized_data_vector = [(x - min_val) / (max_val - min_val) for x in data_vector]
        
        # Scale the normalized_data_vector to range [-target_axis_length, target_axis_length]
        if False: # avg at origin 
            target_normalized_data_vector = [
            (x * 2 * target_axis_length) - target_axis_length for x in normalized_data_vector
            ]
        elif True: # origin is in corner works fine
            target_normalized_data_vector = [x * target_axis_length for x in normalized_data_vector]
        else:
            target_normalized_data_vector = [None] #  gotcha
        return target_normalized_data_vector
    
    @staticmethod
    def repair_curve_object_max_min(curve_object):

            curve_object.max_time = max(curve_object.dict_data_vectors_scaled["time"])
            curve_object.min_time = min(curve_object.dict_data_vectors_scaled["time"])
            curve_object.max_height = max(curve_object.dict_data_vectors_scaled["height"])
            curve_object.min_height = min(curve_object.dict_data_vectors_scaled["height"])
            curve_object.max_depth = max(curve_object.dict_data_vectors_scaled["depth"])
            curve_object.min_depth = min(curve_object.dict_data_vectors_scaled["depth"])
            curve_object.min_data = [curve_object.min_time,curve_object.min_height,curve_object.min_depth]

if __name__ =='__main__':
    Scale.define_paradigm()
    scale_object = Scale()
    
    

    #scale_object.define_paradigm()