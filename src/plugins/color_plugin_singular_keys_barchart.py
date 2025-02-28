import os
from materials import materials
import colorLerp
class Plugin:
    #materials_object=None
    scene_object = None
    style_object = None
    """ @classmethod
    def add_materials_object(cls,materials_object):
        cls.materials_object = materials_object """

    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object=scene_object
        cls.style_object = scene_object.style_object

    def __init__(self):
        self.friendly_name = 'Color by Barchart Keys'
        self.name = os.path.basename(__file__).removesuffix('.py')
        self.dict_known_datapoint_keys=None

    def prepare_color_style(self):

        color_coeff_list_gradient,color_list = colorLerp.colorAssign_gradient_nested(self.scene_object.vectorArray_height) # color is a factor of height # so it needs allllll at once.

        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():

            #curve_object.color_coeff_list = color_coeff_list[i]
            if curve_object.dict_color_coeff is None:# allows there to be an existing entry,for amultiple color model
                curve_object.dict_color_coeff = dict() # 
            color_by_bar_key = self.make_by_bar_key(curve_object)# add chemicalID names to known direcionary, each of which is assigned a color, as assigned
            #curve_object.dict_color_coeff.update({'Color per Datapoint Key':color_by_bar_key})
            curve_object.dict_color_coeff.update({self.friendly_name:color_by_bar_key})
            #curve_object.color = 'varied'
 
    def make_by_bar_key(self,curve_object):
        # this is wrong: this is for the keyed barchart one
        self.dict_known_datapoint_keys=dict()
        color_by_bar_key = []
        temp_materials_object = materials() # instance rather than class variable (assigned in createFBX)..... Need this first one for the idx of colors

        cc=0
        for key,datapoint_object in curve_object.dict_datapoints.items():
            if key in self.dict_known_datapoint_keys.keys():
                color_coeff = self.dict_known_datapoint_keys[key]
                datapoint_object.cc=temp_materials_object.idx.index(color_coeff)    
                #datapoint_object.color_RGB = 
                #datapoint_object.lMaterial = # not here, later
            else:
                color_coeff = temp_materials_object.idx[cc]
                self.dict_known_datapoint_keys.update({key:color_coeff})
                datapoint_object.cc=cc
                if cc<8:
                    cc+=1
                elif cc==8:
                    cc=0   
            color_by_bar_key.append(color_coeff)
            datapoint_object.color_coeff = color_coeff# get from known list
            datapoint_object.cc = cc
        #print(f'color_by_bar_key = {color_by_bar_key}')
        return color_by_bar_key
    
    def FBX_material(self,datapoint_object,materials_object):# apply in createFBX_ or in export_plugin
        lMaterial = materials_object.lMaterials9_list[datapoint_object.cc]
        return lMaterial
    
    

