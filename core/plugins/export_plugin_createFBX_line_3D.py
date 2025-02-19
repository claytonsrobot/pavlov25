'''
Title:export_plugin_createFBX_lineGraph_2D
Created: 10 February 2024
Author: Clayton Bennett

Update request: 13 May 2024
'''
import os
import arrayMath

from plugins.export_plugin import ExportPlugin

class Plugin(ExportPlugin):
    def plugin(self,createFBX_object,datapoint_object):
        
        # style_object specific modules:
        # i think the key=0 vaue is historically for the model_ID, when we were shoving multple materials into a model based on the plotting_style_object list
        self.node_name_determination_2D(datapoint_object,key=0)
        self.color_coeff_determination_delta(datapoint_object) # run once, for each datapoint
        self.controlPoints_lineGraph_3D(datapoint_object,key=0) # four values, in FBXVector4

        lGeometryNode = createFBX_object.geometryNode(datapoint_object,key=0)
        #lMaterial = createFBX_object.material_determination(datapoint_object)#run once for each datapoint. If you want more colors, do that at the dataObjectlevel...
        ######lMaterial = self.style_object.user_input_object.color_function.FBX_material(datapoint_object)
        # but what about datapoints that are complex shapes and characters!  Just leave this artifact here...
        # we need a way to represent complex **reusable** shapes...need is a strong word. ignore this for literal years.
        # okay, so how about a surface mesh with a unique four-point geometry? That's means four separate three-value THD coordinates.
        # that can be handled by a specific FBX style_object plug in controlPoints_ method
        ######lGeometryNode.AddMaterial(lMaterial)    
        return lGeometryNode

    def node_name_determination_2D(self,datapoint_object,key=0):#specific
        if datapoint_object.time is not None and datapoint_object.height is not None:
            nodeName_0 = datapoint_object.header_time+":"+str(round(datapoint_object.time,3))+", "+datapoint_object.header_height+":"+str(round(datapoint_object.height,3))+", j:"+str(datapoint_object.j)+"_"
        else:
            nodeName_0 = 'Missing data.'
        datapoint_object.set_node_name(nodeName_0,key=key)
        return nodeName_0   

    def color_coeff_determination_delta(self,datapoint_object):#specific
        #for use when the geometry links two data points (line graph), rather than representing each point (columns)
        color_coeff_0 = max(datapoint_object.color_coeff,datapoint_object.color_coeff_next) # specific to createFBX_lineGraph_2D
        datapoint_object.set_color_coeff(color_coeff_0)
        return color_coeff_0
    
    def controlPoints_lineGraph_3D(self,datapoint_object,key=0):# specific 
        
        lControlPoint0 = [datapoint_object.time, datapoint_object.height, datapoint_object.depth]
        lControlPoint1 = [datapoint_object.time_next, datapoint_object.height_next, datapoint_object.depth_next] 
        lControlPoint2 = [datapoint_object.time, datapoint_object.height, datapoint_object.depth]

        controlPoints_array = [lControlPoint0,lControlPoint1,lControlPoint2]
        controlPoints_array_fbx4 = arrayMath.fbx4_convert(controlPoints_array)
        datapoint_object.set_controlPoints_array_fbx4(controlPoints_array_fbx4,key=key)
        return controlPoints_array_fbx4