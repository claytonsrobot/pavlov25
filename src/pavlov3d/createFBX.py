'''
Author: Clayton Bennett
Date re-created: 10 January 2024, from original source July 2023
Name: createFBX_.py
Purpose:
Apply basic flow of FBX generation and export,
T be inherited by other create_FBX stylistic versions
'''
# https://stackoverflow.com/questions/62925571/how-do-i-use-env-in-django # security
''' Mock Up'''
'''
Initialize SDK Manage and Scene and
Initialize a Root node
Initialize An object node
Create FBX polygons, with materials/colors
Add polygons to object node
Add object node to root node
Save scene
#Destroy SDK manager
Exit

18 July 2023:
Rip out excess, that seems to accomplish nothing: lLayer and lMaterialLayer
    lMaterialLayer=FbxLayerElementMaterial.Create(lQuadMesh, "")
    lLayerElementNormal=FbxLayerElementNormal.Create(lQuadMesh, "")
    lLayer.SetNormals(lLayerElementNormal)
    Not need to use SetMappingMode or SetReferenceMode
Put back in!

It has been confirmed that in Blender and internally to this Mesh, there is only 1 polygon. That's great.
When imported into Autodesk FBX Review, the polygon count is shown as 2, with triangles drawn.
The goal was to minimize polygons by using a single quadrilateral instead of two triangles. Time to move on from this.
It may be feasible that some viewers automatically convert all quads to triangles, and if this is the case, minimalist triangle-based geometry style should be made available.

Resuse material and scale color, rather than recreating material for each polygon/mesh. 
Why doesn't this work? It doesn't. Oh well.
FAILED!

Goal:
Make color relative to average of two height values: This should happen at the dashboard level.
Also, at dashboard level, dump in vector_heightArray and vector_timeArray values.
Changes, pass in header dimensions from raw CSV files, to node names in triangleColumn file

As of 29 January 2024, Any reference to ".scene_origin" refers to the scene_object.minimum_edge_at_zero_height_plane, which is 0,0,0 in the FBX model 

10 January 2024
How does this version of create_FBX differ from others? 
We should create a base class than can then be inherited by the specific create_FBX versions.
'''

''' Python Version '''
import sys
import os
import numpy as np
import math
import copy
#import blob
from pavlov3d import environment
if environment.fbx_enabled():
    #csv_uploads_pavlovdata
    #from fbx import 
    from fbx import FbxVector4 
    from fbx import FbxNode 
    from fbx import FbxDouble3
    from fbx import FbxMesh # for node creation

    #from fbx import FbxSurfacePhong
    from fbx import FbxScene
    from fbx import FbxManager
    from fbx import FbxIOSettings
    from fbx import IOSROOT

    from pavlov3d.metadata import create_fbxPropertiesFrom_df_metadata

    """ #C:\Program Files\Autodesk\FBX\FBX Python SDK\2020.3.2\samples\ImportScene\DisplayUserProperties.py
    from fbx import FbxProperty # metadata
    from fbx import FbxString
    #from fbx import FbxObjectMetaData # nope
    from fbx import FbxObject # supposedly not different from FbxObjectMetaData
    from fbx import FbxPropertyFlags """

    #lProperty = pObject.GetFirstProperty()
    #lProperty.GetFlag(FbxPropertyFlags.eUserDefined):
    #lString = lProperty.GetLabel() # display name
    #lString = lProperty.GetName() # internal name
    #lPropertyDataType=lProperty.GetPropertyDataType()  

    # from fbx import FbxDocument
    #from fbx import fbxsip
    from fbx import FbxExporter
    from fbx import EXP_FBX_MATERIAL
    from fbx import EXP_FBX_TEXTURE
    from fbx import EXP_FBX_EMBEDDED

from pavlov3d import environment
from pavlov3d.directories import Directories
if environment.vercel()==True:
    from .home.session import add_fbx_file_to_blob_dir
from pavlov3d.text_translation import TranslationFinal
from pavlov3d.lines_FBX import LinesFBX
from pavlov3d.conditional_import import conditional_import
from pavlov3d.materials import materials
#from materials import create_materials_9bins_FBX
#from materials import create_material_free_FBX
#from materials import assign_materials9_FBX # this is where the magic happens # get gradient colors vs solid colors-in-turn


def _import_fbx_layer_modules(style_object,conditional_import_object):# bit outdated now that all is class-ical.
    if style_object.calculate_FBX_normal_and_material_layers:
        from fbx import FbxLayerElement # not used currenty, in _set_material_layer
        from fbx import FbxLayerElementNormal # not used currenty, in _set_material_layer
        from fbx import FbxLayerElementMaterial # not used currenty, in _set_material_layer
        conditional_import_object.FbxLayerElement = FbxLayerElement
        conditional_import_object.FbxLayerElementNormal = FbxLayerElementNormal
        conditional_import_object.FbxLayerElementMaterial = FbxLayerElementMaterial

