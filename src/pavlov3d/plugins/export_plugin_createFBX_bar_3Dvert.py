'''
Title: export_plugin_createFBX_bar_3D
Created: 10 February 2024
Author: Clayton Bennett
'''
from pavlov3d import arrayMath
#import os
from pavlov3d.plugins.export_plugin import ExportPlugin

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
        nodeName = datapoint_object.header_time+":"+str(round(datapoint_object.time,3))+", "+datapoint_object.header_height+":"+str(round(datapoint_object.height,3))+","+datapoint_object.header_depth+":"+str(round(datapoint_object.depth,3))+", j:"+str(datapoint_object.j)+"_"
        datapoint_object.set_node_name(nodeName,key)
        return nodeName

    def color_coeff_determination(self,datapoint_object):#specific
        datapoint_object.set_color_coeff(datapoint_object.color_coeff)
        return datapoint_object.color_coeff
    
    def controlPoints_verticalPlane(self,datapoint_object,key): # depth plane
        lControlPoint0 = [datapoint_object.time-datapoint_object.halfwidth_time, 0, datapoint_object.depth-datapoint_object.halfwidth_depth]
        lControlPoint1 = [datapoint_object.time-datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth-datapoint_object.halfwidth_depth]
        lControlPoint2 = [datapoint_object.time+datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth-datapoint_object.halfwidth_depth]
        lControlPoint3 = [datapoint_object.time+datapoint_object.halfwidth_time, 0, datapoint_object.depth-datapoint_object.halfwidth_depth]

        lControlPoint4 = [datapoint_object.time+datapoint_object.halfwidth_time, 0, datapoint_object.depth-datapoint_object.halfwidth_depth]
        lControlPoint5 = [datapoint_object.time+datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth-datapoint_object.halfwidth_depth]
        lControlPoint6 = [datapoint_object.time+datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth+datapoint_object.halfwidth_depth]
        lControlPoint7 = [datapoint_object.time+datapoint_object.halfwidth_time, 0, datapoint_object.depth+datapoint_object.halfwidth_depth]

        lControlPoint8 = [datapoint_object.time+datapoint_object.halfwidth_time, 0, datapoint_object.depth-datapoint_object.halfwidth_depth]
        lControlPoint9 = [datapoint_object.time-datapoint_object.halfwidth_time, 0, datapoint_object.depth-datapoint_object.halfwidth_depth]

        lControlPoint10 = [datapoint_object.time-datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth-datapoint_object.halfwidth_depth]
        lControlPoint11 = [datapoint_object.time-datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth+datapoint_object.halfwidth_depth]
        lControlPoint12 = [datapoint_object.time+datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth+datapoint_object.halfwidth_depth]
        lControlPoint13 = [datapoint_object.time+datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth-datapoint_object.halfwidth_depth]
        lControlPoint14 = [datapoint_object.time-datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth-datapoint_object.halfwidth_depth]
        lControlPoint15 = [datapoint_object.time-datapoint_object.halfwidth_time, 0, datapoint_object.depth-datapoint_object.halfwidth_depth]

        lControlPoint16 = [datapoint_object.time-datapoint_object.halfwidth_time, 0, datapoint_object.depth+datapoint_object.halfwidth_depth]
        
        """
        controlPoints_array = [lControlPoint0,lControlPoint1,lControlPoint2,lControlPoint3,
                               lControlPoint4,lControlPoint5,lControlPoint6,lControlPoint7,
                               lControlPoint7,
                               lControlPoint8,lControlPoint9,
                               lControlPoint10,lControlPoint11,lControlPoint12,lControlPoint13,
                               lControlPoint14,lControlPoint15]
        """
        controlPoints_array = [lControlPoint0,lControlPoint3,lControlPoint2,lControlPoint12,
                               lControlPoint11,lControlPoint16,lControlPoint0] # money!

        
        controlPoints_array_fbx4 = arrayMath.fbx4_convert(controlPoints_array)
        datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key)
        #
        return controlPoints_array_fbx4

