'''
Title: import_data_singleSheet_multiColumn.py
Author: Clayton Bennet
Created: 14 February 2024 (HaPpy Valentine's Day <3, from Luang Prabang :D)
'''
import numpy as np
if False:
    import pandas as pd
import os
from curve_ import Curve
from datapoint import DataPoint
import import_lib
class Plugin:
    """ scene_object = None
    style_object = None # should chance all instance of style. to style_object.

    @classmethod
    def pass_in_scene_object(cls,scene_object):
        cls.scene_object = scene_object
        cls.style_object = scene_object.style_object """

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py')
        import_lib.PluginSetup.import_None_instantiate(self)
        """ 
        self.df = None

        self.names = None
        self.vectorArray_time = None
        self.vectorArray_height = None
        self.vectorArray_depth = None
        self.headers_time = None
        self.headers_height = None
        self.headers_depth = None

        self.vectorArray_halfwidth_time = None
        self.vectorArray_halfwidth_height = None
        self.vectorArray_halfwidth_depth = None
        self.average_halfwidth_time = None
        self.average_halfwidth_height = None
        self.average_halfwidth_depth = None
        self.vectorArray_direction = None
    
        self.vectorArray_radius_minus_time = None
        self.vectorArray_radius_plus_time = None
        self.vectorArray_radius_minus_height = None
        self.vectorArray_radius_plus_height = None
        self.vectorArray_radius_minus_depth = None
        self.vectorArray_radius_plus_depth = None 
        """
        

    def run_import(self,scene_object,import_lib_object):

        # update to pass_in_scene_object paradigm()?
        self.style_object = scene_object.style_object
        user_input_object = scene_object.user_input_object
        Curve.pass_in_scene_object(scene_object)
        # need to add third dimension option. Not here, create new similar function.
        #hierarchy_object.dict_curve_objects_all = dict() # supress here 23 March 2024

        vectorArray_time = []
        vectorArray_height = []
        headers_time = []
        headers_height = []
        names=[]

        filename = user_input_object.filenames[0] # works for single sheet
        df,filename_sans_extension = self.read_data(filename,user_input_object)
        self.df = df
        df_heights = import_lib_object.checkColumnNames_singleSheet(df, user_input_object.column_height,user_input_object.data_start_idx)
        self.df_heights = df_heights

        data_start_idx = user_input_object.data_start_idx
        metadataColumns = list(df.columns[:data_start_idx]) # manual. # wrong
        df_data = df.iloc[:,data_start_idx:]
        #print(f'user_input_object.metadata_columns:{user_input_object.metadata_columns}')
        df_metadata=import_lib_object.check_for_metadata_coloumns(df,user_input_object.metadata_columns)

        #vector_dict = dict.fromkeys({user_input_object.column_time,user_input_object.column_height})
        vector_dict = dict()
        vector_time_labelname = df_data.keys()

        for index, row in df_data.iterrows():
            name =  df[user_input_object.column_time][index]
            # birth curve_object instances
            curve_object = Curve(name=name)
            curve_object.add_curve_object_to_scene_object() #check use 30Jan

            vector_height = row.to_list()
            vector_time_bar = np.array(list(range(len(vector_height))))*20#scaled to make bars wider
            vector_time =vector_time_bar

            vector_dict[user_input_object.column_time] = vector_time
            vector_dict[user_input_object.column_height] = vector_height
            vector_dict = import_lib_object.check_vectors_for_text(vector_dict)
            vector_dict = import_lib_object.check_time_vector_for_negative_change(vector_dict)
            vector_time=vector_dict[user_input_object.column_time]
            vector_height=vector_dict[user_input_object.column_height]
            curve_object.df_metadata=df_metadata.iloc[index]

            for i,point in enumerate(vector_time):
                # birth datapoint instances
                datapoint_object = DataPoint(curve_object) # birth
                curve_object.dict_datapoints.update({vector_time_labelname[i]:datapoint_object})
                datapoint_object.time = vector_time_bar[i]
                datapoint_object.height = vector_height[i]
                datapoint_object.chemicalID = vector_time_labelname[i] # metadata: put it all in!!!!!! FUCK YES.
                datapoint_object.metadata = df[metadataColumns].iloc[i]
                # it's time. send itttttttt.

            header_time = 'index'
            header_height = 'value'
            vectorArray_time.append(vector_time)
            vectorArray_height.append(vector_height)
            headers_time.append(header_time)
            headers_height.append(header_height)
            names.append(name)

            self.names = names 
            self.vectorArray_time = vectorArray_time
            self.vectorArray_height = vectorArray_height
            self.headers_time = headers_time
            self.headers_height = headers_height

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

        return names,vectorArray_time,vectorArray_height,headers_time,headers_height 

    def read_data(self,filename,user_input_object):
        print("filename: ",filename)
        try:
            #df = pd.read_csv(user_input_object.data_directory+"\\"+filename,skiprows=user_input_object.skiprows)
            df = pd.read_csv(user_input_object.data_directory+"/"+filename)
            name =  filename.rstrip('.csv')
        except:
            #df = pd.read_excel(user_input_object.data_directory+"\\"+filename,skiprows=user_input_object.skiprows)
            df = pd.read_excel(user_input_object.data_directory+"/"+filename)
            name =  filename.rstrip('.xlsx')
        df=df.replace('nan', 0)
        df=df.fillna(0)
        return df,name