class CreateFBX:
    # this currently is set up for styles that have one node per datapoint
    style_object = None
    scene_object = None
    user_input_object = None
    hierarchy_object = None
    lSdkManager = None
    lRootNode = None
    lScene = None
    lFileFormat = None
    lEmbedMedia = None
    conditional_import_object = None
    plotting_style_plugin_object = None
    export_control_object = None
    
    def __init__(self,filename_FBX,file_encoding):
        self.filename_FBX = filename_FBX
        self.file_encoding = file_encoding
        self.lMaterials9_list = None # set by _set_lMaterials9_list()
        self.materials_object = None
        self.group_nodes = None 
        self.group_names = None 
        self.model_ID = None
        self.lines_FBX_machine = LinesFBX()
        #self.assign_scene_variables(scene_object) # called externally in main.py
        #self._create_FBX()
        # tracker vars # ugly, but effective. # replace with dictionaries, with shared keys to 
        # specifically for ['barchart_keys_color_model']

    @classmethod
    def assign_scene_variabes(cls, scene_object):
        cls.scene_object = scene_object
        cls.style_object = scene_object.style_object
        cls.user_input_object = scene_object.user_input_object
        cls.hierarchy_object = scene_object.hierarchy_object
        LinesFBX.asign_scene_object(scene_object)   
        cls.conditional_import_object = conditional_import()
        _import_fbx_layer_modules(cls.style_object,cls.conditional_import_object)

    @classmethod
    def assign_plotting_style_plugin(cls,plotting_style_plugin_object):
        cls.plotting_style_plugin_object = plotting_style_plugin_object

    def assign_export_control_object(self,export_control_object):
        self.export_control_object = export_control_object

    def assign_import_function_(self,import_function):
        self.import_function = import_function

    """ def assign_color_function_dict(self,color_function_dict):# assigned where? in style_object.py
        self.color_function_dict = color_function_dict """

    def assign_color_function_list(self,color_function_list):# assigned where? in style_object.py
        #self.color_function_dict = color_function_dict
        self.color_function_list = color_function_list

    @classmethod
    def assign_FBX_SDK_variables(cls,lSdkManager,lScene,lFileFormat,lEmbedMedia,lRootNode):
        cls.lSdkManager = lSdkManager
        cls.lRootNode = lRootNode
        cls.lScene = lScene
        cls.lFileFormat = lFileFormat
        cls.lEmbedMedia = lEmbedMedia
        LinesFBX.assign_FBX_SdkManager(lSdkManager)
        
    
    def generate_model(self):
        #self.filename_FBX = filename_FBX
        #self.file_encoding = file_encoding
        self._initialize_SDK_objects() # makes call to assign_FBX_SDK_variables()
        self._set_lMaterials9_list() # interally references self.lSdkManager
        self._initialize_and_link_top_level_hierarchy()

        self._build_all_model_color_versions() # the heavy lifting

        self._build_curve_accssories()
        self._build_group_fences() # interally references self.lSdkManager, self.lRootNode, and self.group_names,
        self._build_group_texts()
        self._attach_or_destroy_top_nodes()
        self._save_scene() # interally references self.filename_FBX, self.lFileFormat, self.lSdkManager and self.lScene

    def _set_lMaterials9_list(self):
        # Create stock colors, to be assigned  at creation of each column
        self.materials_object =  materials()
        self.materials_object.assign_lSdkManager(self.lSdkManager)
        self.lMaterials9_list = self.materials_object.lMaterials9_list

    
    def _initialize_and_link_top_level_hierarchy(self):
        self.lModelNode_top = FbxNode.Create(self.lSdkManager,'Models_') # models attached in self._build_model_version_with_curves()

        self.lTextsNode_top = FbxNode.Create(self.lSdkManager,'Texts_')
        self.lTextsNode_groups_tier1 = FbxNode.Create(self.lSdkManager,'Texts_Groups_Tier_1_')
        self.lTextsNode_groups_tier2 = FbxNode.Create(self.lSdkManager,'Texts_Groups_Tier_2_')
        self.lTextsNode_curves = FbxNode.Create(self.lSdkManager,'Texts_Curves_')
        self.lTextsNode_scene_description = FbxNode.Create(self.lSdkManager,'Texts_Scene_Description_')

        self.lTickNumbersNodes_curves = FbxNode.Create(self.lSdkManager,'Numbers_Ticks_')
        self.lTickNumbersNodes_exploded = FbxNode.Create(self.lSdkManager,'Numbers_Ticks_Exploded_')

        self.lAxesNode_top = FbxNode.Create(self.lSdkManager,'Axes_')
        self.lAxesNodes_exploded = FbxNode.Create(self.lSdkManager,'Axes_Exploded_')
        self.lAxesNodes_curves = FbxNode.Create(self.lSdkManager,'Axes_Curves_')

        self.lTicksNode_top = FbxNode.Create(self.lSdkManager,'Ticks_')
        self.lTicksNodes_exploded = FbxNode.Create(self.lSdkManager,'Ticks_Exploded_')
        self.lTicksNodes_curves = FbxNode.Create(self.lSdkManager,'Ticks_Curves_')

        self.lFencesNode_top = FbxNode.Create(self.lSdkManager,'Fences_')
        self.lFencesNode_groups_tier1 = FbxNode.Create(self.lSdkManager,'Fences_Groups_Tier_1_')
        self.lFencesNode_groups_tier2 = FbxNode.Create(self.lSdkManager,'Fences_Groups_Tier_2_')
        self.lFencesNodes_curves = FbxNode.Create(self.lSdkManager,'Fences_Curves_')

        @staticmethod
        def _link_top_level_hierarchy(self):
        
            self.lFencesNode_top.AddChild(self.lFencesNode_groups_tier1)
            self.lFencesNode_top.AddChild(self.lFencesNode_groups_tier2)

            self.lTextsNode_top.AddChild(self.lTextsNode_groups_tier1)
            self.lTextsNode_top.AddChild(self.lTextsNode_groups_tier2)
            self.lTextsNode_top.AddChild(self.lTextsNode_curves)
            self.lTextsNode_top.AddChild(self.lTextsNode_scene_description)
            self.lTextsNode_top.AddChild(self.lTickNumbersNodes_curves)
            
            self.lAxesNode_top.AddChild(self.lAxesNodes_curves)
            self.lAxesNode_top.AddChild(self.lAxesNodes_exploded)
            
            self.lTicksNode_top.AddChild(self.lTicksNodes_curves)
            self.lTicksNode_top.AddChild(self.lTicksNodes_exploded)

        _link_top_level_hierarchy(self)

        #self.lRootNode.AddChild(self.lFencesNode_top)
        #self.lRootNode.AddChild(self.lTextsNode_top)
        #self.lRootNode.AddChild(self.lAxesNode_top)

    def _attach_or_destroy_top_nodes(self):
        nodes = [\
        self.lModelNode_top, # later 
        self.lTextsNode_top,
        self.lAxesNode_top,
        self.lTicksNode_top,
        self.lFencesNode_top,
        ]

        def check_if_empty(node):
            bool_empty=True

            if node.GetChildCount()==0:
                bool_empty=False

            return bool_empty
        
        def attach_top_node_to_root_node_or_destroy(node):
            if check_if_empty(node):
                self.lRootNode.AddChild(node)
            else:
                node.Destroy()

        for i,node in enumerate(nodes):
            attach_top_node_to_root_node_or_destroy(node)

    def _initialize_and_link_curves_and_groups(self,lModelNode):
        #self._initialize_scene_node()
        self._initialize_and_link_group_tier1_nodes(lModelNode)
        self._initialize_and_link_group_tier2_nodes()
        self._initialize_and_link_curve_nodes()

    def _build_all_model_color_versions(self):
        print("_build_all_model_color_versions(")
        for i,color_plugin_object in enumerate(self.style_object.color_function_list):
            print(f"i:{i}")
            if i <= len(self.style_object.export_function_list)-1:
                export_plugin_object = self.style_object.export_function_list[i]
            else:
                export_plugin_object = self.style_object.export_function_list[0]
            print(f'\ncolor_plugin_object = {color_plugin_object}')
            self._build_model_version_with_curves(color_plugin_object,export_plugin_object)

    def _build_model_version_with_curves(self, color_plugin_object,export_plugin_object):
        model_ID,lModelNode = self._prep_model(color_plugin_object)
        print("_build_model_version_with_curves()")
        self._initialize_and_link_curves_and_groups(lModelNode)
        self.generate_hierarchy_with_specific_color_style(color_plugin_object,model_ID,export_plugin_object)

    def _prep_model(self,color_plugin_object):
        model_ID = color_plugin_object.friendly_name
        self.lModelNode = FbxNode.Create(self.lSdkManager,'Model: '+model_ID) #name=model_ID # will be overwritten.
        self.lModelNode_top.AddChild(self.lModelNode)
        return model_ID,self.lModelNode

    def _link_to_supernode(self,childnode,supernode):
        supernode.AddChild(childnode)

    def _initialize_scene_node(self):
        self.scene_node = FbxNode.Create(self.lSdkManager,'Model: '+'fix') # the hell is this 21 Dec 24
        #lModelNode_top = FbxNode.Create(self.lSdkManager,'Model: '+model_ID) #name=model_ID
    
    def _initialize_and_link_group_tier1_nodes(self,lModelNode):
        self.dict_group_t1_nodes = dict()
        for name_gt1, group_t1_object in self.hierarchy_object.dict_tier_objects[1].dict_group_objects.items():
            group_t1_node = FbxNode.Create(self.lSdkManager,name_gt1+'_')
            translation_vector = group_t1_object.data_origin_relative_to_supergroup_data_origin
            self._set_object_default_position(group_t1_node, translation_vector)
            self.dict_group_t1_nodes.update({name_gt1:group_t1_node})
            if False: 
                self._link_to_supernode(group_t1_node,supernode = self.lModelNode_top)
            else:
                self._link_to_supernode(group_t1_node,supernode = lModelNode)

    def _initialize_and_link_group_tier2_nodes(self):
        self.dict_group_t2_nodes = dict()
        for name_gt2,group_t2_object in self.hierarchy_object.dict_tier_objects[2].dict_group_objects.items():
            group_t2_node = FbxNode.Create(self.lSdkManager,name_gt2+'_')
            translation_vector = group_t2_object.data_origin_relative_to_supergroup_data_origin
            self._set_object_default_position(group_t2_node, translation_vector)
            self.dict_group_t2_nodes.update({name_gt2:group_t2_node})
            self._link_to_supernode(group_t2_node,supernode = self.dict_group_t1_nodes[group_t2_object.supergroup.name])
        self.dict_group_nodes = {**self.dict_group_t1_nodes,**self.dict_group_t2_nodes}

    def _initialize_and_link_curve_nodes(self):
        self.dict_curve_nodes = dict()
        for name_c,curve_object in self.hierarchy_object.dict_tier_objects[3].dict_curve_objects.items():
            curve_node = FbxNode.Create(self.lSdkManager,name_c+'_')
            translation_vector = curve_object.data_origin_relative_to_supergroup_data_origin
            self._set_object_default_position(curve_node,translation_vector)
            self.dict_curve_nodes.update({name_c:curve_node})
            self._link_to_supernode(curve_node,supernode = self.dict_group_t2_nodes[curve_object.supergroup.name])
        
    def _build_curve_accssories(self):
        self._build_curve_axes()
        self._build_curve_texts()
        self._build_curve_ticks()
        self._build_curve_fences()
        self._build_local_tick_numbering()
        if False:
            self._build_exploded_ticks()
            self._build_exploded_tick_numbering()

    def _build_curve_axes(self):
        for key,curve_object in self.hierarchy_object.dict_curve_objects_all.items():
            lCurveObjectNode = self.dict_curve_nodes[key]
            lAxesNode_curve = self.lines_FBX_machine.linesNode(lines_array=curve_object.axis_array,nodeName="Axes: "+curve_object.name+"_")
            if self.style_object.createFBX_embed_axes_in_curve_object_at_scene_level_or_curve_level_or_none=='curve':
                translation_vector = [0,0,0]
                self._set_object_default_position(lAxesNode_curve,translation_vector)
                lCurveObjectNode.AddChild(lAxesNode_curve)
            elif self.style_object.createFBX_embed_axes_in_curve_object_at_scene_level_or_curve_level_or_none=='scene':
                translation_vector = curve_object.data_origin_relative_to_scene_data_origin
                self._set_object_default_position(lAxesNode_curve,translation_vector)
                if self.lAxesNodes_curves.GetChildCount()<len(self.hierarchy_object.dict_curve_objects_all):
                    self.lAxesNodes_curves.AddChild(lAxesNode_curve)

    def _build_curve_ticks(self):
        for key,curve_object in self.hierarchy_object.dict_curve_objects_all.items():
            lCurveObjectNode = self.dict_curve_nodes[key]
            lTicksNode_curve = self.lines_FBX_machine.linesNode(lines_array=curve_object.ticks_arrays,nodeName="Ticks: "+curve_object.name+"_")
            if self.style_object.createFBX_embed_ticks_in_curve_object_at_scene_level_or_curve_level_or_none=='curve':
                translation_vector = [0,0,0]
                self._set_object_default_position(lTicksNode_curve,translation_vector)
                self.lTicksNodes_curves.AddChild(lTicksNode_curve)
            elif self.style_object.createFBX_embed_ticks_in_curve_object_at_scene_level_or_curve_level_or_none=='scene':
                translation_vector = curve_object.data_origin_relative_to_scene_data_origin
                self._set_object_default_position(lTicksNode_curve,translation_vector)
                if self.lTicksNodes_curves.GetChildCount()<len(self.hierarchy_object.dict_curve_objects_all):
                    self.lTicksNodes_curves.AddChild(lTicksNode_curve)

    def _build_exploded_ticks(self):
        for key,curve_object in self.hierarchy_object.dict_curve_objects_all.items():
            lCurveObjectNode = self.dict_curve_nodes[key]
            lTicksNode_exploded = self.lines_FBX_machine.linesNode(lines_array=curve_object.ticks_arrays,nodeName="Exploded Ticks: "+curve_object.name+"_")
            if self.style_object.createFBX_embed_ticks_in_curve_object_at_scene_level_or_curve_level_or_none=='curve':
                translation_vector = [0,0,0]
                self._set_object_default_position(lTicksNode_exploded,translation_vector)
                self.lTicksNodes_exploded.AddChild(lTicksNode_exploded)
            elif self.style_object.createFBX_embed_ticks_in_curve_object_at_scene_level_or_curve_level_or_none=='scene':
                translation_vector = curve_object.data_origin_relative_to_scene_data_origin
                self._set_object_default_position(lTicksNode_exploded,translation_vector)
                if self.lTicksNodes_exploded.GetChildCount()<len(self.hierarchy_object.dict_curve_objects_all):
                    self.lTicksNodes_exploded.AddChild(lTicksNode_exploded)
        
    def _build_curve_texts(self):
        # separate axis tests and title texts
        for key,curve_object in self.hierarchy_object.dict_curve_objects_all.items():
            lCurveObjectNode = self.dict_curve_nodes[key]
            texts_array=[]
            #text_label_object = curve_object.dict_text_labels['']# here is where it grabs them # call by key instead, expicitly
            # must check if it has
            text_label_object = copy.copy(curve_object.dict_text_labels['title_'])
            texts_array.extend(text_label_object.characters_array)
            text_label_object = copy.copy(curve_object.dict_text_labels['axis_time_'])
            texts_array.extend(text_label_object.characters_array)
            text_label_object = copy.copy(curve_object.dict_text_labels['axis_height_'])
            texts_array.extend(text_label_object.characters_array)
            text_label_object = copy.copy(curve_object.dict_text_labels['axis_depth_'])
            texts_array.extend(text_label_object.characters_array)
            ''' # turn on
            text_label_object = copy.copy(curve_object.dict_text_labels['tick_numbers_time_axis_'])
            texts_array.extend(text_label_object.characters_array)
            text_label_object = copy.copy(curve_object.dict_text_labels['tick_numbers_height_axis_'])
            texts_array.extend(text_label_object.characters_array)
            text_label_object = copy.copy(curve_object.dict_text_labels['tick_numbers_depth_axis_'])
            texts_array.extend(text_label_object.characters_array)
            '''
            name = "Texts: "+curve_object.name+"_"
            lTextsNode_curve = self.lines_FBX_machine.linesNode(lines_array=texts_array,nodeName=name) # wild: does this need to be called as FBX specfic? 
            if self.style_object.createFBX_embed_text_in_curve_object_at_scene_level_or_curve_level_or_none == 'curve': # default, tried and true for all of 2024, and before and after
                translation_vector = [0,0,0]
                self._set_object_default_position(lTextsNode_curve,translation_vector)
                lCurveObjectNode.AddChild(lTextsNode_curve)
            elif self.style_object.createFBX_embed_text_in_curve_object_at_scene_level_or_curve_level_or_none == 'scene':
                translation_vector = curve_object.data_origin_relative_to_scene_data_origin
                self._set_object_default_position(lTextsNode_curve,translation_vector)
                if self.lTextsNode_curves.GetChildCount()<len(self.hierarchy_object.dict_curve_objects_all):
                    self.lTextsNode_curves.AddChild(lTextsNode_curve)

    def _build_local_tick_numbering(self):
        # this would work better with a dedicated tick numbering dictionary for each curve
        # that, or you can shove multiple tick numbering into the same charcater array...but to do thaat we can use the dictionary as well
        for key,curve_object in self.hierarchy_object.dict_curve_objects_all.items():
            lCurveObjectNode = self.dict_curve_nodes[key]
            #if curve_object.tick_numbering_object_height is not None:
            if len(curve_object.dict_tick_numbering) > 0:
                texts_array = []
                for key,value in curve_object.dict_tick_numbering.items():
                    texts_array.extend(value.characters_array)
                    #text_label_object = copy.copy(curve_object.dict_text_labels['tick_numbering']) register for expansion but dont use here
                name = "Tick Numbers: "+curve_object.name+"_"
                lTickNumbersNode_curve = self.lines_FBX_machine.linesNode(lines_array=texts_array,nodeName=name)

                if self.style_object.createFBX_embed_text_in_curve_object_at_scene_level_or_curve_level_or_none == 'scene':
                    translation_vector = curve_object.data_origin_relative_to_scene_data_origin
                    self._set_object_default_position(lTickNumbersNode_curve,translation_vector)
                    if self.lTickNumbersNodes_curves.GetChildCount()<len(self.hierarchy_object.dict_curve_objects_all):
                        self.lTickNumbersNodes_curves.AddChild(lTickNumbersNode_curve)

                elif self.style_object.createFBX_embed_text_in_curve_object_at_scene_level_or_curve_level_or_none == 'curve':
                    translation_vector = [0,0,0]
                    self._set_object_default_position(lTickNumbersNode_curve,translation_vector)
                    lCurveObjectNode.AddChild(lTickNumbersNode_curve)
            
    def _build_exploded_tick_numbering(self):
        #no i hate it.

        for key,curve_object in self.hierarchy_object.dict_curve_objects_all.items():
            lCurveObjectNode = self.dict_curve_nodes[key]

            explosion_translation_time = np.array([self.scene_object.diameter[0],0,0])
            explosion_translation_height = np.array([0,self.scene_object.diameter[1],0])
            explosion_translation_depth = np.array([0,0,self.scene_object.diameter[2]])

            texts_array = curve_object.tick_numbering.characters_array
            name = "Tick Numbers: "+curve_object.name+"_"
            lTickNumbersNode_curve = self.lines_FBX_machine.linesNode(lines_array=texts_array,nodeName=name)
            if self.style_object.createFBX_embed_text_in_curve_object_at_scene_level_or_curve_level_or_none == 'scene':
                translation_vector = curve_object.data_origin_relative_to_scene_data_origin - explosion_translation_depth
                self._set_object_default_position(lTickNumbersNode_curve,translation_vector)
                if self.lTickNumbersNodes_curves.GetChildCount()<len(self.hierarchy_object.dict_curve_objects_all):
                    self.lTickNumbersNodes_curves.AddChild(lTickNumbersNode_curve)

            # dont do this
            elif self.style_object.createFBX_embed_text_in_curve_object_at_scene_level_or_curve_level_or_none == 'curve':
                translation_vector = np.array([0,0,0]) - explosion_translation_depth
                self._set_object_default_position(lTickNumbersNode_curve,translation_vector)
                lCurveObjectNode.AddChild(lTickNumbersNode_curve)

    def _build_curve_fences(self):
        for key,curve_object in self.hierarchy_object.dict_curve_objects_all.items():
            lCurveObjectNode = self.dict_curve_nodes[key]
            if self.style_object.createFBX_embed_fence_in_curve_object_at_scene_level_or_curve_level_or_none == 'scene': # works either way
                lFencesNodes_curves = FbxNode.Create(self.lSdkManager,"Fences_Curves_")
                for curve_object in self.hierarchy_object.dict_curve_objects_all.values():
                    lFenceNode_curve = self.lines_FBX_machine.linesNode(lines_array=curve_object.fence_lines,nodeName="Fences: "+curve_object.name+"_") 
                    translation_vector = [0,0,0] 
                    self._set_object_default_position(lFenceNode_curve,translation_vector)
                    lFencesNodes_curves.AddChild(lFenceNode_curve)
                self.lFencesNode_top.AddChild(lFencesNodes_curves)

            # dont do this
            elif self.style_object.createFBX_embed_fence_in_curve_object_at_scene_level_or_curve_level_or_none== 'curve':
                lFenceNode_curve = self.lines_FBX_machine.linesNode(lines_array=curve_object.fence_lines,nodeName="Fences: "+curve_object.name+"_")   
                #translation_vector = np.multiply(-1,curve_object.data_origin_relative_to_scene_minimum_edge_at_zero_height_plane) # data origin is embedded into the nature of the fence
                translation_vector = np.multiply(-1,curve_object.data_origin_relative_to_scene_data_origin)
                self._set_object_default_position(lFenceNode_curve,translation_vector)
                lCurveObjectNode.AddChild(lFenceNode_curve)
    
    
    def _build_group_fences(self):
        for key, group_object in self.hierarchy_object.dict_group_objects_all.items(): 
            if not(group_object.fence_lines is None):
                fence_label = 'Fences: '+group_object.name
                fence_lines = group_object.fence_lines

                lFenceNode = self.lines_FBX_machine.linesNode(lines_array=fence_lines,nodeName=fence_label) # feeds in all axes and ticks for a single data object

                if self.style_object.group_fences_embedded_at_scene_level_or_group_level=='scene': # default
                    # without adding translation, it has already been applied / it is inferred that the trnslations is already minimum_edge_at_zero_height_plane_relative_to_supergroup_minimum_edge_at_zero_height_plane
                    self.lFencesNode_top.AddChild(lFenceNode)
                    if group_object.tier_level == 1:
                        self.lFencesNode_groups_tier1.AddChild(lFenceNode)
                    elif group_object.tier_level == 2:
                        self.lFencesNode_groups_tier2.AddChild(lFenceNode)


    def _build_group_texts(self):
        
        for key, group_object in self.hierarchy_object.dict_group_objects_most.items(): 
            
            if len(group_object.dict_text_labels) > 0: 

                texts_array=[]
                for text_label_object in group_object.dict_text_labels.values():
                    texts_array.extend(text_label_object.characters_array)
                lTextNode_group=self.lines_FBX_machine.linesNode(lines_array=texts_array,nodeName="Texts_"+group_object.name+"_")

                if self.style_object.group_texts_embedded_at_scene_level_or_group_level=='scene': # this is why the hack is here. But, we can make the choice.
                    
                    translation_vector = TranslationFinal.final_group_label_translation_relative_to_scene_fence(group_object)
                    #print(f"createFBX._build_group_texts(): translation_vector = {translation_vector}")
                    if group_object.tier_level == 1:
                        self._set_object_default_position(lTextNode_group,translation_vector)
                        self.lTextsNode_groups_tier1.AddChild(lTextNode_group)

                    elif group_object.tier_level == 2:
                        self._set_object_default_position(lTextNode_group,translation_vector)
                        self.lTextsNode_groups_tier2.AddChild(lTextNode_group)

                elif self.style_object.group_texts_embedded_at_scene_level_or_group_level=='group': # works....why doesnt; it work for the fence then?
                    lGroupNode = self.dict_group_nodes[key]
                    translation_vector = [0,0,0]
                    self._set_object_default_position(lTextNode_group,translation_vector)
                    lGroupNode.AddChild(lTextNode_group) #"""
    
    def nest_at_top(self,child_object):
        self.lRootNode.AddChild(child_object)
        True

    def _initialize_SDK_objects(self):
        # The first thing to do is to create the FBX SDK manager which is the 
        # object allocator for almost all the classes in the SDK.
        self.lSdkManager = FbxManager.Create()
        if not self.lSdkManager:
            sys.exit(0)
        
        ios = FbxIOSettings.Create(self.lSdkManager, IOSROOT)
        self.lSdkManager.SetIOSettings(ios)
        #https://stackoverflow.com/questions/35549348/how-to-fbx-sdk-export-binary-fbx-file-with-python
        lFileFormat,lEmbedMedia = self._set_file_type(self.file_encoding) # where file_encoding is 'ascii' or 'bin'
        self.lSdkManager.GetIOSettings().SetBoolProp(EXP_FBX_MATERIAL, True)
        self.lSdkManager.GetIOSettings().SetBoolProp(EXP_FBX_TEXTURE, True)
        self.lSdkManager.GetIOSettings().SetBoolProp(EXP_FBX_EMBEDDED, lEmbedMedia) # False if you want ASCII, True if you want BIN

        # Create the entity that will hold the scene.
        lScene = FbxScene.Create(self.lSdkManager, "")
        lRootNode = lScene.GetRootNode()
        self.assign_FBX_SDK_variables(self.lSdkManager,lScene,lFileFormat,lEmbedMedia,lRootNode)

    def _set_object_default_position(self,pFileObject,translation_vector):
        [objectTime_translation_i,objectHeight_translation_i,objectDepth_translation_i] = translation_vector
        # variable names reflect the THD (time, height, depth) paradigm
        pFileObject.LclTranslation.Set(FbxDouble3(objectTime_translation_i,
                                                objectHeight_translation_i,
                                                objectDepth_translation_i))
        pFileObject.LclRotation.Set(FbxDouble3(0.0, 0.0, 0.0))
        pFileObject.LclScaling.Set(FbxDouble3(1.0, 1.0, 1.0))

    def _set_file_type(self,file_encoding):
        pFileFormat = self.lSdkManager.GetIOPluginRegistry().GetNativeWriterFormat()
        lFormatCount = self.lSdkManager.GetIOPluginRegistry().GetWriterFormatCount()
        for lFormatIndex in range(lFormatCount):
            if self.lSdkManager.GetIOPluginRegistry().WriterIsFBX(lFormatIndex):
                lDesc = self.lSdkManager.GetIOPluginRegistry().GetWriterFormatDescription(lFormatIndex)
                if file_encoding in lDesc:
                    pFileFormat = lFormatIndex
                    break
        if file_encoding.lower() == 'bin':
            pEmbedMedia = True
        else:
            pEmbedMedia = False
        return pFileFormat, pEmbedMedia

    #https://github.com/3DTech-Steven7/python-fbx/blob/master/maya_37/fbx/FbxCommon.py
    def _save_scene(self):
        lExporter = FbxExporter.Create(self.lSdkManager, "")
        result = lExporter.Initialize(self.filename_FBX, self.lFileFormat, self.lSdkManager.GetIOSettings())
        if result is True:
            
            #print(f'environment.vercel()={environment.vercel()}')
            
            if environment.vercel()==True:
                os.chdir("/tmp/")
                result = lExporter.Export(self.lScene)
                print(f'self.filename_FBX = {self.filename_FBX}')
                add_fbx_file_to_blob_dir(self.filename_FBX)
                result = None
                    
            else:
                os.chdir(self.scene_object.exportdir) # change working directory to exportdir
                
                
                result = lExporter.Export(self.lScene)
            os.chdir(Directories.get_program_dir()) # change working directory # stop changing directories and instead just know where you are at. learn to notate relative directories.
        lExporter.Destroy()
        return result

    
    def generate_hierarchy_with_specific_color_style(self,color_plugin_object,model_ID,export_plugin_object):
        print("generate_hierarchy_with_specific_color_style")
        print(f"model = {model_ID}")
        for key,lCurveObjectNode in self.dict_curve_nodes.items():
            curve_object = self.hierarchy_object.dict_curve_objects_all[key]
            self.generate_curve_node(curve_object,lCurveObjectNode,
                                                        model_ID=model_ID,
                                                        color_plugin_object = color_plugin_object,
                                                        export_plugin_object = export_plugin_object)

    def generate_curve_node(self,curve_object,lCurveObjectNode,
                                                        model_ID,
                                                        color_plugin_object,
                                                        export_plugin_object):
        
        lDatasNode = FbxNode.Create(self.lSdkManager,"Data_") # one for each file
        if curve_object.df_metadata is not None:
            create_fbxPropertiesFrom_df_metadata(curve_object,lDatasNode)
        j=0
        for key,datapoint_object in curve_object.dict_datapoints.items():
            '''start: can be done elsewhere, earlier'''
            #in data import, and for depth and point_size, in style_object. 
            #halfwidths, color coeffs, etx require comlete set to determine'''
            #print("If this breaks here, it is because I am testing. Turn it back on to run. 12 February 2025")


            if True:
                # this carries the one live datapoint. This is dumb.
                datapoint_object.set_vars(time = curve_object.dict_data_vectors_scaled["time"][j],
                                            height = curve_object.dict_data_vectors_scaled["height"][j],
                                            depth = curve_object.dict_data_vectors_scaled["depth"][j],
                                            halfwidth_time = curve_object.dict_data_vectors_scaled["halfwidth_time"][j],
                                            halfwidth_height = curve_object.dict_data_vectors_scaled["halfwidth_height"][j],
                                            halfwidth_depth = curve_object.dict_data_vectors_scaled["halfwidth_depth"][j],
                                            point_size = self.style_object.point_size)

            datapoint_object.set_vars(j = j,
                                        header_time = curve_object.header_time,
                                        header_height = curve_object.header_height,
                                        header_depth = curve_object.header_depth)
                                            #""" Bool """
            #if datapoint_object.color_coeff is None: # not none at this point, set wrong already: 3:43 PM on 12 February 2024
            datapoint_object.set_vars(model_ID = model_ID,
                                        color_coeff = curve_object.dict_color_coeff[model_ID][j])
            # i changed this to hack my shit together, on 29 Feb.
            # this is terrible naming convention, because what the heck does color_coeff mean
            # also, model_ID is half outdated, half entirely necessary
            # a flying spaghetti monster i have build
            # it's dumb because it overwrites it

            if j<len(curve_object.time)-1:
                time_next = curve_object.dict_data_vectors_scaled["time"][j+1]
                height_next = curve_object.dict_data_vectors_scaled["height"][j+1]
                depth_next = curve_object.dict_data_vectors_scaled["depth"][j+1]
                color_coeff_next = curve_object.dict_color_coeff[model_ID][j+1]
            else: # you are at the last item, and should make a last line of zero length
                time_next = curve_object.dict_data_vectors_scaled["time"][j]
                height_next = curve_object.dict_data_vectors_scaled["height"][j]
                depth_next = curve_object.dict_data_vectors_scaled["depth"][j]
                color_coeff_next = curve_object.dict_color_coeff[model_ID][j]

            datapoint_object.set_vars(time_next = time_next,
                                    height_next = height_next,
                                    depth_next = depth_next,
                                    color_coeff_next = color_coeff_next)
            '''end: can be done elsewhere, earlier'''
            ###lGeometryNode = self.plotting_style_plugin_object.plugin(self,datapoint_object)  ## do not delete, only off for testing
            #print(f'datapoint_object:{datapoint_object}')

            #print("If this breaks here, it is because I am testing. Turn it back on to run. 12 February 2025")
            if True:
                self.scene_object.datapoint_object = datapoint_object # no this  sucks, because it changes every instance. like, it's fine for troubleshooting, to have the datapoint easily available. but that can be done using just the last iteration only.
            lGeometryNode = export_plugin_object.plugin(self,datapoint_object) # THE CALL
            lMaterial = color_plugin_object.FBX_material(datapoint_object,self.materials_object) # error here 

            lGeometryNode.AddMaterial(lMaterial)    
            lDatasNode.AddChild(lGeometryNode)
            j+=1
        lCurveObjectNode.AddChild(lDatasNode)

        return True
        

    def geometryNode(self,datapoint_object,key):
        # When is this called: in the given export plugin. Should be present in all useful export plugins.
        lGeometryNode = FbxNode.Create(self.lSdkManager,datapoint_object.nodeName_dict[key]) # one for each data point (minus one) in a file
        lGeometryMesh = FbxMesh.Create(self.lSdkManager, datapoint_object.nodeName_dict[key]) # one mesh per triangle
        n = len(datapoint_object.controlPoints_array_fbx4_dict[key])
        #print(f'n={n}')
        lGeometryMesh.InitControlPoints(n)

        if self.style_object.calculate_FBX_normal_and_material_layers:# extraneous
            lLayer,lNormalLayer,normalDirection_array_fbx4 = self._set_normal_layer(lGeometryMesh,datapoint_object.controlPoints_array_fbx4_dict[key])
            for ni in range(n):
                lGeometryMesh.SetControlPointAt(datapoint_object.controlPoints_array_fbx4_dict[key][ni],ni)
                lNormalLayer.GetDirectArray().Add(normalDirection_array_fbx4)
            lLayer = self._set_material_layer(lGeometryMesh,lLayer,lNormalLayer)
        else:
            for ni in range(n):
                lGeometryMesh.SetControlPointAt(datapoint_object.controlPoints_array_fbx4_dict[key][ni],ni)

        # Array of polygon vertices, how a collection of points and faces become a single object.
        lPolygonVertices = tuple(np.arange(0,n,1))
        lGeometryMesh.BeginPolygon(0) #https://docs.unity3d.com/Packages/com.autodesk.fbx@4.1/api/Autodesk.Fbx.FbxMesh.html
        for j in range(n):
            lGeometryMesh.AddPolygon(lPolygonVertices[j]) # Control point index.
        lGeometryMesh.EndPolygon()
        lGeometryNode.SetNodeAttribute(lGeometryMesh)
        # kFBXObjectMetaData
        # DisplayMetaData() and DisplayMetaDataConnections()
        # Pavlov_active.metadata_sandbox()
        ################ META DATA how-to, please do not delete yet
        """    FbxObjectMetaData* pFamilyMetaData = FbxObjectMetaData::Create(pScene, "Family");
        FbxProperty::Create(pFamilyMetaData, FbxStringDT, "Level", "Level").Set(FbxString("Family"));
        FbxProperty::Create(pFamilyMetaData, FbxStringDT, "Type", "Type").Set(FbxString("Wall"));
        FbxProperty::Create(pFamilyMetaData, FbxFloatDT, "Width", "Width").Set(10.0f);
        FbxProperty::Create(pFamilyMetaData, FbxDoubleDT, "Weight", "Weight").Set(25.0);
        FbxProperty::Create(pFamilyMetaData, FbxDoubleDT, "Cost", "Cost").Set(1.25);

        FbxObjectMetaData* pTypeMetaData = FbxCast<FbxObjectMetaData>(pFamilyMetaData->Clone(FbxObject::eReferenceClone, pScene));

        pTypeMetaData->SetName("Type");

        // On this level we'll just override two properties
        pTypeMetaData->FindProperty("Cost").Set(2500.0);
        pTypeMetaData->FindProperty("Level").Set(FbxString("Type"));

        FbxObjectMetaData* pInstanceMetaData = FbxCast<FbxObjectMetaData>(pTypeMetaData->Clone(FbxObject::eReferenceClone, pScene));

        pInstanceMetaData->SetName("Instance");

        // And on this level, we'll go in and add a brand new property, too.
        FbxProperty::Create(pInstanceMetaData, FbxStringDT, "Sku", "Sku#").Set(FbxString("143914-10"));
        pInstanceMetaData->FindProperty("Width").Set(1100.50f);
        pInstanceMetaData->FindProperty("Type").Set(FbxString("Super Heavy Duty Wall"));
        pInstanceMetaData->FindProperty("Level").Set(FbxString("Instance"));

        // Finally connect metadata information to some of our nodes.
        pNodeA->ConnectSrcObject(pInstanceMetaData);
        pNodeC->ConnectSrcObject(pInstanceMetaData);    // Share the same object

        pNodeD->ConnectSrcObject(pTypeMetaData);

        return true;
        """
        ''' # These commands are useful for troubleshooting. However, the relevant meshes live inside lGeometryNode.
        lGeometryMesh.GetPolygonVertexCount()
        lGeometryMesh.GetPolygonSize(0)
        lGeometryMesh.GetPolygonCount()
        '''
        datapoint_object.set_FBX_geometry(lGeometryNode,key=key)
        return lGeometryNode
    
    def _set_normal_layer(self,lGeometryMesh,controlPoints_array):#extraneous
        # When these are allowed to run, the export file gets 50% larger.
        # This adds 1Layer and 1MaterialLayer data to the export file. Unecessary.
        # No apparent improvement or feature addition when viewing in CAD Assistant.
        FbxLayerElement = self.conditional_import_object.FbxLayerElement
        FbxLayerElementNormal = self.conditional_import_object.FbxLayerElementNormal
        normalDirection_array = self._calculate_normal_direction(controlPoints_array) # one direction, in FbxVector4
        normalDirection_array_fbx4 = FbxVector4(normalDirection_array[0],normalDirection_array[1],normalDirection_array[2])
        lLayer = lGeometryMesh.GetLayer(0)
        if lLayer is None:
            lGeometryMesh.CreateLayer()
            lLayer = lGeometryMesh.GetLayer(0)
        lNormalLayer= FbxLayerElementNormal.Create(lGeometryMesh, "")
        lNormalLayer.SetMappingMode(FbxLayerElement.eByControlPoint)#.eByEdge,.eByPolygon,.eByControlPoint
        lNormalLayer.SetReferenceMode(FbxLayerElement.eDirect)#.eDirect
        return lLayer,lNormalLayer,normalDirection_array_fbx4

    def _set_material_layer(self,lGeometryMesh,lLayer,lNormalLayer):#extraneous
        FbxLayerElement = self.conditional_import_object.FbxLayerElement
        FbxLayerElementMaterial = self.conditional_import_object.FbxLayerElementMaterial
        lLayer.SetNormals(lNormalLayer)
        lMaterialLayer=FbxLayerElementMaterial.Create(lGeometryMesh, "")
        lMaterialLayer.SetMappingMode(FbxLayerElement.eByPolygon)#.eByEdge,.eByPolygon
        lMaterialLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)#.eByEdge,.eIndexToDirect
        lLayer.SetMaterials(lMaterialLayer)
        return lLayer

    def _calculate_normal_direction(self,controlPoints_array):
        controlPoints_array = np.array(controlPoints_array)
        P1 = controlPoints_array[0]
        P2 = controlPoints_array[1]
        P3 = controlPoints_array[2]
        #print ('controlPoints_array = ',controlPoints_array)
        u = P2-P1
        v = P3-P1
        #N = np.cross(u,v)
        N = np.cross(v,u) # this is blaspehmy, but my directions are all backwards and this is a bandaid fix 19/2/23
        N_mag = self._calculate_magnitude(N)
        normal = N/N_mag
        if __name__ == "__main__": 
            print("normal = \n",normal)
            print("\n")
        return normal
    
    def _calculate_magnitude(self,vector):
            # Source: https://www.geeksforgeeks.org/how-to-get-the-magnitude-of-a-vector-in-numpy/
            return math.sqrt(sum(pow(element, 2) for element in vector))
    
    def _store_model_ID(self,model_ID):#will change to multiple values within one object instance if self.style_object.createFBX_model_color has more than one value
        self.model_ID = model_ID
    
    def bundle_geometries(self,lGeometryNode_dict,nodeName_parent):
        lGeometryNode = FbxNode.Create(self.lSdkManager,nodeName_parent)
        for key,node in lGeometryNode_dict.items():
            lGeometryNode.AddChild(node)
        return lGeometryNode

class vector_placement:
    def __init__(self):
        self.name = 'vector_placement'

