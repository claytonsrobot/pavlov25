'''
Title: messaging.py
Created: 20 January 2024
Author: Clayton Bennett

Purpose:
Store messages called from main.py or otherwise.
Pass in scene_object and other necessary variables
'''
def print_data_range(scene_object):
    if scene_object.min_time != None and scene_object.max_time != None and scene_object.headers_time != None:
        #print(f"scene_object.headers_time = {scene_object.headers_time}")
        print("Time range: ",scene_object.min_time," to ",scene_object.max_time," ",scene_object.headers_time[0])
    else:
        print("Time data not imported.")
        
    if scene_object.min_height != None and scene_object.max_height != None and scene_object.headers_height != None:
        #print(f"scene_object.headers_height = {scene_object.headers_height}")
        print("Height range: ",scene_object.min_height," to ",scene_object.max_height," ",scene_object.headers_height[0])
    else:
        print("Height data not imported.")
    
    if scene_object.min_depth != None and scene_object.max_depth != None and scene_object.headers_depth != None:
        print("Depth range: ",scene_object.min_depth," to ",scene_object.max_depth," ",scene_object.headers_depth[0])
        #print(f"scene_object.headers_depth = {scene_object.headers_depth}")
    else:
        print("Depth range: Third dimension not imported.")



