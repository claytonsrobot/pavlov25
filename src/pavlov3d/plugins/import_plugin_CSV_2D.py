'''
Title: import plugin_CSV_2D.py
Author: Clayton Bennett
Created 16 February 2024

Purpose:
Serve as a known import plugin (represented in the gui_object import dictionary and as a GUI dropdown menu item available for user selection)
Process:
Import each CSV sheet as a dataframe and make the dataframe an attribute of each curve_object "curve"
'''
if False:
    import pandas as pd
import numpy as np
from src.helpers.filename_utils import get_this_filename
from src.plugins.import_plugin_general import read_data_genfromtext, ImportPlugin
 
class Plugin(ImportPlugin):
    def __init__(self):
        super().__init__()  # Call Parent's __init__
        self.name = get_this_filename(__file__)
        self.filetype_allowed = ["csv,xlsx,xls"]

    def run_import(self):
        self.discern_filenames()
        for filepath in self.filepaths:
        
            gdf,name= read_data_genfromtext(filepath,self.user_input_object, self.scene_object)
            
            column_id_time,column_number_time = \
                self.import_lib_object.check_existence_of_provided_column_id_time(gdf,self.user_input_object)
            column_id_height,column_number_height = self.import_lib_object.check_existence_of_provided_column_id_height(gdf,self.user_input_object)

            scale_t = 1
            vector_time = gdf[:,column_number_time]
            vector_time = np.delete(vector_time, 0)
            vector_time = vector_time.astype(np.float64)
            vector_time = np.multiply(scale_t,vector_time)

            vector_height = gdf[:,column_number_height]
            vector_height = np.delete(vector_height, 0)
            vector_height = vector_height.astype(np.float64)
            vector_height = np.multiply(300,vector_height)

            vector_dict = dict()
            vector_dict[column_id_time] = vector_time # Could just as easily use the number as the key, and need less.
            vector_dict[column_id_height] = vector_height
            #print(f'vector_dict.keys():{vector_dict.keys()}')
            vector_dict = self.import_lib_object.check_vectors_for_text(vector_dict) # cut off at index if found
            vector_dict = self.import_lib_object.check_time_vector_for_negative_change(vector_dict) # cut off at index if found
            vector_time=vector_dict[column_id_time]
            vector_height=vector_dict[column_id_height]
            
            #header_time = df.columns[column_number_time]
            #header_height = df.columns[column_number_height]
            header_time = gdf[0][column_number_time]
            header_height = gdf[0][column_number_height]

            if self.scene_object.style_object.styleChoice_depth00 == 'depthByHeight_coeff':
                vector_depth = np.multiply(self.scene_object.style_object.depthByHeight_coeff,vector_height)
                header_depth = header_height
            else: 
                print(f'Unexpected style for handling vector_depth in {self.name}')

            # These "self." vector arrays are initialized in super, import_plugin_general.ImportPlugin
            self.vectorArray_time.append(vector_time)
            self.vectorArray_height.append(vector_height)
            self.headers_time.append(header_time)
            self.headers_height.append(header_height)
            self.names.append(name)

            curve_object = self.Curve(name=name) # due to issue with dynamic import
            curve_object.add_headers(header_time,header_height,header_depth)
            curve_object.add_raw_data(vector_time,vector_height,vector_depth) 
            ## work on the data Object initialization

            # security risk
            #non_standard_datapoint_attributes = None # alters kwargs sent to DataPoint
            #if non_standard_datapoint_attributes is not None:
            #    DataPoint.add_non_standard_attributes(non_standard_datapoint_attributes) # retch
            for i,point in enumerate(vector_time):
                # birth datapoint instances
                datapoint_object = self.DataPoint(curve_object) # birth
                #datapoint_object.name 
                curve_object.dict_datapoints.update({vector_time[i]:datapoint_object})
                datapoint_object.time = vector_time[i]
                datapoint_object.height = vector_height[i]
                #print(f"datapoint_object.height = {datapoint_object.height}")
                datapoint_object.depth = vector_depth[i]
        
                #datapoint_object.halfwidth_time
                #datapoint_object.halfwidth_height
                #datapoint_object.halfwidth_depth


        self.headers_depth = self.headers_height # for 2D redundant data
        
        self.import_lib_object.check_point_tally_for_all_files(self.vectorArray_time)
        
        return self.names,self.vectorArray_time,self.vectorArray_height,self.headers_time,self.headers_height 

