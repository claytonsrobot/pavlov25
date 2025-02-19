'''
Author: Clayton Bennett
Title: lines_FBX.py (was axes_FBX.py)
Created: 22 September 2023
Purpose: Unpack lines_arrays and show triangles to represent axes and ticks for each object. 

Default color of all lines: black.

18 October 2023:
Add controlPoints_line_polygon module, feed in lLineMesh, generate control points and polygon, add to Mesh, then return the baptized lLineMesh
I want to add multiuple meshes to the same node. Where is the best place to do this without making a mess.


Ticks used to be done like this:
Axes
    Axis(header_time[i])
        Axis Mesh
        Tick [0] node
            Tick mesh, H
            Tick mesh, D
        Tick [1] node
            Tick mesh, H
            Tick mesh, D
        Tick [2] node
            Tick mesh, H
            Tick mesh, D
    Axis(header_height[i])
        Axis Mesh
        Tick [0] node
            Tick mesh, T
            Tick mesh, D
        Tick [1] node
            Tick mesh, T
            Tick mesh, D
        Tick [2] node
            Tick mesh, T
            Tick mesh, D
    Axis(header_depth[i])
        Axis Mesh
        Tick [0] node
            Tick mesh, H
            Tick mesh, T
        Tick [1] node
            Tick mesh, H
            Tick mesh, T
        Tick [2] node
            Tick mesh, H
            Tick mesh, T
This is outdated now, because rather than two meshes (horizontal and vertical) wiithi each node, there is now one complex mesh.

Can I intermix meshes and nodes as children of a node? In the same way that folders can contain both files and subfolders.
No.
Between the file conversion from FBX to GLB, single-mesh nodes are dropped, to result in multiple meshes per node in the GLB.

Artifact comments:
    Make it perfect, make it right.
    Plus, what we learn here will be applied to letters.
    Frankly, that's why we're doing it, to prepare for mesh components of a letter being a part of a phrase node.
    How can I chunk up the problem, yet know that it won't be a patchwork of messy spaghetti code?
    Answer: Use my own OOP to feed into the SDK node tree, and my OOP can have more detail!
    Can a SDK mesh have more than one triangle within the mesh? (No.)
    I'm sorry my friend - All meshes/polygons must be tangential, i.e., control points must be shared.
    Point being, you cannot have two (or more) isolated meshes that belong to the same node.

Remnants:
    #FbxMesh.AddPolygon 
    #FbxMesh.GetPolygonGroup

7 January 2024:
Destroy outdated comments, destroy outdated code.
Previously, there was an effort to allow existing meshes to be revisted and added to, but this is A) Not possible or B) Not worth it, or at the very least C) Not necessary.
'''
import numpy as np

from fbx import FbxVector4
from fbx import FbxNode # yes
from fbx import FbxMesh

from materials import materials

