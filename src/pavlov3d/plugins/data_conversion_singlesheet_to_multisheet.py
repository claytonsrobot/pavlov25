'''
Title: data_conversion_singleSheet_to_multisheet.py
Author: Clayton Bennet
Created: 20 October 2024 
'''
import sys
import numpy as np
from pathlib import Path

#import pandas as pd
import os
from pavlov3d.plugins.import_plugin_general import read_data_genfromtext
#import import_lib
class Convert:
    def __init__(self):
        self.name = Path(__file__).name.lower().removesuffix('.py')        

    def run_import(self,filename):
        head,tail = os.path.split(os.getcwd()) # gross, 
        filepath = head / "imports" / filename 
        # need to add third dimension option. Not here, create new similar function.
        #hierarchy_object.dict_curve_objects_all = dict() # supress here 23 March 2024
        self.gdf,filename_sans_extension = self.get_data(filepath)

    def get_data(self,filepath):
        #head,tail = os.path.split(filepath)
        gdf,name= read_data_genfromtext(filepath,self.user_input_object, self.scene_object)
        print(name)
        for row in gdf:
            if row[0] == 'start_time':
                pass
            else:
                row = [x for x in row if str(x) != 'nan']
                row = np.asarray(row).astype(float)
                
                start_time = row[0]
                end_time = row[1]
                vector_height = row[2:-1]

                n = len(vector_height)
                vector_time = np.linspace(start_time,end_time,num = n, endpoint = True)
                self.save_data(vector_time,vector_height,name)
        #row_number_time
        """ scale_t = 1
        vector_time = gdf[:,column_number_time]
        vector_time = np.delete(vector_time, 0)
        vector_time = vector_time.astype(np.float64)
        vector_time = np.multiply(scale_t,vector_time)
        vector_height = gdf[:,column_number_height]
        vector_height = np.delete(vector_height, 0)
        vector_height = vector_height.astype(np.float64) """
        return gdf,name  

    
    def save_data(self,vector_time,vector_height,name):
        filename = name = name+"_"+str(vector_time[0])+".csv"
        np.savetxt(filename, np.column_stack((vector_time, vector_height)), delimiter=",", fmt='%s', header="time,value")

def main():    
    c = Convert()
    c.run_import("brach_avello-ghost-lotus.csv")

if __name__ == "__main__":
    main()
