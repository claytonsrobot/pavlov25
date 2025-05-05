"""
Title: entity.py
Author: Clayton Bennett
Create: 10 April 2025

Entity objets and mesh objects should be added to the Pavlovian lexicon.
"""
import numpy as np
from src.pavlovian_object import PavlovianObject

class Entity(PavlovianObject):
    """
    Instead of 'curve', we should use the same 'entity'. Because, and entity can be a colletion of meshes, or really any discernible singular item.  
    """
    scene_object = None
    hierarchy_object = None

    def __init__(self):
        "Entity phone home."
        super().__init__()
        self.name = "entity object"
        self.entity_type = str()
        self.fence = dict()
        self.scale = np.array([None,None,None])
        self.spin = np.array([0*np.pi,0*np.pi,0*np.pi])

    def set_parent(self,parent):
        self.parent=parent
        "make backwards compatible with pavlov25"
        self.group_object = parent
    #def add_child(self,child):
        # same as super

if __name__ == "__main__":
    entity = Entity()
    print(f"self.spin = {entity.spin}")
    print(f"parent = {entity.parent}")
    print(f"entity.__doc__ = {entity.__doc__}")
    print(f"dir(entity) = {dir(entity)}")
    print("types:")
    for key,value in entity.__dict__.items():    
        print(f"\ttype({key}): {type(value)}")