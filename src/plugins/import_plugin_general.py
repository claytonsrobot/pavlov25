"""
Title: import_plugin_general.py
Author Clayton Bennett
Created: 289 March 2025
"""
import platform
if False:
    import pandas as pd
import os
import numpy as np
from datetime import datetime
import import_lib
import sys
import time
import environmental
from src.directories import Directories


#from scale import Scale
from curve_ import Curve
from datapoint import DataPoint # this is resetting because this import plugin is passed through importlib

def read_data_genfromtext(filepath,user_input_object,scene_object):
    filename = os.path.basename(filepath).lower()
    name = filename 
    # name = os.path.splitext(filename)[0]
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
    DataPoint = DataPoint
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