'''
Author: Clayton Bennett
Created: 9 July 2023
Title: arrayMath

Purpose:
provide min and max functions for nested array with two levels


'''
import numpy as np
# from stackoverflow.com/questions/47327646/handling-none-when-adding-numbers
def None_sum(array1,array2):
    length = len(array1) 
    if len(array1)==len(array2):
        if any([i==None for i in array1]) or any([i==None for i in array2]):
            output=[None]*length
        else:
            output = np.array(array1)+np.array(array2)
    else:
        output=np.array([])
    return output

def None_product(array1,array2):
    length = len(array1) 
    if len(array1)==len(array2):
        if any([i==None for i in array1]) or any([i==None for i in array2]):
            output=[None]*length
        else:
            output = np.multiply(array1,array2)
    else:
        output=np.array([]) # is this best? we want this to never happen
        #output = None
    return output

def None_scalar(scalar,array1):
    length = len(array1) 
    if any([i==None for i in array1]):
        output=[None]*length
    else:
        output = np.multiply(scalar,array1)

    return output

def max_arrayMath(vectorArray):
    try:
        maxValue = max(vectorArray[0]) # check first vector
        for i,vector_i in enumerate(vectorArray): # 2 level nested array
            #print(f"vectorArray, i = {i}")
            if maxValue<max(vector_i):
                maxValue = max(vector_i)
    except Exception:
        try:
            maxValue = max(vector_i)
        except:
            maxValue = None
            print("max:　An included vector did not exists")
    return maxValue

def min_arrayMath(vectorArray):
    try:
        minValue = min(vectorArray[0]) # check first vector
        for i,vector_i in enumerate(vectorArray): # 2 level nested array
            if minValue>min(vector_i):
                minValue = min(vector_i)
    except Exception:
        minValue = min(vectorArray)
        print("min:　An included vector did not exists")
    return minValue

def fill_arrayMath(vectorArray,vectorArray_B): # example of general form
    i=0
    #j=0
    halfwidthtime_list = [[]]
    halfdepth_list = [[]]
    #coefficient_deltaTime = 0.8 # this must be able to be controlled by the program, therefore cannot be abstracted away
    coefficient_deltaTime = 1
    width_coefficient_perBar = 20
    width_coefficient_byMaxTime = 0.2
    while i<len(vectorArray_time):
        j=0
        halfwidthtime_min = halfdelta(vectorArray_time[i]) # find minimum difference between all points in a vector
        while j<len(vectorArray_time[i]):
            halfwidthtime_list[i].append(coefficient_deltaTime*halfwidthtime_min)
            if styleChoice_width00 == 'perBar':
                halfdepth_list[i].append(width_coefficient_perBar*coefficient_deltaTime*halfwidthtime_min)
            if styleChoice_width00 == 'byMaxTime':
                halfdepth_list[i].append(width_coefficient_byMaxTime*maxTime)
            if styleChoice_width00 == 'square_depthEqualHeight':
                halfdepth_list[i].append(vectorArray_height[i][j]/2)
            j=j+1
        i=i+1
        if i<len(vectorArray_time): # only do this if there is going to be another round (don't do it on the last round)
            halfwidthtime_list.append([])
            halfdepth_list.append([])

def fbx4_convert(array):
    # the purpose of this is to function for inputs of length 3 or 4...but come on, when does that happen.
    # why would it be a four to start with?
    # this function might not be merited.
    # import FbxCommon
    from fbx import FbxVector4
    array_fbx4 = []
    for vector in array:
        #print("vector = ",vector)
        #print("type(vector) = ",type(vector))
        try:
            length = len(vector)
        except:
            length = vector.size
        if length==4:
            vector_fbx4 = FbxVector4(vector[0],vector[1],vector[2],vector[3])
        elif length==3:
            vector_fbx4 = FbxVector4(vector[0],vector[1],vector[2])
        array_fbx4.append(vector_fbx4)
    
    return array_fbx4


