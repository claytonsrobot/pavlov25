'''
Title: flock.py
Author(s): Clayton Bennett and Chris Taylor
Created: 09 February 2025

Purpose:
Any collection of shape, or any portion of the entire scene pointcloud, can be referred to as a flock. 
A flock can be codified as a flock object.
A flock object can include a dictionary of shapes, as well as a dictionary of subflocks.  

Any shape in the scene belongs to a flock. A flock can contain shapes and/or subflocks.
Shapes and subflocks can colloquially together be referred to as allsubs. 
'''

class Flock:
    scene_object = None
    @classmethod
    def assign_scene_object(cls,scene_object):
        cls.scene_object = scene_object

    def __init__(self):
        self.name = None
        self.tier_level = int()

        '''Allsubs'''
        self.dict_subflocks = dict()
        self.dict_shapes = dict()
        
        '''Superflock'''
        #The superflock is the flock_object of which this flock is a subflock. 
        #The superflock is allowed to be the scene_object. 
        self.superflock = None # 

    ''' Functons: Setters >START '''
    def set_superflock(self,flock_object):
        self.superflock = flock_object
    def add_flock_to_subflock_dictionary(self,flock_object):
        # Consider making dict_subflocks a set of objects, insted of a dictionary, 
        # because key names could be a problem, in terms of redundancy.
        self.dict_subflocks.update({flock_object.name:flock_object}) # check for existing cmparable name
        flock_object.set_superflock(self)
    def add_shape_to_shape_dictionary(self,shape_object):
        # Consider making dict_shapes a set of shapes, insted of a dictionary, 
        # because key names could be a problem, in terms of redundancy.
        self.dict_subflocks.update({shape_object.name:shape_object}) # check for existing cmparable name
        shape_object.set_superflock(self)
    ''' Functons: Setters >END '''

    ''' Functions for testing and analysis >START '''
    def isf(self,integer):
        return self.intsubflock(integer) 
    def intsubflock(self,integer):
        # Expected form: flock_object.intsubflock(0)
        subflock_object = self._intdict(integer, self.dict_subflocks)
        return subflock_object
    def ish(self,integer):
        return self.intshape(integer)
    def intshape(self,integer):
        # Expected form: flock_object.intshape(0)
        shape_object = self._intdict(integer, self.dict_shapes)
        return shape_object
    def _intdict(self,integer,dictionary):
        # This lets you very quickly access a dictionary object using an integer.
        # General form, for .intshape() and .intsubflock() 
        # Expected use: To test and spot check, just look at the first entry using index 0: [0]
        if integer < len(dictionary):
            return list(dictionary.values())[integer]
        else:
            return None
    ''' Functions for testing and analysis >END '''
    
    ''' Functions for managing allsubs translation >START '''
    def determine_allsubs_origins_and_spans_relative_to_self_minimum_corner_at_zero_height_plane(self):
        pass 
        # Once complete, each allsub will have a value assigned for their 
        # attribute .origin_relative_to_superflock_minimum_corner_origin_at_zero_height_plane, 
        # which is orginally initializaed as np.array([None,None,None])

        # Also, once complete, each allsub will have a value assigned for their 
        # attribute .span_relative_to_superflock_minimum_corner_origin_at_zero_height_plane, 
        # which is orginally initializaed as np.array([None,None],
        #                                             [None,None],
        #                                             [None,None])

        return False
    ''' Functions for managing allsubs translation >END '''

