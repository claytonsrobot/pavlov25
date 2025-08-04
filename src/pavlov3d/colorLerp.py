'''
Title: colorLerp.py
Author: Clayton Bennett
Created 05 June 2023

Purpose: Input a number between 0.0 and 1.0 to return an RGB output on a gradient, in form color = [R,G,B]

Lowest outcome, purple. Highest outcome, yellow.

Purple-Blue-Green-Yellow is canon (Matlab default and Blender default)

Blue stays the same, at 204, from puprple, to blue, to light blue. The blue value drops to 63 through to yellow.
Green is 63 from purple to dark blue, then grows linearly to 204 just after light blue, at the first hint of green. It stays 204 through to yellow.
Red starts at 204 at the very beginging of purple, then drops linearly to 63 in blue, until the first hint of green, then grows again to the end of yellow.

# currently broken, Red value is comig out low at  0.0 and 1.0 cc, should be high value. 22 June 2023.
# Fixed, working! Now convert to method. 22b June 2023.

'''
import numpy as np
from src.pavlov3d import arrayMath

# determine RGB values based on color_coeff

'''
def interp(X,maxX, minX,minY,maxY):
    slope = (maxY-minY)/(maxX-minX)
    ratio = (X-minX)/(maxX-minX)
    Y = (ratio * (maxY-minY))+minY
    return Y
'''

def interpRaise(X,minX, maxX,minY,maxY):
    slope = (maxY-minY)/(maxX-minX)
    ratio = (X-minX)/(maxX-minX)
    Y = (ratio * (maxY-minY))+minY
    return Y

def interpDrop(X,minX, maxX,minY,maxY):
    ratio = (X-minX)/(maxX-minX)
    Y = maxY - (ratio * (maxY-minY))
    return Y
'''
def linearDrop(cc,minRGB,maxRGB):
    byte256 = interpDrop(cc,0,1,minRGB,maxRGB)
    return byte256                                                                     

def linearRaise(cc,minRGB,maxRGB):
    byte256 = interpRaise(cc,0,1,minRGB,maxRGB)
    return byte256
'''
def colorLerp(color_coeff):
    maxRGB = 204 # out of 255
    minRGB = 63 # out of 255
    maxRGB = 255 # out of 255
    minRGB = 0 # out of 255
    cc = color_coeff
    if 0.0 <= cc and cc < 0.2:
        #R = linearDrop(cc,minRGB,maxRGB)
        R = interpDrop(cc,0,0.2,minRGB,maxRGB)
        G = minRGB
        B = maxRGB
    elif 0.2 <= cc and cc < 0.4:
        R = minRGB
        #G = linearRaise(cc,minRGB,maxRGB)
        G = interpRaise(cc,0.2,0.4,minRGB,maxRGB)
        B = maxRGB
    elif 0.4 <= cc and cc < 0.6:
        R = minRGB
        G = maxRGB
        #B = linearDrop(cc,minRGB,maxRGB)
        B = interpDrop(cc,0.4,0.6,minRGB,maxRGB)
    elif 0.6 <= cc and cc < 0.8:
        #R = linearRaise(cc,minRGB,maxRGB)
        R = interpRaise(cc,0.6,.8,minRGB,maxRGB)
        G = maxRGB
        B = minRGB
    elif 0.8 <= cc and cc <= 1.0:
        #R = linearRaise(cc,minRGB,maxRGB)
        R = maxRGB
        G = interpDrop(cc,0.8,1.0,minRGB,maxRGB)
        B = minRGB
    elif 1.0 < cc or 0.0 > cc:
        print("colorLerp requires a color_coefficient between 0.0 an 1.0.")
        print(f'color_coeff={color_coeff}')
    else:
        print(f'cc={cc}: colorLerp expects a color_coefficient between 0.0 an 1.0. ')
        print(f'color_coeff={color_coeff}')
    RGB = [R,G,B]
    return RGB

def colorLerp_coeff(color_coeff):
    RGB = colorLerp(color_coeff)
    RGB = np.divide(RGB,255)
    return RGB

def colorAssign(heightList):
    colorList = []
    color_coeff_list = []
    minHeight = min(heightList) # worth the speeed to calculate only once?
    maxHeight = max(heightList) # worth the speeed to calculate only once?
    for height in heightList:
        color_coeff = (height-minHeight)/(maxHeight-minHeight)
        color_coeff_list.append(color_coeff)
        colorList.append(colorLerp(color_coeff))
    colorList = np.divide(colorList,255)
    return colorList, color_coeff_list


def colorAssign_gradient_nested(vectorArray): # attempt to make function accept nested array of vectors, instead of just 1 vector
    #arrayMath.max_arrayMath # used for finding max value for nested array, to assign color values compared between different objects (from different vectors) 
    #arrayMath.min_arrayMath # to compare between objects
    max_value = arrayMath.max_arrayMath(vectorArray)
    min_value = arrayMath.min_arrayMath(vectorArray)
    i=0
    color_list = [[]]
    color_coeff_list = [[]]
    while i<len(vectorArray):
        j=0
        while j<len(vectorArray[i]):
            value = vectorArray[i][j]
            if np.isnan(value):
                value=0
            color_coeff = (value-min_value)/(max_value-min_value)
            color_coeff_list[i].append(color_coeff)
            try:
                color_value = np.divide(colorLerp(color_coeff),255)
            except:
                print(value, "FORCED: colorLerp.colorAssign_gradient_nested")
                color_value = 0
            color_list[i].append(color_value)
            j=j+1
        i=i+1
        if i<len(vectorArray):  # only do this if there is going to be another round (don't do it on the last round)
            color_list.append([])
            color_coeff_list.append([])

    return color_coeff_list,color_list

#color_coeff = (this_value-min_value)/(max_value-min_value)
'''
Test:   
color_coeff = 0.0
RGB = colorLerp(color_coeff)
print("RGB = ",RGB, "color_coeff = ",color_coeff)
color_coeff = 0.85
RGB = colorLerp(color_coeff)
print("RGB = ",RGB, "color_coeff = ",color_coeff)
color_coeff = 1.0
RGB = colorLerp(color_coeff)
print("RGB = ",RGB, "color_coeff = ",color_coeff)
'''

