"""
Title: mesh.py
Author: Clayton Bennett
Create: 10 April 2025

Entity objets and mesh objects should be added to the Pavlovian lexicon.
"""
import numpy as np
from src.pavlovian_object import PavlovianObject


class Mesh(PavlovianObject):

    """
    Instead of flocks and meshes, we have groups which hold entities which can be build of meshes (and maybe other things, like datapoints).
    """
    def __init__(self):
        "Get meshed."
        super().__init__()
        self.name = "entity object"
        self.mesh_type = str()
        self.entity = object()
        
        self.vertices = dict()
        self.normal = np.array([None,None,None])
        self.spin = 0*np.pi

    def set_parent(self,parent):
        self.parent=parent
        "make backwards compatible with pavlov25"
        self.entity_object = parent
        try:
            self.group_object = parent.parent
        except:
            pass


if __name__ == "__main__":
    mesh = Mesh()
    print(f"self.spin = {mesh.spin}")
    print(f"parent = {mesh.parent}")
    print(f"mesh.__doc__ = {mesh.__doc__}")
    print(f"dir(mesh) = {dir(mesh)}")
    print("types:")
    for key,value in mesh.__dict__.items():    
        print(f"\ttype({key}): {type(value)}")