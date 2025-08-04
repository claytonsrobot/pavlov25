'''
Title:  materials.py, formerly materialBins.py
Author: Clayton Bennett
Created 21 June 2023

Purpose:
The original idea had been to reduce the filesize of output FBX files by reducing the number of materials.
This didn't work.
But, the visual effect is nice.

The goal today is to clean up yesterday's implementation.
'''
import numpy as np

#import FbxCommon
from fbx import FbxDouble3
from fbx import FbxSurfacePhong

from src.pavlov3d.colorLerp import colorLerp
class materials:
    def __init__(self):
        self.names = 'materials_object'
        self.lSdkManager = None
        self.lMaterials9_list = None
        self.lMaterials9_black = None
        self.predefined_color_coeff_list = [0.0,0.111111, 0.22222222, 0.33333333, 0.44444444,0.66666667, 0.77777778, 0.88888889, 1.0]
        self.idx = [0.0,0.111111, 0.22222222, 0.33333333, 0.44444444, 0.55555556, 0.66666667, 0.77777778, 0.88888889, 1.0]    
    
    def assign_lSdkManager(self,lSdkManager):
        self.lSdkManager = lSdkManager
        self.color_roulette = 0 
        self.dict_datapoint_keys = dict() # ugly, but effective.

        self.lMaterial_black = self.create_material_black(lSdkManager)
        self.lMaterials9_list = self.create_materials_9bins_FBX(lSdkManager)

    def colorRanges(self,color_coeff):
        # Used by the materials9_FBX method to create 9 stock materials
        # Not in final form. Combine this with the materials_FBX method, into one method.
        #The color values should be inherant to the material.
        
        if self.idx[0] <= color_coeff  and color_coeff < self.idx[1]:
            c=0
        elif self.idx[1] <= color_coeff  and color_coeff < self.idx[2]:
            c=1
        elif self.idx[2] <= color_coeff  and color_coeff < self.idx[3]:
            c=2
        elif self.idx[3] <= color_coeff  and color_coeff < self.idx[4]:
            c=3
        elif self.idx[4] <= color_coeff  and color_coeff < self.idx[5]:
            c=4
        elif self.idx[5] <= color_coeff  and color_coeff < self.idx[6]:
            c=5
        elif self.idx[6] <= color_coeff  and color_coeff < self.idx[7]:
            c=6
        elif self.idx[7] <= color_coeff  and color_coeff < self.idx[8]:
            c=7
        elif self.idx[8] <= color_coeff  and color_coeff <= self.idx[9]:
            c=8
        else:
            print("color_coeff is not between 0.0 and 1.0")
            if color_coeff < 0:
                print("color_coeff is less than 0. Treat it like it is 0.")
                c=0
            if 1 < color_coeff:
                print("color_coeff is greater than 1. Treat it like it is 1.")
                c=8
        color_coeff_output = self.predefined_color_coeff_list[c]
        return color_coeff_output

    def create_materials_9bins_FBX(self,lSdkManager):
        material_names = ['mat0_pink',\
                        'mat1_purple',\
                        'mat2_blue',\
                        'mat3_lightblue',\
                        'mat4_bluegreen',\
                        'mat5_green',\
                        'mat6_yelllow',\
                        'mat7_orange',\
                        'mat8_red']
        lMaterials9_list = []
        i=0
        while i<len(material_names):
            color_coeff = self.colorRanges(self.predefined_color_coeff_list[i])
            RGB = colorLerp(color_coeff)
            RGB = np.divide(RGB,255)
            color = FbxDouble3(RGB[0],RGB[1],RGB[2])
            lMaterial = FbxSurfacePhong.Create(lSdkManager,material_names[i]) 
            lMaterial.Diffuse.Set(color)
            lMaterials9_list.append(lMaterial)
            i=i+1
        return lMaterials9_list

    def create_material_free_FBX(self,color_coeff):
        # can use height as color coefficient? uhhhh how was this done before.
        # the problem is that we wrote unstable code on top of unstable code assuming that the under layer was ok even though it's not okay

        RGB = colorLerp(color_coeff)
        RGB = np.divide(RGB,255)
        color = FbxDouble3(RGB[0],RGB[1],RGB[2])
        material_name = str(color_coeff)
        lMaterial = FbxSurfacePhong.Create(self.lSdkManager,material_name) 
        lMaterial.Diffuse.Set(color)

        return lMaterial

    def assign_materials9_FBX(self,color_coeff):
        c = self.assign_c9_index_from_raw_color_coefficient(color_coeff)
        lMaterial = self.lMaterials9_list[c]
        return lMaterial

    def assign_c9_index_from_raw_color_coefficient(self,color_coeff):
        # Used by the materials9_FBX method to create 9 stock materials
        # Not in final form. Combine this with the materials_FBX method, into one method.
        #The color values should be inherant to the material.
        #self.predefined_color_coeff_list = [0.0,0.1, 0.22222222, 0.33333333, 0.44444444,0.66666667, 0.77777778, 0.88888889, 1.0]
        if self.idx[0] <= color_coeff  and color_coeff < self.idx[1]:
            c=0
        elif self.idx[1] <= color_coeff  and color_coeff < self.idx[2]:
            c=1
        elif self.idx[2] <= color_coeff  and color_coeff < self.idx[3]:
            c=2
        elif self.idx[3] <= color_coeff  and color_coeff < self.idx[4]:
            c=3
        elif self.idx[4] <= color_coeff  and color_coeff < self.idx[5]:
            c=4
        elif self.idx[5] <= color_coeff  and color_coeff < self.idx[6]:
            c=5
        elif self.idx[6] <= color_coeff  and color_coeff < self.idx[7]:
            c=6
        elif self.idx[7] <= color_coeff  and color_coeff < self.idx[8]:
            c=7
        elif self.idx[8] <= color_coeff  and color_coeff <= self.idx[9]:
            c=8
        else:
            print("color_coeff is not between 0.0 and 1.0")
            if color_coeff < 0:
                print("color_coeff is less than 0. Treat it like it is 0.") 
                c=0
            elif 1 < color_coeff:
                print("color_coeff is greater than 1. Treat it like it is 1.")
                c=8
            else:
                c=0 # problem in data import
        #color_coeff_output = self.predefined_color_coeff_list[c]
        #lMaterial = lMaterials9_list[c]
        return c    
        
    def create_material_black(self,lSdkManager):
        #RGB = [0,0,0] # black
        #color = FbxDouble3(RGB[0],RGB[1],RGB[2])
        black = FbxDouble3(0,0,0)
        color = black
        lMaterial_black = FbxSurfacePhong.Create(lSdkManager,"black")
        lMaterial_black.Diffuse.Set(color)
        
        return lMaterial_black

    def create_material_green_contrast_text(self,lSdkManager):
        RGB = [12, 66, 40] # green
        #hsl(153, 51.20%, 16.90%)
        #rgb(12, 66, 40)
        color = FbxDouble3(RGB[0],RGB[1],RGB[2])
        lMaterial_green_contrast_text = FbxSurfacePhong.Create(lSdkManager,"green_contrast_text")
        lMaterial_green_contrast_text.Diffuse.Set(color)
        
        return lMaterial_green_contrast_text

    def create_material_blue_contrast_text(self,lSdkManager):
        #RGB = [12, 66, 40] # green
        RGB = [60, 79, 189] # blue
        color = FbxDouble3(RGB[0],RGB[1],RGB[2])
        lMaterial_blue_contrast_text = FbxSurfacePhong.Create(lSdkManager,"green_contrast_text")
        lMaterial_blue_contrast_text.Diffuse.Set(color)
        return lMaterial_blue_contrast_text

    def create_material_custom_RGB(self,lSdkManager,RGB):
        #RGB = [12, 66, 40] # green
        color = FbxDouble3(RGB[0],RGB[1],RGB[2])
        lMaterial_custom_RGB = FbxSurfacePhong.Create(lSdkManager,"custom_RGB")
        lMaterial_custom_RGB.Diffuse.Set(color)
        return lMaterial_custom_RGB

