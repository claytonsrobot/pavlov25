import os
from pathlib import Path
#from materials import materials
#import colorLerp
class Plugin:
    #materials_object=None
    scene_object = None
    style_object = None
    hierarchy_object = None
    """ @classmethod
    def add_materials_object(cls,materials_object):
        cls.materials_object = materials_object """

    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object=scene_object
        cls.style_object = scene_object.style_object
        cls.hierarchy_object = scene_object.hierarchy_object

    def __init__(self):
        self.friendly_name = 'Color per Curve'
        self.name = Path(__file__).name.lower().removesuffix('.py')
        self.dict_known_datapoint_keys=None
        
    def prepare_color_style(self):
        cc=0
        for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
            if curve_object.dict_color_coeff is None:# allows there to be an existing entry,for amultiple color model
                curve_object.dict_color_coeff = dict() # 
            color_coeff_singular=[cc]*len(curve_object.time)

            curve_object.dict_color_coeff.update({self.friendly_name:color_coeff_singular})
            #curve_object.color = cc  
            #cc+=1
            if cc<8:
                cc+=1
            elif cc==8:
                cc=0 
            
        
            
    def FBX_material(self,datapoint_object,materials_object):# called in in createFBX_
        # we could have the material generated at dict_color_coeff assignment, so that there's no confusion. 
        # this is an FBX publisher, get over it.
        #lMaterial = self.materials_object.lMaterials9_list[datapoint_object.cc]
        lMaterial = materials_object.lMaterials9_list[datapoint_object.color_coeff]# should do more than call 1Materials9_list,call true gradient as well
        #lMaterial = materials_object.lMaterials9_list[datapoint_object.color_coeff] # managed wrong for mutliple colors
        return lMaterial
    
    

