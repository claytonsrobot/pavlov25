'''
Title: datapoint_FBX.py
Created: 10 February 2024
Author: Clayon Bennett
Purpose: object to hold data for each datapoint,as generated in createrFBX.
Classically has been a list called triangle_vars

'''

class DataPoint:
    style_object = None
    @classmethod
    def assign_style_object(cls, style_object):
        cls.style_object = style_object

    allowed_keys = set(['parent','time',
                        'height','depth','point_size',
                    'time_next','height_next','depth_next',
                    'j','header_time','header_height','header_depth',
                    'model_ID','color_coeff','color_coeff_next',
                    'lMaterial',
                    'controlPoints_array_fbx4',
                    'halfwidth_time',
                    'halfwidth_height',
                    'halfwidth_depth',
                    'halfwidth_time_next',
                    'halfwidth_height_next',
                    'halfwidth_depth_next'])
    
    # security risk
    #@classmethod # means that these attributes will be permanently added for all instances during this run of the program
    #def add_non_standard_attributes(cls,non_standard_attributes): 
    #    allowed_keys = allowed_keys.union(non_standard_attributes)
        # called in import plugin, beofre data points are created
            
    def __init__(self,curve_object):
        #self.name = self.parent.name+str(self.j)
        #https://stackoverflow.com/a/40631881
        self.__dict__.update((key, None) for key in self.allowed_keys)
        self.parent = curve_object
        # these dictionaries are here to allow for multiple geometry nodes to then be made children of one node for the datapoint
        # for things like plus style, or character sprites (though currently material determination is drived by self.color_coeff, so all planes are the same color)
        self.controlPoints_array_fbx4_dict = dict()# can hold more than one, like for plus style
        self.lMaterial_dict = dict()
        self.lGeometryNode_dict = dict()
        self.nodeName_dict = dict() #
        self.dict_data_raw = dict()
        self.dict_data_scaled = dict()
        #self.color_coeff_dict = dict()
        #self.color_coeff=None
        self.point_size = self.style_object.point_size
        ##self.cc=None # integer 0 through 8 # only used for binned gradient?

    def set_vars(self,**kwargs):
        self.__dict__.update((key, value) for key, value in kwargs.items() if key in self.allowed_keys)
    
    def set_node_name(self,nodeName,key):
        #self.nodeName = nodeName
        self.nodeName_dict.update({key:nodeName})

    def set_FBX_material(self,lMaterial):#,key):
        self.lMaterial = lMaterial
        #self.lMaterial_dict.update({key:lMaterial})
        # alright: these should be duplicates. A data point does not need to have multiple object or colors: diverse surfaces can belong to the curve_object, not the datapoint

    def set_FBX_geometry(self,lGeometryNode,key):
        #self.lGeometryNode = lGeometryNode
        self.lGeometryNode_dict.update({key:lGeometryNode})

    def set_controlPoints_array_fbx4(self,controlPoints_array_fbx4,key):
        #self.controlPoints_array_fbx4 = controlPoints_array_fbx4
        self.controlPoints_array_fbx4_dict.update({key:controlPoints_array_fbx4})

    def set_color_coeff(self,color_coeff):
        self.color_coeff = color_coeff
        #self.color_coeff_dict.update({key:color_coeff})
        # alright: these should be duplicates. A data point does not need to have multiple object or colors: diverse surfaces can belong to the curve_object, not the datapoint 
