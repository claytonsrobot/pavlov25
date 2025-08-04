'''
Title: export_plugin_createFBX_bar_3D
Created: 10 February 2024
Author: Clayton Bennett
'''
import arrayMath
#import os
from plugins.export_plugin import ExportPlugin

class Plugin(ExportPlugin):
    def plugin(self,createFBX_,datapoint_object):
        
        # style_object specific modules:
        self.node_name_determination(datapoint_object,key=0)
        self.color_coeff_determination(datapoint_object) # run once, for each datapoint
        self.controlPoints_verticalPlane(datapoint_object,key=0) # makes call to datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key=key)
        lGeometryNode = createFBX_.geometryNode(datapoint_object,key=0) # makes call to datapoint_object.set_FBX_geometry(lGeometryNode,key=key)
        #lMaterial = createFBX_.material_determination(datapoint_object)#run once for each datapoint. If you want more colors, do that at the dataObjectlevel...
        # but what about datapoints that are complex shapes and characters! Just leave this artifact here...
        # we need a way to represent complex **reusable** shapes...need is a strong word. ignore this for literal years.
        # okay, so how about a surface mesh with a unique four-point geometry? That's means four separate three-value THD coordinates.
        # that can be handled by a specific FBX style_object plug in controlPoints_ method
        #lGeometryNode.AddMaterial(lMaterial)
        return lGeometryNode

    def node_name_determination(self,datapoint_object,key):#specific
        #print(f"datapoint_object.header_time = {datapoint_object.header_time}")
        #str(round(datapoint_object.time,3))
        #print(f"datapoint_object.header_height = {datapoint_object.header_height}")
        #str(round(datapoint_object.height,3))
        #print(f"datapoint_object.header_depth = {datapoint_object.header_depth}")
        #str(round(datapoint_object.depth,3))
        #print(f"datapoint_object.j = {datapoint_object.j}")
        #nodeName = datapoint_object.header_time+":"+str(round(datapoint_object.time,3))+", "+datapoint_object.header_height+":"+str(round(datapoint_object.height,3))+","+datapoint_object.header_depth+":"+str(round(datapoint_object.depth,3))+", j:"+str(datapoint_object.j)+"_"
        nodeName = datapoint_object.header_time+":"+str(round(datapoint_object.dict_data_raw["time"],3))+", "+datapoint_object.header_height+":"+str(round(datapoint_object.dict_data_raw["height"],3))+","+datapoint_object.header_depth+":"+str(round(datapoint_object.dict_data_raw["depth"],3))+", j:"+str(datapoint_object.j)+"_"
        datapoint_object.set_node_name(nodeName,key)
        return nodeName

    def color_coeff_determination(self,datapoint_object):#specific
        datapoint_object.set_color_coeff(datapoint_object.color_coeff)
        return datapoint_object.color_coeff
    
    def controlPoints_verticalPlane(self,datapoint_object,key): # depth plane
        lControlPoint0 = [datapoint_object.time-datapoint_object.halfwidth_time, 0, 0]
        lControlPoint1 = [datapoint_object.time-datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth]
        lControlPoint2 = [datapoint_object.time+datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth]
        lControlPoint3 = [datapoint_object.time+datapoint_object.halfwidth_time, 0, 0]

        controlPoints_array = [lControlPoint0,lControlPoint1,lControlPoint2,lControlPoint3]
        controlPoints_array_fbx4 = arrayMath.fbx4_convert(controlPoints_array)
        datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key)
        #
        return controlPoints_array_fbx4