class LinesFBX:
    scene_object = None
    style_object = None
    lSdkManager=None
    materials_object=None
    @classmethod
    def asign_scene_object(cls,scene_object):
        cls.scene_object = scene_object
        cls.style_object = scene_object.style_object
        
    @classmethod
    def assign_FBX_SdkManager(cls,lSdkManager):
        cls.lSdkManager = lSdkManager
        cls.materials_object=materials()
        cls.materials_object.assign_lSdkManager(lSdkManager)

    def __init__(self):
        self.name = 'lines_FBX_' # text
        #self.show = True
        #self.assign_class_variables(scene_object)
    
    def __str__(self):
        return "Line object creation." 

    def __doc__(self):
        return "May the lord bless you and keep you in this wireframe paradigm."

    def __name__(self):
        return "Develop - what does this do?"

    def scale():
        return #"Develop - to alter scale after the axis has already been created.

    def linesNode(self,lines_array,nodeName,translation_vector = [0,0,0]):

        nodeName_lines = nodeName
        lLinesNode = FbxNode.Create(self.lSdkManager,nodeName_lines) # one for each file
        editNode = lLinesNode
        if lines_array is not None:
            for line_array in lines_array:
                name = line_array[0]
                data = line_array[1]

                if name is not None and data is not None:
                    # both name and data exist
                    lLineNode = self.lineNode(name,data,translation_vector)
                    editNode.AddChild(lLineNode) 
                elif name is not None and data is None:
                    # only name exists, it is the name of a parent
                    lSuperNode = FbxNode.Create(self.lSdkManager,name)
                    editNode.AddChild(lSuperNode)
                    editNode = lSuperNode # step in a tree hierarchy level
                elif name is None and data is not None:
                    # only data exists, it is a nameless child
                    lLineNode = self.lineMesh(self.lSdkManager,data,translation_vector) # makes a whole node with a nested mesh, to add as child to the current node
                    editNode.AddChild(lLineNode)  
                elif name is None and data is None:
                    # neither name nor data exists, step up a level
                    editNode = FbxNode.GetParent(editNode) # step out a tree hierarchy level
        return lLinesNode

    def lineNode(self,name,data,translation_vector):# consider using a default value of translation_vector=[0,0,0] if lineNode is ever to be run other than being called by linesNode.
        lLineNode = FbxNode.Create(self.lSdkManager,name) # one for each data point (minus one) in a file
        lLineMesh = FbxMesh.Create(self.lSdkManager, name) # one mesh per triangle
        lLineMesh = self.controlPoints_line_polygon(data,lLineMesh,translation_vector)
        lLineNode.SetNodeAttribute(lLineMesh)
        lMaterial_black = self.materials_object.lMaterial_black
        lMaterial_green_contrast_text = self.materials_object.create_material_green_contrast_text(self.lSdkManager)
        lMaterial_blue_contrast_text = self.materials_object.create_material_blue_contrast_text(self.lSdkManager)
        # these colors are non-accurate
        RGB=[166, 66, 0]# burnt orange rgb(113, 56, 0)
        RGB = [113, 56, 0] # darker
        RGB = [78, 39, 0] # darker
        lMaterial_custom_RGB = self.materials_object.create_material_custom_RGB(self.lSdkManager,RGB)

        if self.style_object.text_color == 'black':
            lMaterial_0 = lMaterial_black
        elif self.style_object.text_color == 'green_contrast_text':
            lMaterial_0 = lMaterial_green_contrast_text
        elif self.style_object.text_color == 'blue_contrast_text':
            lMaterial_0 = lMaterial_blue_contrast_text
        elif self.style_object.text_color == 'custom_RGB':
            lMaterial_0 = lMaterial_custom_RGB

        lLineNode.AddMaterial(lMaterial_0)
        return lLineNode

    def lineMesh(self,data,translation_vector):
        lLineNode = FbxNode.Create(self.lSdkManager,"pavlovLine")
        lLineMesh = FbxMesh.Create(self.lSdkManager, "pavlovLine") # one mesh per triangle
        lLineMesh = self.controlPoints_line_polygon(data,lLineMesh,translation_vector)
        lLineNode.SetNodeAttribute(lLineMesh)
        lMaterial_black = materials.create_material_black(self.lSdkManager)
        lLineNode.AddMaterial(lMaterial_black)
        return lLineNode

    def controlPoints_line_polygon(self,data,lLineMesh,translation_vector):
        # each coords vector should have two values, name and data
        # example: line_array = ['Axis, Time',[[0,1],[2,3],[4,5]]] # except for the first bit
        time_coords,height_coords,depth_coords = data[:,0],data[:,1],data[:,2]

        controlPoints_array_fbx4 = []
        for n in range(len(data)):
            lControlPoint_n = [float(time_coords[n]+translation_vector[0]),
                            float(height_coords[n]+translation_vector[1]),
                            float(depth_coords[n]+translation_vector[2])]
            lControlPoint_n_fbx4 = FbxVector4(lControlPoint_n[0],lControlPoint_n[1],lControlPoint_n[2])
            controlPoints_array_fbx4.append(lControlPoint_n_fbx4)
        n = len(controlPoints_array_fbx4)

        lLineMesh.InitControlPoints(n)
        for ni in range(n):
            lLineMesh.SetControlPointAt(controlPoints_array_fbx4[ni],ni)

        # Array of polygon vertices, how a collection of points and faces become a single object.
        lPolygonVertices = tuple(np.arange(0,n,1))
        lLineMesh.BeginPolygon(0) # Material index. BeginPolygon(int pMaterial,int pTexture,int pGroup,bool pLegacy)
        #https://docs.unity3d.com/Packages/com.autodesk.fbx@4.1/api/Autodesk.Fbx.FbxMesh.html
        for j in range(n):
            lLineMesh.AddPolygon(lPolygonVertices[j]) # Control point index.
        lLineMesh.EndPolygon() 
        
        return lLineMesh
