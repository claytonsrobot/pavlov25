'''
Title: chart_element.py
Created: 2 April 2024
Author: Clayton Bennett
'''

class ChartElement:
    def __init__(self,name,coords):
        self.name = name
        self.coords = coords
        self.element_span_relative_to_parent_data_origin = [[None,None],[None,None],[None,None]]
    def set_span_for_axis(self):
        coords = self.coords
        min_time = min(coords[:,0])
        min_height = min(coords[:,1])
        min_depth = min(coords[:,2])
        max_time = max(coords[:,0])
        max_height = max(coords[:,1])
        max_depth = max(coords[:,2])
        self.element_span_relative_to_parent_data_origin =[[min_time,max_time],[min_height,max_height],[min_depth,max_depth]] # assumption

    def convert_text_label_to_a_chart_element(self,text_label):
        eat_me = 1

