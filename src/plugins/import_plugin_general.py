"""
Title: import_plugin_general.py
Author Clayton Bennett
Created: 289 March 2025
"""
if False:
    import pandas as pd
import os
import numpy as np
import import_lib
import time
from src.directories import Directories
from src.helpers.filename_utils import get_this_filename

def read_data_genfromtext(filepath,user_input_object,scene_object):
    filename = os.path.basename(filepath).lower()
    name = filename # name = os.path.splitext(filename)[0]
    if scene_object.request != None:
        # if already loaded
        gdf = scene_object.request.session['loaded_csv'][filename] # maybe this is the wrong key
        gdf = np.array(gdf)
    else:
        front = ''
        with open(front+filepath, 'r', encoding='utf-8-sig') as f:      
            gdf = np.genfromtxt(f, dtype=None, delimiter=',', skip_header=0).tolist() # test
            gdf = np.array(gdf)
            time.sleep(2)
    gdf[gdf == 'nan'] = 0 # like df.replace('nan', 0)
    gdf=np.nan_to_num(gdf) # like gdf.fillna(0)
    return gdf,name

def read_data_pandas(filename,user_input_object):
    print(f'\nfilename: {filename} \n')
    name = os.path.splitext(filename)[0]
    try:
        df = pd.read_csv(Directories.get_import_dir()+'/'+filename,skiprows=user_input_object.skiprows)
    except:
        df = pd.read_excel(Directories.get_import_dir()+'/'+filename,skiprows=user_input_object.skiprows)
    df.replace('nan', 0)
    df.fillna(0)
    return df,name

class ImportPlugin:
    scene_object = None
    style_object = None
    user_input_object = None
    DataPoint = None
    Curve = None
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
    @classmethod
    def assign_config_input_object(cls,config_input_object):
        cls.config_input_object = config_input_object
    @classmethod
    def pass_in_DataPoint_class(cls,DataPoint):
        cls.DataPoint = DataPoint
    @classmethod
    def pass_in_Curve_class(cls,Curve):
        cls.Curve = Curve
    def __init__(self):
        self.name = get_this_filename(__file__)
        import_lib.PluginSetup.import_None_instantiate(self)
        self.initialize_in_import_super()

    def initialize_in_import_super(self):
        self.vectorArray_time = []
        self.vectorArray_height = []
        self.vectorArray_depth = []
        self.headers_time = []
        self.headers_height = []
        self.headers_depth = []
        self.names=[]
        
        self.scale_t = 1
        self.scale_h = 1
        self.scale_d = 1

        print(f'scale = [{self.scale_t},{self.scale_h},{self.scale_d}]')
    
    def discern_filenames(self):
        if self.config_input_object.grouping_algorithm == "group-by-text": 
            self.filenames, self.filepaths = self.import_lib_object.sort_filenames_after_adding_leading_zeros_vercel(self.user_input_object,self.scene_object)
            return self.filenames, self.filepaths
        '''except:
            print('We need a way to handle when some or all filenames contain no numbers. ')
            print('Vercel file import failure ')
            self.filenames = self.user_input_object.filenames
        '''
            
    
    def clean_up_vector(self, vector, scale_coeff):
        vector = np.delete(vector, 0) # remove first element 
        vector = vector.astype(np.float64) # cast as type
        vector = np.multiply(scale_coeff,vector) # scale
        return vector
    def shoeshine_all_vectors(self,vector_time,vector_height,vector_depth):
        vector_time = self.clean_up_vector(vector_time, scale_coeff = self.scale_t)
        vector_height = self.clean_up_vector(vector_height, scale_coeff = self.scale_h)
        vector_depth = self.clean_up_vector(vector_depth, scale_coeff = self.scale_d)
        return vector_time,vector_height,vector_depth
        