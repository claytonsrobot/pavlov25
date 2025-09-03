'''
Author: Clayton Bennett
Date Created: 22 May 2024, converted from triangleColumns
Old name: createFBX_squareeColumns
Purpose:
Apply basic flow of FBX generation and export,
to create a minimalist column style

'''
import os
#from arrayMath import fbx4_convert
from pavlov3d import arrayMath
from pavlov3d.plugins.export_plugin import ExportPlugin

class Plugin(ExportPlugin):
    """ def plugin_dataObject(self,createFBX_,dataObject):
        # call from createFBX_ to handle stylistic choices at the dataObject level. What would they be? Dunno :) 
        mystery=1
    #def plugin_datapoint(self,createFBX_,datapoint_object):# rename to this if you ever use the plugin_dataObject """
    def plugin(self,createFBX_,datapoint_object):

        self.node_name_determination(datapoint_object,key=0)
        self.controlPoints_verticalPlane(datapoint_object,key=0) # makes call to datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key=key)
        lGeometryNode = createFBX_.geometryNode(datapoint_object,key=0) #
        return lGeometryNode
    
    def node_name_determination(self,datapoint_object,key):#specific
        nodeName = datapoint_object.header_time+":"+str(round(datapoint_object.time,3))+", "+datapoint_object.header_height+":"+str(round(datapoint_object.height,3))+", j:"+str(datapoint_object.j)+"_"
        datapoint_object.set_node_name(nodeName,key)
        return nodeName

    def controlPoints_verticalPlane(self,datapoint_object,key): # depth plane

        """ lControlPoint0 = [datapoint_object.time - datapoint_object.halfwidth_time, 0, 0]
        lControlPoint1 = [datapoint_object.time + datapoint_object.halfwidth_time, datapoint_object.height, datapoint_object.depth]
        lControlPoint2 = [datapoint_object.time, datapoint_object.height, 0] """
        lControlPoint0 = [datapoint_object.time, 0, 0]
        lControlPoint1 = [datapoint_object.time, 0, datapoint_object.depth]
        lControlPoint2 = [datapoint_object.time, datapoint_object.height, datapoint_object.depth]
        lControlPoint3 = [datapoint_object.time, datapoint_object.height, 0]
        
        controlPoints_array = [lControlPoint0,lControlPoint1,lControlPoint2,lControlPoint3]
        controlPoints_array_fbx4 = arrayMath.fbx4_convert(controlPoints_array)
        datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key)
        return controlPoints_array_fbx4