'''
Title: pngMaker
Author: Clayton Bennett
Project: Pavlov 3D
Created: 27 August 2023

Purpose: Formatting etc for PNG flats
'''
#import time
if False:
    import matplotlib.pyplot as plt
        
# https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
def homogenousCheck(vector):
    homogenous = not vector or vector.count(vector[0]) == len(vector)
    return homogenous

def asterisk(boolean):
    if not boolean:
        asterisk_bool = "*"
    else:
        asterisk_bool = ""
    return asterisk_bool

def preview(scene_object,pngShow,pngExport,exportname='preview'):
    filename_overview_PNG = scene_object.filename_FBX.replace('.fbx','.png')
    if pngShow or pngExport: 
        #unix_mark = time.time()
        #mark_time = round(unix_mark-scene_object.unix_start,2)
        #print("Creating overview image ... mark",mark_time,"sec")
        homogenous_headers_time = homogenousCheck(scene_object.headers_time)
        homogenous_headers_height = homogenousCheck(scene_object.headers_height)

        asterisk_time = asterisk(homogenousCheck(scene_object.headers_time))
        asterisk_height = asterisk(homogenousCheck(scene_object.headers_height))

        xlabel = scene_object.headers_time[0] # assumes all headers are homogenous
        ylabel = scene_object.headers_height[0] # assumes all headers are homogenous

        plt.xlabel(xlabel+asterisk_time)
        plt.ylabel(ylabel+asterisk_height)
        plt.title("Pavlov Preview: "+str(len(scene_object.names))+" files")

        i=0
        while i<len(scene_object.vectorArray_height):
            plt.plot(scene_object.vectorArray_time[i],scene_object.vectorArray_height[i],label = scene_object.names[i])
            i=i+1
        #plt.legend(names, bbox_to_anchor = (0.28,0.71),ncol=3)
        if pngExport:
            plt.savefig(filename_overview_PNG)
            print("Export: ", filename_overview_PNG)

        if pngShow:
            plt.show(block=False)
            plt.pause(2)
            plt.close()
    return filename_overview_PNG

''' test
a = ['txt','txt','txt','txt','txt']
b = ['txt','txt','txt','txt','txt','v']
print(homogenousCheck(a))
print(homogenousCheck(b))
'''
