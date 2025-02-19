'''
Title: export_plugin_createFBX_square_depth
Created: 11 February 2024
Author: Clayton Bennett

Update request: 13 May 2024
'''
import arrayMath
import os
from plugins.export_plugin import ExportPlugin

class Plugin(ExportPlugin):
    def plugin(self,createFBX_,datapoint_object):
        
        # style_object specific modules:
        self.node_name_determination(datapoint_object,key=0)
        self.color_coeff_determination(datapoint_object) # run once, for each datapoint
        self.controlPoints_depthPlane(datapoint_object,key=0) # makes call to datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key=key)
        lGeometryNode = createFBX_.geometryNode(datapoint_object,key=0) # makes call to datapoint_object.set_FBX_geometry(lGeometryNode,key=key)
        #lMaterial = createFBX_.material_determination(datapoint_object)#run once for each datapoint. If you want more colors, do that at the dataObjectlevel...
        # but what about datapoints that are complex shapes and characters! Just leave this artifact here...
        # we need a way to represent complex **reusable** shapes...need is a strong word. ignore this for literal years.
        # okay, so how about a surface mesh with a unique four-point geometry? That's means four separate three-value THD coordinates.
        # that can be handled by a specific FBX style_object plug in controlPoints_ method
        #lGeometryNode.AddMaterial(lMaterial)
        return lGeometryNode
    

    def node_name_determination(self,datapoint_object,key=0):#specific
        if datapoint_object.time is not None and datapoint_object.height is not None:
            nodeName_0 = datapoint_object.header_time+":"+str(round(datapoint_object.time,3))+", "+datapoint_object.header_height+":"+str(round(datapoint_object.height,3))+", j:"+str(datapoint_object.j)+"_"
        else:
            nodeName_0 = 'Missing data.'
        datapoint_object.set_node_name(nodeName_0,key=key)
        return nodeName_0   

    def color_coeff_determination(self,datapoint_object):#specific
        datapoint_object.set_color_coeff(datapoint_object.color_coeff)
        # this should migrate somewhere else, especially if it's unity
        return datapoint_object.color_coeff

    def controlPoints_depthPlane(self,datapoint_object,key): # depth plane
        #point_size=20    # manual override
        lControlPoint0 = [datapoint_object.time-self.size_coefficient*datapoint_object.halfwidth_time, datapoint_object.height-self.size_coefficient*datapoint_object.halfwidth_time, datapoint_object.depth-self.size_coefficient*datapoint_object.halfwidth_time]
        lControlPoint1 = [datapoint_object.time-self.size_coefficient*datapoint_object.halfwidth_time, datapoint_object.height+self.size_coefficient*datapoint_object.halfwidth_time, datapoint_object.depth+self.size_coefficient*datapoint_object.halfwidth_time]
        lControlPoint2 = [datapoint_object.time+self.size_coefficient*datapoint_object.halfwidth_time, datapoint_object.height+self.size_coefficient*datapoint_object.halfwidth_time, datapoint_object.depth+self.size_coefficient*datapoint_object.halfwidth_time]
        lControlPoint3 = [datapoint_object.time+self.size_coefficient*datapoint_object.halfwidth_time, datapoint_object.height-self.size_coefficient*datapoint_object.halfwidth_time, datapoint_object.depth-self.size_coefficient*datapoint_object.halfwidth_time]
        
        controlPoints_array = [lControlPoint0,lControlPoint1,lControlPoint2,lControlPoint3]
        controlPoints_array_fbx4 = arrayMath.fbx4_convert(controlPoints_array)
        #print(f'controlPoints_array_fbx4={controlPoints_array_fbx4}')
        datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key)
        return controlPoints_array_fbx4 
