'''
Author: Clayton Bennett
Created: 9 July 2023
Title: arrayMath

Purpose:
provide min and max functions for nested array with two levels

'''
import numpy as np
# from stackoverflow.com/questions/47327646/handling-none-when-adding-numbers
def max_arrayMath_(vectorArray):
    if not vectorArray:
        print("max: vectorArray is empty")
        return None
    maxValue = max(vectorArray[0])
    for vector_i in vectorArray:
        if not vector_i:
            continue
        if max(vector_i) > maxValue:
            maxValue = max(vector_i)
    return maxValue

def min_arrayMath_(vectorArray):
    if not vectorArray:
        print("min: vectorArray is empty")
        return None
    minValue = min(vectorArray[0])
    for vector_i in vectorArray:
        if not vector_i:
            continue
        if min(vector_i) < minValue:
            minValue = min(vector_i)
    return minValue

def max_arrayMath(vectorArray):
    """
    Return the maximum value across a two-level nested array (list of lists or list of numpy arrays).
    Returns None if the input is empty or only contains empty sublists.
    """
    try:
        # Flatten while guarding against empty sub-vectors
        flat_values = [val for vec in vectorArray if len(vec) > 0 for val in vec]
    except TypeError:
        raise ValueError("max_arrayMath expects a list of iterables")

    if not flat_values:
        return None  # nothing to compare

    return max(flat_values)


def min_arrayMath(vectorArray):
    """
    Return the minimum value across a two-level nested array (list of lists or list of numpy arrays).
    Returns None if the input is empty or only contains empty sublists.
    """
    try:
        flat_values = [val for vec in vectorArray if len(vec) > 0 for val in vec]
    except TypeError:
        raise ValueError("min_arrayMath expects a list of iterables")

    if not flat_values:
        return None

    return min(flat_values)

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

def rangeSelect_tier1(array,chokeRange):
    # if the submitted range does not include any data from a selected file, the file should be removed
    # range select needs to apply to all relevant vectors: if one is rejected, they all are rejected
    
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
    """Return the minimum y-value across all control point sets."""
    return max(max(points[:, 1]) for points in characters_control_points_list)

def determine_current_min_height(characters_control_points_list):
    """Return the minimum y-value across all control point sets."""
    return min(min(points[:, 1]) for points in characters_control_points_list)

def determine_current_max_time(characters_control_points_list):
    """Return the minimum time-value across all control point sets."""
    return max(max(points[:, 0]) for points in characters_control_points_list)

def determine_current_min_time(characters_control_points_list):
    """Return the minimum time-value across all control point sets."""
    return min(min(points[:, 0]) for points in characters_control_points_list)


if __name__ == "__main__":
    #test
    array = [[0,1,2,3,4],[-1,-2,-3,-4],[-7,9,3,-5],[3,-2,1,0]]
    maxHeight = max_arrayMath(array)
    minHeight = min_arrayMath(array)
    print('maxHeight =',maxHeight)
    print('minHeight =',minHeight)

    array = [[1,2,3],[4,5,6]]
    array_fbx4 = fbx4_convert(array)
    print(f"array_fbx4 = {array_fbx4}")
    
