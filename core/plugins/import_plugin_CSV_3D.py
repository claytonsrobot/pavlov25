'''
Title: import plugin_CSV_2D.py
Author: Clayton Bennett
Created 16 February 2024

Purpose:
Serve as a known import plugin (represented in the gui_object import dictionary and as a GUI dropdown menu item available for user selection)
Process:
Import each CSV sheet as a dataframe and make the dataframe an attribute of each curve_object "curve"
'''
import platform
if False:
    import pandas as pd
import os
import numpy as np
from datetime import datetime
import import_lib
import sys
import time

from directories import Directories

#from scale import Scale
from curve_ import Curve
from datapoint import DataPoint
#class import_plugin_CSV_2D:
class Plugin:
    scene_object = None
    style_object = None
    user_input_object = None
    @classmethod
    def assign_scene_object_etc(cls,scene_object):
        cls.scene_object = scene_object
        cls.style_object = scene_object.style_object
    @classmethod
    def assign_user_input_object(cls,user_input_object):
        cls.user_input_object = user_input_object
    """ @classmethod
    def assign_scale_object(cls,scale_object):
        cls.scale_object = scale_object """
    @classmethod
    def assign_import_lib_object(cls,import_lib_object):
        cls.import_lib_object = import_lib_object
        
    def __init__(self):
        
        self.name = os.path.basename(__file__).removesuffix('.py')
        import_lib.PluginSetup.import_None_instantiate(self)
        self.filetype_allowed_list = ["csv","xlsx","xls"]
        """ self.filenames = None
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
        self.vectorArray_radius_plus_depth = None """

    """ def assess_for_scaling(self):
        True
        print(f'Run import in bulk first. \n import scaling method \n Pass all data. \n Then, once scaled, populate the curves and datapoints')
    """
    def populate_curves_and_datapoints(self):
        #self.scale_object.post_scaling_populate_curves_and_datapoints()
        True

    def run_import(self):
        #Curve.pass_in_scene_object(self.scene_object) # dict_curve_objects_all

        
        if 'win' in platform.platform().lower():
            vercel=False
        else:
            vercel=True

        #print(f'\nVERCEL = {vercel}\n')
        if vercel==False:
            #folder='\\media\\csv_uploads_pavlovdata\\'

            # IMPLEMENT CHANGES FOR PROJECTS PARADIGM
            folder='\\imports\\'
            import_wd = Directories.get_program_dir()+folder
            if os.getcwd()==Directories.get_program_dir():
                pass
                #os.chdir(import_wd)
            else:
                pass
            
        else:
            folder=self.scene_object.blob_dir+'/csv_uploads_pavlovdata/'


        vectorArray_time = []
        vectorArray_height = []
        vectorArray_depth = []
        headers_time = []
        headers_height = []
        headers_depth = []
        names=[]
        
        #try: 
        #self.filenames, list_blob_urls, list_objects = self.scene_object.session_object.get_list_csv_current()
        #self.filenames, list_blob_urls, list_objects = self.scene_object.request.session["list_csv_uploads"]
        #self.scene_object.request.session["list_csv_uploads"]
        #self.filesnames = self.user_input_object.filenames
        #self.filespaths = self.user_input_object.filepaths
        ##self.filenames = self.import_lib_object.sort_filenames_after_adding_leading_zeros(self.user_input_object,self.scene_object)
        self.filenames, self.filepaths = self.import_lib_object.sort_filenames_after_adding_leading_zeros_vercel(self.user_input_object,self.scene_object)
        """except:
            print('We need a way to handle when some or all filenames contain no numbers. ')
            print("Vercel file import failure ")
            self.filenames = self.user_input_object.filenames
        """
        
        #def import_data_from_all_filenames_into_vector_arrays(self):
        filecount = len(self.filepaths)
        for j,filepath in enumerate(self.filepaths):
            #DATAFRAME

            gdf,name= self.read_data_genfromtext(filepath,self.user_input_object)
            
            column_id_time,column_number_time = \
                self.import_lib_object.check_existence_of_provided_column_id_time(gdf,self.user_input_object)
            
            column_id_height,column_number_height =\
                  self.import_lib_object.check_existence_of_provided_column_id_height(gdf,self.user_input_object)
            
            column_id_depth,column_number_depth =\
                  self.import_lib_object.check_existence_of_provided_column_id_depth(gdf,self.user_input_object)

            scale_t = 1
            #print(f"column_number_time = {column_number_time}")
            #print(f"gdf = {gdf}")
            vector_time = gdf[:,column_number_time]
            vector_time = np.delete(vector_time, 0)
            if True:
                vector_time = vector_time.astype(np.float64)
                vector_time = np.multiply(scale_t,vector_time)
            elif False:
                vector_time.astype('datetime64[D]')
            else:
                for i,stamp in enumerate(vector_time):
                    time_obj=datetime.strptime(vector_time[i], '%I:%M:%S %p')
                    vector_time[i] = time_obj.strftime('%H:%M:%S')
                print(f"vector_time[i]:{i} = {vector_time[i]}")

            if False:# for stiles excel data, Jan 1 1900, strip days,months,years # base this on config "time-series-transcoding":"excel-datetime"
                if cij["time-series-transcoding":"excel-datetime"]:
                    for i,time_i in enumerate(vector_time):
                        time_of_day=time_i -int(time_i)
                        vector_time[i] = time_of_day#vector_time[i]

            
            
            vector_height = gdf[:,column_number_height]
            vector_height = np.delete(vector_height, 0)
            vector_height = vector_height.astype(np.float64)
            vector_height = np.multiply(1,vector_height)

            vector_depth = gdf[:,column_number_depth]
            vector_depth = np.delete(vector_depth, 0)
            vector_depth = vector_depth.astype(np.float64)
            vector_depth = np.multiply(1,vector_depth)

            vector_dict = dict()
            vector_dict[column_id_time] = vector_time # Could just as easily use the number as the key, and need less.
            vector_dict[column_id_height] = vector_height
            vector_dict[column_id_depth] = vector_depth
            #print(f'vector_dict.keys():{vector_dict.keys()}')
            vector_dict = self.import_lib_object.check_vectors_for_text(vector_dict) # cut off at index if found
            vector_dict = self.import_lib_object.check_time_vector_for_negative_change(vector_dict) # cut off at index if found
            vector_time=vector_dict[column_id_time]
            vector_height=vector_dict[column_id_height]
            vector_depth=vector_dict[column_id_depth]
            
            #header_time = df.columns[column_number_time]
            #header_height = df.columns[column_number_height]
            header_time = gdf[0][column_number_time]
            header_height = gdf[0][column_number_height]
            header_depth = gdf[0][column_number_depth]

            vectorArray_time.append(vector_time)
            vectorArray_height.append(vector_height)
            vectorArray_depth.append(vector_depth)
            headers_time.append(header_time)
            headers_height.append(header_height)
            headers_depth.append(header_depth)
            names.append(name)

            #curve_object = Curve(name=name)
            curve_object = self.scene_object.hierarchy_object.dict_curve_objects_all[name]
            #print(f"name: {name}, curve_object: {curve_object.name}")
            curve_object.add_headers(header_time,header_height,header_depth)
            curve_object.add_raw_data(vector_time,vector_height,vector_depth) 
            curve_object.dict_data_vectors_raw["time"] = vector_time
            
            curve_object.dict_data_vectors_raw["height"] = vector_height
            curve_object.dict_data_vectors_raw["depth"] = vector_depth
            ## work on the data Object initialization

            # security risk
            #non_standard_datapoint_attributes = None # alters kwargs sent to DataPoint
            #if non_standard_datapoint_attributes is not None:
            #    DataPoint.add_non_standard_attributes(non_standard_datapoint_attributes) # retch
            for i,point in enumerate(vector_time):
                # birth datapoint instances
                datapoint_object = DataPoint(curve_object) # birth
                #datapoint_object.name 
                # this needs to go
                curve_object.dict_datapoints.update({vector_time[i]:datapoint_object})
                
                datapoint_object.time = vector_time[i]
                datapoint_object.height = vector_height[i]
                #print(f"datapoint_object.height = {datapoint_object.height}")
                datapoint_object.depth = vector_depth[i]
        
                datapoint_object.halfwidth_time
                datapoint_object.halfwidth_height
                datapoint_object.halfwidth_depth
            
            sys.stdout.write('\r')
            sys.stdout.write(f"File {j+1}/{filecount} loaded, {i} datapoints.")
            sys.stdout.flush()
            time.sleep(0.01)
            #print(f"File {j+1}/{filecount} loaded, {i} datapoints.")

        self.names = names 
        self.vectorArray_time = vectorArray_time
        self.vectorArray_height = vectorArray_height
        self.vectorArray_depth = vectorArray_depth
        self.headers_time = headers_time
        self.headers_height = headers_height
        self.headers_depth = headers_depth

        #self.vectorArray_depth = self.style_object.preparecurve_object.dict_data_vectors_raw["halfwidth_time"]_missing_depth(self.vectorArray_time,self.vectorArray_height) # not entirely necessary
        self.vectorArray_halfwidth_time,self.average_halfwidth_time = self.style_object.prepare_missing_halfwidth_time_vectorArray(self.vectorArray_time)
        self.vectorArray_halfwidth_height,self.average_halfwidth_height = self.style_object.prepare_missing_halfwidth_height_vectorArray(self.vectorArray_height) 
        self.vectorArray_halfwidth_depth,self.average_halfwidth_depth = self.style_object.prepare_missing_halfwidth_depth_vectorArray(self.vectorArray_depth) 
        #self.vectorArray_direction = self.style_object.prepare_missing_direction_vectorArray(vectorArray_time,vectorArray_height,vectorArray_depth)
        self.vectorArray_direction = None
        for i,curve_object in enumerate(self.scene_object.hierarchy_object.dict_curve_objects_all.values()):
            #curve_object.dict_data_vectors_raw["halfwidth_time"]
            #print(f"curve_object.name = {curve_object.name}")
            #            .dict_data_vectors_raw[
            curve_object.dict_data_vectors_raw["halfwidth_time"] = self.vectorArray_halfwidth_time[i]
            curve_object.dict_data_vectors_raw["halfwidth_height"] = self.vectorArray_halfwidth_height[i]
            curve_object.dict_data_vectors_raw["halfwidth_depth"] = self.vectorArray_halfwidth_depth[i]

        self.import_lib_object.check_point_tally_for_all_files(vectorArray_time)
        #os.chdir(Directories.get_program_dir()) # if dilure, then broken
        return names,vectorArray_time,vectorArray_height,headers_time,headers_height

    def read_data(self,filename,user_input_object):
        print(f"\nfilename: {filename} \n")
        try:
            df = pd.read_csv(user_input_object.data_directory+"/"+filename,skiprows=user_input_object.skiprows)
            name =  filename.rstrip('.csv')
        except:
            df = pd.read_excel(user_input_object.data_directory+"/"+filename,skiprows=user_input_object.skiprows)
            name =  filename.rstrip('.xlsx')
        df.replace('nan', 0)
        df.fillna(0)
        return df,name
        

    def read_data_genfromtext(self,filepath,user_input_object):
        filename = os.path.basename(filepath).lower()
        #if self.scene_object.request.session["vercel_bool"]:
        #if True: # already loaded
        if self.scene_object.request != None:
            # already loaded
            
            #front = self.scene_object.request.session["blob_dir"]
            gdf = self.scene_object.request.session["loaded_csv"][filename] # maybe this iss the wrong key
            gdf = np.array(gdf)
            #print(f'gdf1={gdf}')
            
            
        else:
            import time
            front = ""
            with open(front+filepath, 'r', encoding='utf-8-sig') as f: 
                gdf = np.genfromtxt(f, dtype=None, delimiter=',', skip_header=0).tolist() # test
                gdf = np.array(gdf)
                
                #print(f'gdf2={gdf}')
                time.sleep(2)

        #print("gdf: ",gdf)
        
        name =  filename.rstrip('.csv')
        name =  filename.rstrip('.xlsx')
        #df.replace('nan', 0)
        gdf[gdf == 'nan'] = 0
        #gdf.fillna(0)
        gdf=np.nan_to_num(gdf)
        return gdf,name
        