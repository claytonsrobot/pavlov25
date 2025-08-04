import os
#from materials import materials
import colorLerp
class Plugin:
    #materials_object=None
    scene_object = None
    style_object = None
    hierarchy_object = None
    """ @classmethod
    def add_materials_object(cls,materials_object):
        cls.materials_object = materials_object
        #print('materials object added to color_function plugin') """
    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object=scene_object
        cls.style_object = scene_object.style_object
        cls.hierarchy_object = scene_object.hierarchy_object

    def __init__(self):
        self.friendly_name = 'True Gradient'
        self.name = os.path.basename(__file__).removesuffix('.py')

    def prepare_color_style(self):
        for i,curve_object in enumerate(self.hierarchy_object.dict_curve_objects_all.values()):
            color_coeff_list_true_gradient = []
            for height in curve_object.raw.raw_height:
                interp_height_ratio = (height-self.scene_object.min_height)/(self.scene_object.max_height-self.scene_object.min_height)
                color_coeff_list_true_gradient.append(interp_height_ratio)
            if curve_object.dict_color_coeff is None:# allows there to be an existing entry,for amultiple color model
                curve_object.dict_color_coeff = dict() # 
            curve_object.dict_color_coeff.update({self.friendly_name:color_coeff_list_true_gradient}) # actuyally no, this sucks. it works, but it needs a friendly name for the FBX model tree hierarchy.
            #curve_object.color_RBG = 'varied'
    
    def FBX_material(self,datapoint_object,materials_object):# apply in createFBX_ or in export_plugin
        #interp_height_ratio = (datapoint_object.height-self.scene_object.minHeight)/(self.scene_object.max_height-self.scene_object.minHeight)
        #lMaterial = materials_object.create_material_free_FBX(interp_height_ratio)
        lMaterial = materials_object.create_material_free_FBX(datapoint_object.color_coeff)

        return lMaterial
    

