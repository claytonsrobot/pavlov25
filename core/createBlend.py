"""
Title: createBlend.py
Created: 22 October 2024
Author: Clayton Bennett
"""

import bpy

# Define the vertices, edges, and faces of your mesh
vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)]
edges = []  # Leave empty to infer from faces
faces = [(0, 1, 3, 2)]

# Create a new mesh
mesh = bpy.data.meshes.new(name="MyMesh")

# Populate the mesh with data
mesh.from_pydata(vertices, edges, faces)

# Update the mesh to recalculate normals and other data
mesh.update()

# Create an object and link it to the scene
obj = bpy.data.objects.new("MyObject", mesh)
bpy.context.collection.objects.link(obj)