'''
def rangeSelect(array,chokeRange):
    # if the submitted range does not include any data from a selected file, the file should be removed
    # range select needs to apply to all relevant vectors: if one is rejected, they all are rejected
    #array_new = rangeSelect(array,chokeRange)
    # a bit of a time waster
    [iA,iB,jA,jB] = chokeRange
    i=iA
    n=0
    array_choked = []
    keep_idx_choked = []
    i_empty = []
    if iB == -1 or iB is None:
        iB = len(array)
    while i<len(array):
        if jB == -1 or jB is None:
            jB = len(array[i])
        #if jA >= min(array[i]) or jB <= max(array[i]): # NO, this looks at values, not just second tier indices
        vector_i_choked = array[i][jA:jB]
        if not(0==len(vector_i_choked)):
            array_choked.append(vector_i_choked)
            #print("max(vector_i_choked) = ",max(vector_i_choked))
        else:
            
            i_empty.append(i)
            
        keep_idx_choked.append(i)
        i=i+1

    return array_choked, i_empty #,keep_idx_chocked
'''
def rangeSelect_tier1(array,chokeRange):
    # if the submitted range does not include any data from a selected file, the file should be removed
    # range select needs to apply to all relevant vectors: if one is rejected, they all are rejected
    #array_new = rangeSelect(array,chokeRange)
    # a bit of a time waster
    [iA,iB] = chokeRange
    array_choked = []
    keep_idx_choked = []
    i_empty = []
    if iB == -1 or iB is None:
        iB = len(array)
    i=iA
    while i<iB:
        vector_i_choked = array[i]
        if not(0==len(vector_i_choked)):
            array_choked.append(vector_i_choked)
            keep_idx_choked.append(i)
        else:
            i_empty.append(i)
        i=i+1

    return array_choked,i_empty

def rangeSelect_tier2(array,chokeRange):
    # if the submitted range does not include any data from a selected file, the file should be removed
    # range select needs to apply to all relevant vectors: if one is rejected, they all are rejected
    #array_new = rangeSelect(array,chokeRange)
    # a bit of a time waster
    [jA,jB] = chokeRange
    array_choked = []
    keep_idx_choked = []
    i_empty = []
    i=0
    while i<len(array):
        vector_i_choked = array[i]
        if jB == -1 or jB is None:
            jB = len(vector_i_choked)
        vector_i_choked = vector_i_choked[jA:jB]
        if not(0==len(vector_i_choked)):
            array_choked.append(vector_i_choked)
            keep_idx_choked.append(i)
        else:
            i_empty.append(i)
        i=i+1

    return array_choked,i_empty

def count_datapoints(array):
    tally = 0
    for vector_i in array:
        tally=tally+len(vector_i)
    return tally

def count_instances(vectorArray,value):
    tally = 0
    for vector_i in vectorArray:
        tally = tally + vector_i.count(value)
    return tally

def determine_current_max_height(characters_control_points_list):
    # assume postive heights, everything is initally over the time axis
    current_max_height = 0
    for character_controlPoints in characters_control_points_list:
        current_max_height_i = max(character_controlPoints[:,1])
        if current_max_height_i > current_max_height:
            current_max_height = current_max_height_i
    return current_max_height

def determine_current_min_height(characters_control_points_list):
    # assume postive heights, everything is initally over the time axis
    current_min_height = min(characters_control_points_list[0][:,1]) # use first entry to initialize
    for character_controlPoints in characters_control_points_list:
        current_min_height_i = min(character_controlPoints[:,1])
        if current_min_height_i > current_min_height:
            current_min_height = current_min_height_i
    return current_min_height

def determine_current_max_time(characters_control_points_list):
    current_max_time = 0
    for character_controlPoints in characters_control_points_list:
        current_max_time_i = max(character_controlPoints[:,0])
        if current_max_time_i > current_max_time:
            current_max_time = current_max_time_i
    return current_max_time

'''
def rangeCull(vector, keep_idx):
    i=0
    vector_culled = []
    while i<len(keep_idx):
        vector_culled.append(vector[keep_idx[i]])
        print(vector_culled)
        i=i+1
    return vector_culled
'''
'''
def rangeShare(vector,i_empty):
    k=0
    vector_culled = vector
    while k<len(i_empty):
        vector_culled = vector_culled.pop(i_empty[k])
        print(vector_culled)
        k=k+1
    return vector_culled
'''
'''
#test
array = [[0,1,2,3,4],[-1,-2,-3,-4],[-7,9,3,-5],[3,-2,1,0]]
maxHeight = max_arrayMath(array)
minHeight = min_arrayMath(array)
print('maxHeight =',maxHeight)
print('minHeight =',minHeight)

'''
'''
array = [[1,2,3],[4,5,6]]
array_fbx4 = fbx4_convert(array)
'''

''''
iA=0
iB=1
jA = 0
jB = 1
chokeRange = [iA,iB,jA,jB]
array = [[1,2,3,4,5,6],[4,5,6,7,8,9],[0,1,2,3]]
array_new = rangeSelect(array,chokeRange)
print("array_new = ",array_new)
'''
'''
idx = [0,4,6]
a = [0,1,2,3,4,5,6,7,8,9]
a_new = rangeCull(a,idx)
'''
