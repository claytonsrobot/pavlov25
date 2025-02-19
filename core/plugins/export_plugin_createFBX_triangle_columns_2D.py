'''
Author: Clayton Bennett
Date Created: 18 July 2023, converted to plugin in mid February 2024
Old name: createFBX_triangleColumns
Purpose:
Apply basic flow of FBX generation and export,
to create a minimalist column style
'''

import os
#from arrayMath import fbx4_convert
import arrayMath
from plugins.export_plugin import ExportPlugin

class Plugin(ExportPlugin):
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

        lControlPoint0 = [datapoint_object.time, 0, 0]
        lControlPoint1 = [datapoint_object.time, datapoint_object.height, self.point_size]
        lControlPoint2 = [datapoint_object.time, datapoint_object.height, 0]
        
        controlPoints_array = [lControlPoint0,lControlPoint1,lControlPoint2]
        controlPoints_array_fbx4 = arrayMath.fbx4_convert(controlPoints_array)
        datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key)
        return controlPoints_array_fbx4
