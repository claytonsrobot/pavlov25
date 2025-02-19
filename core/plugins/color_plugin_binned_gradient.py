import os
#from materials import materials
import colorLerp
class Plugin:
    #materials_object=None
    scene_object = None
    style_object = None
    hierarchy_object=None

    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object=scene_object
        cls.style_object = scene_object.style_object
        cls.hierarchy_object = scene_object.hierarchy_object

    def __init__(self):
        self.friendly_name = 'Binned Gradient'
        self.name = os.path.basename(__file__).removesuffix('.py')

    def prepare_color_style(self):
        color_coeff_list_gradient,color_list = colorLerp.colorAssign_gradient_nested(self.scene_object.vectorArray_height) # color is a factor of height # so it needs allllll at once.
        for i,curve_object in enumerate(self.hierarchy_object.dict_curve_objects_all.values()):
            if curve_object.dict_color_coeff is None:# allows there to be an existing entry,for amultiple color model
                curve_object.dict_color_coeff = dict() # 
            curve_object.dict_color_coeff.update({self.friendly_name:color_coeff_list_gradient[i]}) # actuyally no, this sucks. it works, but it needs a friendly name for the FBX model tree hierarchy.
            #curve_object.color = color_coeff_list_gradient[i]
    def FBX_material(self,datapoint_object,materials_object):# apply in createFBX_ or in export_plugin
        #print(f'datapoint_object.color_coeff={datapoint_object.color_coeff}')
        lMaterial = materials_object.assign_materials9_FBX(datapoint_object.color_coeff) # assumes you're on a gradient

        return lMaterial
    

