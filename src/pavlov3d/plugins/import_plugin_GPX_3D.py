'''
Title: import plugin_GPX_3D.py
Author: Clayton Bennett
Created 16 February 2024

Purpose:
Serve as a known import plugin (represented in the gui_object import dictionary and as a GUI dropdown menu item available for user selection)
Process:
Import each CSV sheet as a dataframe and make the dataframe an attribute of each curve_object 'curve'
'''
import gpxpy
import numpy as np
import os
if False:
    import pandas as pd
from src.pavlov3d.helpers.filename_utils import get_this_filename
from src.pavlov3d.plugins.import_plugin_general import read_data_genfromtext, ImportPlugin
#from scale import Scale
class Plugin(ImportPlugin):
    def __init__(self):
        super().__init__()  # Call Parent's __init__
        self.name = get_this_filename(__file__)
        self.filetype_allowed_list = ['gpx']
        
    def run_import(self):
        #self.Curve.pass_in_scene_object(self.scene_object) # dict_curve_objects_all
        filenames, filepaths = self.discern_filenames()
        for filepath in filepaths:
            with open(filepath, 'r') as file:
                gpx = gpxpy.parse(file)
                vector_time = []
                vector_height = []
                vector_depth = []

                for track in gpx.tracks:
                    #print(f'Track: {track.name}')
                    for segment in track.segments:
                        #print(f'segment = {segment}')
                        for point in segment.points:
                            #print(f' - Track point: {point.latitude}, {point.longitude}, Elevation: {point.elevation}')
                            vector_time.append(point.latitude)
                            vector_depth.append(point.longitude)
                            vector_height.append(point.elevation)

            #gdf,name= read_data_genfromtext(filepath,self.user_input_object, self.scene_object)
            name = os.path.basename(filepath).lower()
            self.print_gpx_info(gpx)

            vector_time,vector_height,vector_depth = self.shoeshine_all_vectors(vector_time,vector_height,vector_depth)
            
            header_time = 'Latitude'
            header_height = 'Elevation'
            header_depth = 'Longitude'

            vector_dict = dict()
            vector_dict[header_time] = vector_time # Could just as easily use the number as the key, and need less.
            vector_dict[header_height] = vector_height
            vector_dict[header_depth] = vector_depth
            if True:
                vector_dict = self.import_lib_object.check_vectors_for_text(vector_dict) # cut off at index if found
                vector_dict = self.import_lib_object.check_time_vector_for_negative_change(vector_dict) # cut off at index if found
            vector_time=vector_dict[header_time]
            vector_height=vector_dict[header_height]
            vector_depth=vector_dict[header_depth]
            
            # vectors initalized in super
            self.vectorArray_time.append(vector_time)
            self.vectorArray_height.append(vector_height)
            self.vectorArray_depth.append(vector_depth)
            self.headers_time.append(header_time)
            self.headers_height.append(header_height)
            self.headers_depth.append(header_depth)
            self.names.append(name)

            curve_object = self.Curve(name=name) # Curve class passed in, due to issue with dynamic import of the plugin
            curve_object.add_headers(header_time,header_height,header_depth)
            curve_object.add_raw_data(vector_time,vector_height,vector_depth) 
            ## work on the data Object initialization

            for i,point in enumerate(vector_time):
                # birth datapoint instances
                datapoint_object = self.DataPoint(curve_object) # birth
                #datapoint_object.name 
                curve_object.dict_datapoints.update({vector_time[i]:datapoint_object})
                datapoint_object.time = vector_time[i]
                datapoint_object.height = vector_height[i]
                #print(f'datapoint_object.height = {datapoint_object.height}')
                datapoint_object.depth = vector_depth[i]
        
                #datapoint_object.halfwidth_time
                #datapoint_object.halfwidth_height
                #datapoint_object.halfwidth_depth
        
        self.import_lib_object.check_point_tally_for_all_files(self.vectorArray_time)
        
        return self.names,self.vectorArray_time,self.vectorArray_height,self.headers_time,self.headers_height
    
    def print_gpx_info(self,filepath):
        """ Print data from  gpx file"""
        with open(filepath, 'r') as file:
            gpx = gpxpy.parse(file)
        #print(f"gpx = {gpx}")
        # Print general info about the GPX file
        print(f'GPX File Version: {gpx.version}')
        print(f'Creator: {gpx.creator}')
        # Accessing waypoints, routes, and tracks
        for waypoint in gpx.waypoints:
            print(f'Waypoint: {waypoint.name}, Lat: {waypoint.latitude}, Lon: {waypoint.longitude}, Elevation: {waypoint.elevation}')
        for route in gpx.routes:
            print(f'Route: {route.name}')
            for rtept in route.points:
                print(f' - Route point: {rtept.latitude}, {rtept.longitude}')
        return True