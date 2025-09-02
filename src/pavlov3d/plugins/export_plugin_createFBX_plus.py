'''
Title: export_plugin_createFBX_plus
Created: 10 February 2024
Author: Clayton Bennett
'''
#import os
from src.pavlov3d import arrayMath
from src.pavlov3d.plugins.export_plugin import ExportPlugin

class Plugin(ExportPlugin):
    def plugin(self,createFBX_,datapoint_object):
        
        # style specific modules:
        nodeName_parent = self.node_name_determination(datapoint_object,key='vert')
        self.node_name_determination(datapoint_object,key='horiz')
        self.color_coeff_determination(datapoint_object) # run once, for each datapoint
        self.controlPoints_verticalPlane(datapoint_object,key='vert') # makes call to datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key=key)
        self.controlPoints_horizontalPlane(datapoint_object,key='horiz') # makes call to datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key=key)
        lGeometryNode_vertical = createFBX_.geometryNode(datapoint_object,key='vert') # makes call to datapoint_object.set_FBX_geometry(lGeometryNode,key=key)
        lGeometryNode_horizontal = createFBX_.geometryNode(datapoint_object,key='horiz') # makes call to datapoint_object.set_FBX_geometry(lGeometryNode,key=key)
        #lMaterial = createFBX_.material_determination(datapoint_object)#run once for each datapoint. If you want more colors, do that at the dataObjectlevel...
        # but what about datapoints that are complex shapes and characters! Just leave this artifact here...
        # we need a way to represent complex **reusable** shapes...need is a strong word. ignore this for literal years.
        # okay, so how about a surface mesh with a unique four-point geometry? That's means four separate three-value THD coordinates.
        # that can be handled by a specific FBX style plug in controlPoints_ method
        #lGeometryNode_vertical.AddMaterial(lMaterial)
        #lGeometryNode_horizontal.AddMaterial(lMaterial)
        #lGeometryNode = createFBX_.bundle_geometries(lGeometryNode_vertical,lGeometryNode_horizontal,nodeName_parent=nodeName_parent)
        lGeometryNode = createFBX_.bundle_geometries(datapoint_object.lGeometryNode_dict,nodeName_parent=nodeName_parent)
        return lGeometryNode

    def node_name_determination(self,datapoint_object,key):#specific
        nodeName_parent = datapoint_object.header_time+":"+str(round(datapoint_object.time,3))+", "+datapoint_object.header_height+":"+str(round(datapoint_object.height,3))+", j:"+str(datapoint_object.j)+"_"
        nodeName_plane = key+", "+datapoint_object.header_time+":"+str(round(datapoint_object.time,3))+", "+datapoint_object.header_height+":"+str(round(datapoint_object.height,3))+", j:"+str(datapoint_object.j)+"_"
        datapoint_object.set_node_name(nodeName_plane,key)
        return nodeName_parent

    def color_coeff_determination(self,datapoint_object):#specific
        datapoint_object.set_color_coeff(datapoint_object.color_coeff)
        return datapoint_object.color_coeff
    
    def controlPoints_verticalPlane(self,datapoint_object,key): # depth plane
        lControlPoint0 = [datapoint_object.time-datapoint_object.point_size, datapoint_object.height-datapoint_object.point_size, datapoint_object.depth]
        lControlPoint1 = [datapoint_object.time-datapoint_object.point_size, datapoint_object.height+datapoint_object.point_size, datapoint_object.depth]
        lControlPoint2 = [datapoint_object.time+datapoint_object.point_size, datapoint_object.height+datapoint_object.point_size, datapoint_object.depth]
        lControlPoint3 = [datapoint_object.time+datapoint_object.point_size, datapoint_object.height-datapoint_object.point_size, datapoint_object.depth]
        controlPoints_array = [lControlPoint0,lControlPoint1,lControlPoint2,lControlPoint3]
        controlPoints_array_fbx4 = arrayMath.fbx4_convert(controlPoints_array)
        datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key)
        return controlPoints_array_fbx4

    def controlPoints_horizontalPlane(self,datapoint_object,key): # height plane
        lControlPoint0 = [datapoint_object.time-datapoint_object.point_size, datapoint_object.height, datapoint_object.depth-datapoint_object.point_size]
        lControlPoint1 = [datapoint_object.time-datapoint_object.point_size, datapoint_object.height, datapoint_object.depth+datapoint_object.point_size]
        lControlPoint2 = [datapoint_object.time+datapoint_object.point_size, datapoint_object.height, datapoint_object.depth+datapoint_object.point_size]
        lControlPoint3 = [datapoint_object.time+datapoint_object.point_size, datapoint_object.height, datapoint_object.depth-datapoint_object.point_size]
        controlPoints_array = [lControlPoint0,lControlPoint1,lControlPoint2,lControlPoint3]
        controlPoints_array_fbx4 = arrayMath.fbx4_convert(controlPoints_array)
        datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key)
        return controlPoints_array_fbx4
