'''
Author: Clayton Bennett
Created: 02 December 2023
Title: groupLines.py

Purpose: Create lines_array for group fencing and labeling
Modules: groupFence groupLabel
Inputs: dict_group_objects_tier2[group]

For a fences, place a square at the corners of the span. Five control points, to complete one square, easy.
Add second and third fences, for three sides total, for a fence visible in each plane.


04 December, bug:
For groups with only one object, the groupFence is never expanding and/or changing origin.
For the first group, at the origin, the groupFence doesn't include the labels or title.

Alter fences to be a collection of individual line meshes, as opposed to one node.
But does this matter after conversion to GLB?

Artifact:
     # this is how it was done in the old days, to create line arrays that can be fed to linesFBX in createFBX
    THD_direction = [1,0,0] # time
    ticks_array = []
    supergroup = ["Ticks: "+header, None]
    ticks_array.append(supergroup)
    for value_n in values:
        tick_coords = ticks_controlPoints(value_n,halflength_tick, THD_direction)
        tick_array = [str(round(value_n,2))+" "+header] # text label
        tick_array.append(tick_coords)
        ticks_array.append(tick_array)
        ticks_array.append([None,None])

07 January 2024:
    Make fences "see-through" by making each individual line a single mesh for a node that is a child of that fence-face.
    This means fences will not appear in shaded material appearances, or any appearance other than wireframe.
    Previously, fences were square meshes (two triangular meshes) that would obfuscate other model elements.
    Clicking on a model element with a fence in the way was impossible.
    This has been solved now, by making each line its own node, with no central surface.
    Use np.vstack to hack up bits of the whole fence control points array into individual line segments.

11 January 2024:
    The decree has been made: the span of a group_object or a curve_object will only be relative to its own origin.
    In other words, a translation factor will not be added to span.
    This is in accoradance with OOP principles. It will reduce confusion. And, it will keep bare the 0-0-0 data origin paradigm, which might be subject to change in the future, but in the present it allows us to manage it.
    Then, what will happen to the node name of group lines? They will need a translation factor, I imagine, in a similar way that naming for ticks_redundant is informed of scaling.

The current (17 Nov 2023) feed to the createFBX module has a set of lists that are indexable fort each data object, sourced from each CSV.
The inputs that deviating from this are the FBX filenmame and the file encoding.
For group translation (origin placement, orientation, as well as labels and fences), it would be right to feed in group objects.
How? Firstly, what would exist after/for the pyplot/pygame preview that can subsequently be fed to the createFBX module?
How can translation and origin data be tied to fence and label (line) data?

Deal with subgroup relative origins within group, and group relative origin within the scene.
It doesn't have to be inherent if there is also fed an index-correlated origin list, which could be generated within the same loop.

Naming convention: lose the 's' plurality for both 'labels' and 'fences', indicated there is only one fence and one label per group

'''
import numpy as np
import math # for the elliptical/circular fence trigonometry

def cleanstr(string):
    return string.replace('\n','').replace('[ ','[').replace(' ',',').replace(',,',',') + "_"
    #.replace('[,','[').replace('][','],[')  not used, but keep ready
