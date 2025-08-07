'''
Title: import_data_singleSheet_multiColumn.py
Author: Clayton Bennet
Created: 14 February 2024 (HaPpy Valentine's Day <3, from Luang Prabang :D)
'''
import numpy as np
from src.pavlov3d.helpers.filename_utils import get_this_filename
from src.pavlov3d.plugins.import_plugin_general import read_data_genfromtext, read_data_pandas, ImportPlugin

from src.pavlov3d import import_lib
class Plugin(ImportPlugin):

    def __init__(self):
        self.name = get_this_filename(__file__)
        import_lib.PluginSetup.import_None_instantiate(self)

    def run_import(self,scene_object,import_lib_object):
        # need to add third dimension option. Not here, create new similar function.
        #hierarchy_object.dict_curve_objects_all = dict() # supress here 23 March 2024

        filename = self.user_input_object.filenames[0] # works for single sheet
        df,filename_sans_extension = read_data_pandas(filename,self.user_input_object)
        self.df = df
        df_heights = import_lib_object.checkColumnNames_singleSheet(df, self.user_input_object.column_height,self.user_input_object.data_start_idx)
        self.df_heights = df_heights

        data_start_idx = self.user_input_object.data_start_idx
        metadataColumns = list(df.columns[:data_start_idx]) # manual. # wrong
        df_data = df.iloc[:,data_start_idx:]
        #print(f'self.user_input_object.metadata_columns:{self.user_input_object.metadata_columns}')
        df_metadata=import_lib_object.check_for_metadata_coloumns(df,self.user_input_object.metadata_columns)

        #vector_dict = dict.fromkeys({self.user_input_object.column_time,self.user_input_object.column_height})
        vector_dict = dict()
        vector_time_labelname = df_data.keys()

        for index, row in df_data.iterrows():
            name =  df[self.user_input_object.column_time][index]
            # birth curve_object instances
            curve_object = self.Curve(name=name)
            curve_object.add_curve_object_to_hierarchy_object() #check use 30Jan

            vector_height = row.to_list()
            vector_time_bar = np.array(list(range(len(vector_height))))*20#scaled to make bars wider
            vector_time =vector_time_bar

            vector_dict[self.user_input_object.column_time] = vector_time
            vector_dict[self.user_input_object.column_height] = vector_height
            vector_dict = import_lib_object.check_vectors_for_text(vector_dict)
            vector_dict = import_lib_object.check_time_vector_for_negative_change(vector_dict)
            vector_time=vector_dict[self.user_input_object.column_time]
            vector_height=vector_dict[self.user_input_object.column_height]
            curve_object.df_metadata=df_metadata.iloc[index]

            for i,point in enumerate(vector_time):
                # birth datapoint instances
                datapoint_object = self.DataPoint(curve_object) # birth
                curve_object.dict_datapoints.update({vector_time_labelname[i]:datapoint_object})
                datapoint_object.time = vector_time_bar[i]
                datapoint_object.height = vector_height[i]
                datapoint_object.chemicalID = vector_time_labelname[i] # metadata: put it all in!!!!!! FUCK YES.
                datapoint_object.metadata = df[metadataColumns].iloc[i]
                # it's time. send itttttttt.

            header_time = 'index'
            header_height = 'value'
            # These "self." vector arrays are initialized in super, import_plugin_general.ImportPlugin
            self.vectorArray_time.append(vector_time)
            self.vectorArray_height.append(vector_height)
            self.headers_time.append(header_time)
            self.headers_height.append(header_height)
            self.names.append(name)

            self.headers_depth = self.headers_height # for 2D redundant data
            self.vectorArray_depth = self.style_object.prepare_missing_depth(self.vectorArray_time,self.vectorArray_height) # not entirely necessary
            self.vectorArray_halfwidth_time,self.average_halfwidth_time = self.style_object.prepare_missing_halfwidth_time_vectorArray(self.vectorArray_time)
            
            self.vectorArray_halfwidth_height = None # not used now, override
            self.vectorArray_halfwidth_depth = None # not used now, override
            self.average_halfwidth_height = None
            self.average_halfwidth_depth = None
            #self.vectorArray_direction = self.style_object.prepare_missing_direction_vectorArray(vectorArray_time,vectorArray_height,vectorArray_depth)
            self.vectorArray_direction = None

            curve_object.add_raw_data(vector_time,
                                    vector_height,
                                    vector_height)
            curve_object.header_time = header_time
            curve_object.header_height = header_height
            curve_object.header_depth = header_height
            curve_object.chemID_list=vector_time_labelname
        #print(f'curve_object.dict_datapoints.keys() = {curve_object.dict_datapoints.keys()}')

        return self.names,self.vectorArray_time,self.vectorArray_height,self.headers_time,self.headers_height 

