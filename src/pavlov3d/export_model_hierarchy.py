'''
Title: export_model_hierarchy.py
Author: Clayton Bennett
Created 28 June 2024
'''

class Hierarchy:
    scene_object = None
    createFBX_object = None

    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object = scene_object

    @classmethod
    def assign_scene_object(cls,createFBX_object):
        cls.createFBX_object = createFBX_object

    def assign_to_top_level(self,instance):
        True

    def assign_to_parent(self,instance,parent):
        True










