'''
Title: deltaList
Author: Clayton Bennet
Created: 27 March 2023
Purpose: Output a list of the distance between each consecutive item in a numeric list.
This is acccomplished by subtracting each item from the previous item.
The delta list will be one element smaller than the original vector
'''
import numpy as np

def deltaList(vector):
    deltaList_out = []
    i=1
    # for i,x in enumerate(vector):
    while i<len(vector):
        delta = vector[i]-vector[i-1]
        if not(delta==0.0):
            deltaList_out.append(delta)    
        i=i+1
    return deltaList_out

def halfdelta_min_finder(vector):
    if not(len(vector)>1):
        halfdelta_min = None
    else:
        halfdelta_min = None
        deltaList_out = deltaList(vector)
        for delta in deltaList_out:
            halfdelta = abs(delta/2)
            if halfdelta == 0:
                continue
            elif halfdelta_min is None:
                halfdelta_min = halfdelta
            elif halfdelta < halfdelta_min:
                halfdelta_min = halfdelta
            #min(deltaList_out)/2 # need to be able to use for abs
    return halfdelta_min

def halfdelta_min_reasonable_finder(vector):
    halfdelta_min = halfdelta_min_finder(vector)
    halfdelta_min_reasonable = 0.01*(max(vector)-min(vector)) # get 1% of spread 
    if halfdelta_min_reasonable > halfdelta_min:
        return halfdelta_min_reasonable
    else:
        return halfdelta_min


def halfdelta_max_finder(vector):
    if not(len(vector)>1):
        halfdelta_max = None
    else:
        halfdelta_max = None
        deltaList_out = deltaList(vector)
        for delta in deltaList_out:
            halfdelta = abs(delta/2)
            if halfdelta == 0:
                continue
            elif halfdelta_max is None:
                halfdelta_max = halfdelta
            elif halfdelta > halfdelta_max:
                halfdelta_max = halfdelta
            #min(deltaList_out)/2 # need to be able to use for abs
    return halfdelta_max

def halfdelta_avg_finder(vector):
    # finds average halfdelta, excluding delta of zero
    halfdelta_max = halfdelta_max_finder(vector)
    halfdelta_min = halfdelta_min_finder(vector)
    return (halfdelta_min+halfdelta_max)/2


def halfdeltaList(vector):
    if not(len(vector)>1):
        halfdelta_min = None
    else:
        deltaList_out = deltaList(vector)
        halfdeltaList = np.multiply(0.5,deltaList_out)
    return halfdeltaList

if __name__ == "__main__":
    vector = [0,1,2,3,4,6,7,7.800]
    dL = deltaList(vector)
    print(dL)
    hdm = halfdelta_min_finder(vector)
    print(hdm)
    hdList = halfdeltaList(vector)
    print(hdList)
