'''
Title: data_conversion_singleSheet_to_multisheet.py
Author: Clayton Bennet
Created: 20 October 2024 
'''
import sys
sys.path.insert(0,'C:\\Users\\user\\.pyenv\\pyenv-win\\versions\\3.10.10\\Lib\\site-packages\\')
import numpy as np

#import pandas as pd
import os
#import import_lib
class Convert:

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py')        

    def run_import(self,filename):
        head,tail = os.path.split(os.getcwd())
        filepath = head+"\\imports\\"+filename 
        # need to add third dimension option. Not here, create new similar function.
        #hierarchy_object.dict_curve_objects_all = dict() # supress here 23 March 2024

        vectorArray_time = []
        vectorArray_height = []
        headers_time = []
        headers_height = []
        names=[]

        self.gdf,filename_sans_extension = self.read_data(filepath)


    def read_data(self,filepath):

        head,tail = os.path.split(filepath)
        gdf,name= self.read_data_genfromtext(filepath)
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
    
    def read_data_genfromtext(self,filepath):

        filename = os.path.basename(filepath)

        front = ""
        with open(front+filepath, 'r', encoding='utf-8-sig') as f: 
            gdf = np.genfromtxt(f, dtype=None, delimiter=',', skip_header=0).tolist() # test
            gdf = np.array(gdf)
            #print(f'gdf={gdf}')

        #print("gdf: ",gdf)
        
        name =  filename.replace('.csv','')
        
        #gdf[gdf == 'nan'] = 0
        #gdf.fillna(0)
        gdf=np.nan_to_num(gdf)
        return gdf,name
    
    def save_data(self,vector_time,vector_height,name):
        filename = name = name+"_"+str(vector_time[0])+".csv"
        """
        with open(..., 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writecolumn(vector_time)
            wr.writecolumn(vector_height)"""
        
        np.savetxt(filename, np.column_stack((vector_time, vector_height)), delimiter=",", fmt='%s', header="time,value")
        

def main():
    
    c = Convert()
    c.run_import("brach_avello-ghost-lotus.csv")

if __name__ == "__main__":
    main()
