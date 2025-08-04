'''
Title: import_lib.py
Author: Clayton Bennett
Date: 22 December 2022
import raw data, to feed to STL generation
1. Generate GUI (Kivy for mobile, customTkinter for desktop). For now, take prompts in IDLE.
---->2. Choose Data source (CSV, online database, MAT file, XLSX, etc)
---->3. Parse data source (choose columns, pages, etc)
4. Choose output style, including shape and how to organize output in Blender image.
5. File export.

resources:
https://docs.python-guide.org/writing/structure/

'''

import os # for normalizing pathname of directory
if False:
    import pandas as pd # for data management
import src.pavlov3d.numeric_islands as ni
#from datapoint import DataPoint
#from curve_ import Curve
from src.pavlov3d import arrayMath

class ImportLib:
    """ scene_object = None
    style_object = None """
    user_input_object = None
    column_id_time_default = 0
    column_id_height_default = 2


    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix('.py')
        #script_dir = Directories.get_core_dir()
        
        self.filenames = None
        self.filenames_sortable = None
        self.column_id_time = None
        self.column_id_height = None

        self.names = None
        self.vectorArray_time = None
        self.vectorArray_height = None
        self.headers_time = None
        self.headers_height = None
        self.import_funtion = None
        #self.get_data_2D()

        self.column_id_time_default = 0
        self.column_id_height_default = 1
        self.column_id_depth_default = 2

    def check_vectors_for_text(self,vector_dict):
        boolean_text=None
        index_text=[]
        for column_id,vector in vector_dict.items():
            for i,x in enumerate(vector):
                if isinstance(x,str):
                    boolean_text=True
                    index_text.append(i)
                    column_id_i = column_id
                    break

        if boolean_text is True:
            #print(f'text: {vector[i]},{i},{column_id_i}')
            #print(vector_dict)
            for column_id,vector in vector_dict.items():
                vector_dict[column_id] = vector[0:min(index_text)]

        #return boolean_text,index_text,vector_abridged
        return vector_dict
    
    def check_time_vector_for_negative_change(self,vector_dict):
        #load for initialization, wait to be tripped
        there_is_a_time_vector=None
        boolean_negative_change=None
        
        for column_id,vector in vector_dict.items():
            if type(column_id) is str:
                if 'time' in column_id.lower():  
                    vector_time = vector
                    there_is_a_time_vector=True
                    column_id_i = column_id
        if there_is_a_time_vector is True:
            for i,x in enumerate(vector_time):
                if i+1<len(vector_time) and i>2:# get through the first two numbers first - there is commonly a drop from 0 to 1
                    if x>vector_time[i+1]:
                        boolean_negative_change=True
                        index_negative_change=i
                        vector_time_value_at_negative_change = vector_time[i]
                        break
        
        if boolean_negative_change is True:
            #print(f'time: {vector[i]},{i},{column_id_i}')
            #print(vector_dict)
            print("\n")
            print(f'boolean_negative_change:{boolean_negative_change}: Data from the raw file has been rejected.\nThis is a purposeful design:\nThe Time column in the relevant file had a decrease in time value,\nwhich is expected to be erroneous')
            print(f"index_negative_change = {index_negative_change}")
            print(f"vector_time_value_at_negative_change ={vector_time_value_at_negative_change}")
            print(f"vector_time ={vector_time}")
            print("\n")
            for column_id,vector in vector_dict.items():
                vector_dict[column_id] = vector[0:index_negative_change]

        return vector_dict

    def checkColumnNames(self,df,string):
        #DATAFRAME
        #print(f'self={self}')
        # check for match of text segment, regardless of case
        # returns column number with first instance of the string matching a portion of the column name
        for i,name in enumerate(df.columns):
            if string.lower() in name.lower():
                break
            else:
                i = False  
        return i

    def checkColumnNames_gdf(self,gdf,string):
        #DATAFRAME
        #print(f'self={self}')

        # check for match of text segment, regardless of case
        # returns column number with first instance of the string matching a portion of the column name
        for i,name in enumerate(gdf[0]):
            #print(f'string={string}')
            #print(f'name={name}')
            
            if string.lower() in name.lower():
                break
            else:
                i = False  
        #print(f"i={i}")
        return i
    
    def checkColumnNames_singleSheet(self,df,column_keep_first_letter,data_start_idx):
        # check for match of text segment, regardless of case
        # returns column number with first instance of the string matching a portion of the column name
        i=int(data_start_idx)
        while i<len(df.columns):
            name = df.columns[i]
            if not(column_keep_first_letter in name):# this explicitly looks for the first letter. We can do better than that.
                # remove column from dataframe
                del(df[name])
                #print(i)
            else:
                i=i+1
            
            #i=i+1
        "all columns to the right of column N (inclusive) have been removed where the first letter of the column name does not match the columns_keep_start pattern."
        df_heights=df.copy()
        return df_heights   

        #column_vector1 = df.columns.get_loc(df.filter(like=column_id_time, axis=1).columns[0])
    
    def check_existence_of_provided_column_id_time(self,gdf,user_input_object):
    #def check_existence_of_provided_column_id_time(self,df,user_input_object):
        # messy and confusing approach

        if isinstance(user_input_object.column_time,str):
            #column_number_time = self.checkColumnNames(df,user_input_object.column_time)
            column_number_time = self.checkColumnNames_gdf(gdf,user_input_object.column_time)
            column_id_time = user_input_object.column_time
            # if found, provide numnber, if not provide False
        elif isinstance(user_input_object.column_time,int):
            column_number_time = user_input_object.column_time
            column_id_time = user_input_object.column_time
            
        if isinstance(column_number_time,bool):
            column_number_time = self.column_id_time_default
            column_id_time = self.column_id_time_default
            print("Column 1 text string not found, default used: "+str(self.column_id_time_default))
            # add option for if no match is found
        return column_id_time,column_number_time

    def check_existence_of_provided_column_id_height(self,gdf,user_input_object):
    #def check_existence_of_provided_column_id_height(self,df,user_input_object):
        if isinstance(user_input_object.column_height,str):
            #column_number_height = self.checkColumnNames(df,user_input_object.column_height)
            column_number_height = self.checkColumnNames_gdf(gdf,user_input_object.column_height)
            
            column_id_height = user_input_object.column_height
            # if found, provide numnber, if not provide False
        elif isinstance(user_input_object.column_height,int):
            column_number_height = user_input_object.column_height
            column_id_height = user_input_object.column_height
        if isinstance(column_number_height,bool):
            column_number_height = self.column_id_height_default
            column_id_height = self.column_id_height_default
            print("Column 2 text string not found, default used: "+str(self.column_id_height_default))
        return column_id_height,column_number_height
    
    def check_existence_of_provided_column_id_depth(self,gdf,user_input_object):
        if isinstance(user_input_object.column_depth,str):
            #column_number_depth = self.checkColumnNames(df,user_input_object.column_depth)
            column_number_depth = self.checkColumnNames_gdf(gdf,user_input_object.column_depth)
            
            column_id_depth = user_input_object.column_depth
            # if found, provide numnber, if not provide False
        elif isinstance(user_input_object.column_depth,int):
            column_number_depth = user_input_object.column_depth
            column_id_depth = user_input_object.column_depth
        if isinstance(column_number_depth,bool):
            column_number_depth = self.column_id_depth_default
            column_id_depth = self.column_id_depth_default
            print("Column 2 text string not found, default used: "+str(self.column_id_depth_default))
        return column_id_depth,column_number_depth
    
    def sort_filenames_after_adding_leading_zeros(self,user_input_object,scene_object):
        #print(f'user_input_object.filenames = {user_input_object.filenames}')
        if scene_object.style_object.find_numbers_in_filenames_and_equalize_digits is True:
            if False:
                filenames_sortable = ni.investigate_numeric_islands(user_input_object.filenames,scene_object.style_object,user_input_object)
            else:
                filenames_sortable = user_input_object.filenames
            filenames_sortable, filenames = zip(*sorted(zip(filenames_sortable, user_input_object.filenames)))
        else:
            filenames = user_input_object.filenames
            
        return filenames
    
    def sort_filenames_after_adding_leading_zeros_vercel(self,user_input_object,scene_object):
        #print(f'user_input_object.filenames = {user_input_object.filenames}')
        if scene_object.style_object.find_numbers_in_filenames_and_equalize_digits is True:
            if False:
                filenames_sortable = ni.investigate_numeric_islands(user_input_object.filenames,scene_object.style_object,user_input_object)
            else:
                filenames_sortable = user_input_object.filenames

            if len(user_input_object.filepaths)>1:
                #print(zip(filenames_sortable, user_input_object.filenames,  user_input_object.filepaths ))
                #print(sorted(zip(filenames_sortable, user_input_object.filenames,  user_input_object.filepaths)))
                filenames_sortable, filenames, filepaths = zip(*sorted(zip(filenames_sortable, user_input_object.filenames,  user_input_object.filepaths )))

            else:
                filenames = user_input_object.filenames
                filepaths = user_input_object.filepaths
        else:
            filenames = user_input_object.filenames
            
        return filenames, filepaths
    
    def check_for_metadata_coloumns(self,df,metadatacolumn_id_list):
        #print(f'metadatacolumn_id_list={metadatacolumn_id_list}')
        df_metadata = pd.DataFrame()
        for column_id in metadatacolumn_id_list:
            #print(column_id)
            if column_id in df.columns:
                df_metadata[column_id]=df[column_id]
        return df_metadata
    
    def check_point_tally_for_all_files(self,vectorArray_time):
        tally = arrayMath.count_datapoints(vectorArray_time)
        print(tally, "datapoints")
        count_limit = 800 
        # This is a soft judgement by Clayton: 
        # If the point tally exceeds this count_limit, you should not use a heavy style, namely the classic bar style, which has 6 sides / 12 triangles.
        if tally>count_limit:
            pass
            #print(f'\n{tally} datapoints > countlimit {count_limit}:\nIt is suggested to use a minimalist export style.\n')
        # futhermore, given point talley and the currently selected export style, estimate file size

    def separate_numeric_columns(self,df):
        # should we check every item or just the top item
        df_numeric = df.copy()
        df_str = df.copy()
        
        # cut out strings
        for column_name in df_numeric.columns:
            #first_entry = df_numeric[column_name][0]
            first_entry = df_numeric[column_name].iloc[0]
            if isinstance(first_entry,str):
                if not(first_entry.isnumeric()):
                    df_numeric.drop(column_name, axis=1, inplace=True)

        # cut out numbers - assume anything that isn't a number is a string, i.e. booleans are strings
        for column_name in df_str.columns:
            #first_entry = df_str[column_name][0]
            first_entry = df_str[column_name].iloc[0]
            if not(isinstance(first_entry,str)):
                df_str.drop(column_name, axis=1, inplace=True)
            else:
                if first_entry.isnumeric():
                    df_str.drop(column_name, axis=1, inplace=True)
        return df_numeric,df_str
    
    def groupby_paradigm(self,paradigm):
        ''' future work'''
        paradigm_options = ['filename',
                            'boilercell',
                            'buddycell']
        description =   '''
                        grouping paradigm can be based on:
                        the filename, where the file includes data
                        boilercell, one cell in the file that applies to the all data in the file
                        buddycell, each datapoint in the cell has a partner cell that discerns the relevant group 
                        '''

class PluginSetup: 
    @staticmethod
    def import_None_instantiate(instance):
        instance.df = None

        instance.names = None
        instance.vectorArray_time = None
        instance.vectorArray_height = None
        instance.vectorArray_depth = None
        instance.headers_time = None
        instance.headers_height = None
        instance.headers_depth = None

        instance.vectorArray_halfwidth_time = None
        instance.vectorArray_halfwidth_height = None
        instance.vectorArray_halfwidth_depth = None
        instance.average_halfwidth_time = None
        instance.average_halfwidth_height = None
        instance.average_halfwidth_depth = None
        instance.vectorArray_direction = None
    
        instance.vectorArray_radius_minus_time = None
        instance.vectorArray_radius_plus_time = None
        instance.vectorArray_radius_minus_height = None
        instance.vectorArray_radius_plus_height = None
        instance.vectorArray_radius_minus_depth = None
        instance.vectorArray_radius_plus_depth = None
        return True