class Fences:
    style_object = None
    scene_object = None
    hierarchy_object = None

    @classmethod
    def assign_scene_object_etc(cls,scene_object):
        cls.scene_object = scene_object
        cls.style_object = scene_object.style_object
        cls.hierarchy_object = scene_object.hierarchy_object

    def __init__(self):
        self.name = 'fences'
    def generate_fences(self):

        for key,curve_object in self.hierarchy_object.dict_curve_objects_all.items():
            curve_fences_arrays = self.build_object_fences(active_object = curve_object) # this approach should instead accept any pavlov object

        for group_object in self.hierarchy_object.dict_group_objects_most.values():
            if self.style_object.group_labels_outside_fences is True:
                group_fences_arrays = self.build_object_fences_without_label(active_object = group_object) # this approach should instead accept any pavlov object  build_object_fences_without_label(

            else:
                group_fences_arrays = self.build_object_fences(active_object = group_object) # this approach should instead accept any pavlov object  
            
        # scene_object
        #group_fences_arrays = self.build_object_fences(active_object = self.scene_object) # this approach should instead accept any pavlov object  

    def build_object_fences(self,active_object):
        # minimum edge paradogm vs a data origin paradigm, for curves relative to their super group or the entire scene
        
        # span_relative_to_scene_minimum_edge_at_zero_height_plane is set in translation.py
        '''
        cp_bottom = fence_controlPoints_bottom(active_object.span_relative_to_scene_minimum_corner_origin)
        cp_back = fence_controlPoints_back(active_object.span_relative_to_scene_minimum_corner_origin)
        cp_right = fence_controlPoints_right(active_object.span_relative_to_scene_minimum_corner_origin
        '''                                  
        #print(f"active_object.span_relative_to_scene_data_origin = {active_object.span_relative_to_scene_data_origin}")
        try:
            # if the name is not input into the known group binning in the GUI,an error will come here
            if False: # standard
                cp_bottom = self.fence_controlPoints_bottom(active_object.span_relative_to_scene_minimum_edge_at_zero_height_plane)
                cp_back = self.fence_controlPoints_back(active_object.span_relative_to_scene_minimum_edge_at_zero_height_plane)
                cp_right = self.fence_controlPoints_right(active_object.span_relative_to_scene_minimum_edge_at_zero_height_plane)
            if True: # test
                cp_bottom = self.fence_controlPoints_bottom(active_object.span_relative_to_scene_data_origin)
                cp_back = self.fence_controlPoints_back(active_object.span_relative_to_scene_data_origin)
                cp_right = self.fence_controlPoints_right(active_object.span_relative_to_scene_data_origin)

        except:
            active_object.scene_object.cmd_output = active_object # this is meant to allow the command to be accessed for troubleshooting
            print(f'active_object.name:{active_object.name}, active_object.scene_object.cmd_output:{active_object.scene_object.cmd_output}')
            print(f'o.span_relative_to_scene_minimum_edge_at_zero_height_plane is called in main and assigned in translation by translation.calculate_span_relative_to_scene_minimum_edge_at_zero_height_plane_top_down(), interating top down')
            print("We need to add groups and subgroups to hold files that don't fit into the user-provided group names")
            print("span determination error: cp_bottom = fence_controlPoints_bottom(active_object.span_relative_to_scene_minimum_edge_at_zero_height_plane)")
        
        group_fences_arrays = self.build_fence_arrays(active_object,cp_bottom,cp_back,cp_right)
        return group_fences_arrays

    def build_object_fences_without_label(self,active_object):
        cp_bottom = self.fence_controlPoints_bottom(active_object.span_relative_to_scene_data_origin_without_text_label)
        cp_back = self.fence_controlPoints_back(active_object.span_relative_to_scene_data_origin_without_text_label)
        cp_right = self.fence_controlPoints_right(active_object.span_relative_to_scene_data_origin_without_text_label)
        group_fences_arrays = self.build_fence_arrays(active_object,cp_bottom,cp_back,cp_right)
        return group_fences_arrays

    def build_fence_arrays(self,active_object,cp_bottom,cp_back,cp_right):
        group_fences_arrays = []
        # named version, to communicate coordinates of lines
        # busy as hell, but useful for troubleshooting
        # needs updated for oop, with dictionaries. And possible fence.py, fence_machine.py, etc
        group_fence_array = ["Bottom: "+active_object.name,None]
        group_fences_arrays.append(group_fence_array)
        name=cleanstr(str(np.round(cp_bottom[0:2],2))) # this replacement of the newline character is necessary if you want to export to ascii. 
        group_fences_arrays.append([name,np.vstack([cp_bottom[0:2],cp_bottom[0]])])
        name=cleanstr(str(np.round(cp_bottom[1:3],2)))
        group_fences_arrays.append([name,np.vstack([cp_bottom[1:3],cp_bottom[1]])])
        name=cleanstr(str(np.round(cp_bottom[2:4],2)))
        group_fences_arrays.append([name,np.vstack([cp_bottom[2:4],cp_bottom[2]])])
        name=cleanstr(str(np.round(cp_bottom[3:5],2)))
        group_fences_arrays.append([name,np.vstack([cp_bottom[3:5],cp_bottom[3]])])
        group_fences_arrays.append([None,None]) # exit code, so it knows to pop out a level
        
        '''alt # concise and generalizable, but over-optimized for now # the point here is to preare for an elliptical or circular bottom fence
        group_fence_array_chunk = [["Bottom: "+active_object.name,None]]
        for i in range(len(cp_right)):
            group_fence_array_chunk = self._generate_fence_segment_details(i,group_fence_array_chunk,fence_controlPoints_matrix=cp_bottom)
        group_fence_array_chunk.append([None,None])
        # use oop dictionary here as well, though i like feeding in linearly like this. All good things...
        group_fences_arrays.extend(group_fence_array_chunk) #changed from append
        # end alt'''

        if self.style_object.add_bottom_fence_only is False:
            group_fence_array = ["Back: "+active_object.name,None]
            group_fences_arrays.append(group_fence_array)
            name=cleanstr(str(np.round(cp_back[0:2],2)))
            group_fences_arrays.append([name,np.vstack([cp_back[0:2],cp_back[0]])])
            name=cleanstr(str(np.round(cp_back[1:3],2)))
            group_fences_arrays.append([name,np.vstack([cp_back[1:3],cp_back[1]])])
            name=cleanstr(str(np.round(cp_back[2:4],2)))
            group_fences_arrays.append([name,np.vstack([cp_back[2:4],cp_back[2]])])
            name=cleanstr(str(np.round(cp_back[3:5],2)))
            group_fences_arrays.append([name,np.vstack([cp_back[3:5],cp_back[3]])])
            group_fences_arrays.append([None,None])

        if self.style_object.add_bottom_fence_only is False:
            group_fence_array = ["Right: "+active_object.name,None]
            group_fences_arrays.append(group_fence_array)
            name=cleanstr(str(np.round(cp_right[0:2],2)))
            group_fences_arrays.append([name,np.vstack([cp_right[0:2],cp_right[0]])])
            name=cleanstr(str(np.round(cp_right[1:3],2)))
            group_fences_arrays.append([name,np.vstack([cp_right[1:3],cp_right[1]])])
            name=cleanstr(str(np.round(cp_right[2:4],2)))
            group_fences_arrays.append([name,np.vstack([cp_right[2:4],cp_right[2]])])
            name=cleanstr(str(np.round(cp_right[3:5],2)))
            group_fences_arrays.append([name,np.vstack([cp_right[3:5],cp_right[3]])])
            group_fences_arrays.append([None,None])

        active_object.fence_lines = group_fences_arrays # this is what makes it into the program
        return group_fences_arrays

    """ def _generate_fence_segment_details(self,i,group_fence_array_chunk,fence_controlPoints_matrix):
        line_segment_controlpoints = np.vstack([fence_controlPoints_matrix[i:i+2],fence_controlPoints_matrix[i]])
        name=str(np.round(fence_controlPoints_matrix[i:i+2],2))
        group_fence_array_chunk.append([name,line_segment_controlpoints])
        return group_fence_array_chunk """

    def fence_controlPoints_bottom(self,span):
        '''
        Here, a complete fence is provided, with all four corners and then a revisit to the first corner.
        Above, these control points are hacked up into groups of two, where two points are used and then the first of the two is revisited.
        '''
        # Is span accurate to the object origin or to the scene origin?
        # It depends if it includes translation or not. I'm starting to think that span should not include translation, for an OOP paradigm.
        # Ergo, object.span will be relative to the origin of the object.
        [[minTime,maxTime],\
        [minHeight,maxHeight],\
        [minDepth,maxDepth]] = span

        zero=0
        fence_controlPoints_matrix = \
        np.array([\
        [minTime, minHeight, minDepth],
        [minTime, minHeight, maxDepth],
        [maxTime, minHeight, maxDepth],
        [maxTime, minHeight, minDepth],
        [minTime, minHeight, minDepth]])
        
        return fence_controlPoints_matrix

    def fence_controlPoints_back(self,span):
        '''
        Here, a complete fence is provided, with all four corners and then a revisit to the first corner.
        Above, these control points are hacked up into groups of two, where two points are used and then the first of the two is revisited.
        '''
        [[minTime,maxTime],\
        [minHeight,maxHeight],\
        [minDepth,maxDepth]] = span

        zero=0
        
        fence_controlPoints_matrix = \
        np.matrix([\
        [minTime, minHeight, minDepth],
        [minTime, maxHeight, minDepth],
        [maxTime, maxHeight, minDepth],
        [maxTime, minHeight, minDepth],
        [minTime, minHeight, minDepth]])
        
        return fence_controlPoints_matrix

    def fence_controlPoints_right(self,span):
        '''
        Here, a complete fence is provided, with all four corners and then a revisit to the first corner.
        Above, these control points are hacked up into groups of two, where two points are used and then the first of the two is revisited.
        '''
        [[minTime,maxTime],\
        [minHeight,maxHeight],\
        [minDepth,maxDepth]] = span

        zero=0
        fence_controlPoints_matrix = \
        np.matrix([\
        [maxTime, minHeight, minDepth],
        [maxTime, minHeight, maxDepth],
        [maxTime, maxHeight, maxDepth],
        [maxTime, maxHeight, minDepth],
        [maxTime, minHeight, minDepth]])
        
        return fence_controlPoints_matrix
    
    def fence_controlPoints_bottom_ellipse(self,span):
        '''
        Here, a complete fence is provided, with n corners and then a revisit to the first corner.
        Above, these control points are hacked up into groups of two, where two points are used and then the first of the two is revisited.
        '''
        # Is span accurate to the object origin or to the scene origin?
        # It depends if it includes translation or not. I'm starting to think that span should not include translation, for an OOP paradigm.
        # Ergo, object.span will be relative to the origin of the object.
        [[minTime,maxTime],\
        [minHeight,maxHeight],\
        [minDepth,maxDepth]] = span

        theta_list = [0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330,360] # instead, generate from value n, instead of using explicit theta values
        radius = shootme
        for theta in theta_list:
            theta = theta_list[i]
            time = radius*math.cos(math.radians(theta))
            depth = radius*math.cos(math.radians(theta))
        # this should all be an ellipse 
        translation_time = 0
        translation_depth = 0
        
        zero=0
        fence_controlPoints_matrix = \
        np.array([\
        [minTime, minHeight, minDepth],
        [minTime, minHeight, maxDepth],
        [maxTime, minHeight, maxDepth],
        [maxTime, minHeight, minDepth],
        [minTime, minHeight, minDepth]])
        
        return fence_controlPoints_matrix
    

