"""
Title: pavlovian_object.py
Author: Clayton Bennett
Created 10 April 2025

Purpose: Be the super class with shared attributes for group objects, entity objects, mesh objects, scene object, and curve objects.
"""
import numpy as np

class PavlovianObject:

    def __init__(self):
        ""
        self.name = "pavlovian object"
        
        self.parent = object()
        self.children = dict()
        
        self.group_object = object()
        self.child_set = set()
        
        self.active = bool()
        
        self.fence = dict()
        self.scale = np.array([None,None,None])
        self.spin = np.array([0*np.pi,0*np.pi,0*np.pi])

    def set_parent(self,parent):
        self.parent=parent
        "make backwards compatible with pavlov25"
        self.group_object = parent
    def add_child(self,child):
        self.child_set = self.child_object.add(child)
        self.children = self.children.update({child.key:child})
        

if __name__ == "__main__":
    pavlovian_object = PavlovianObject()
    print(f"self.spin = {pavlovian_object.spin}")
    print(f"parent = {pavlovian_object.parent}")
    print(f"pavlovian_object.__doc__ = {pavlovian_object.__doc__}")
    print(f"dir(pavlovian_object) = {dir(pavlovian_object)}")
    print("types:")
    for key,value in pavlovian_object.__dict__.items():    
        print(f"\ttype({key}): {type(value)}")