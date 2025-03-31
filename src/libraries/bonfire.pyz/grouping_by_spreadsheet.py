"""
Title: grouping_by_spreadsheet.py
Author: Clayton Bennett
Created: 20 January 2024

Purpose:
Explicit Pavlov grouping algorithm, using a mapping file, pointed to, in the groupings directory. 
Meant to minigate errors in grouping_by_text.py

Flow:
Check grouping-selection json file in groupings directory to know which grouping map file to use.
Import that CSV file, and look or particular headings (File., Group., Subgoup.)
USe np.getfromtext()

Elsewhere:
Implement select config and select group map functionality in CLI, to go beyond using the default in the json pointer file.
when rnning main in the CLI, also return the same objects you would get by running make, such that a user cn reference their variables for evaluation and also pick up in the middle
I.E, main in CLI should reference make? Also when does main before a class?

Inputs:
# SHould the JSON handler be called in user_config.py - Yes.
""" 
import numpy as np
from src.directories import Directories



def assign_group_membership_for_complete_hierarchy(hierarchy_object):
    hierarchy_object
    
    Directories.get_groupings_dir()


    with open(front+filepath, 'r', encoding='utf-8-sig') as f: 
        gdf = np.genfromtxt(f, dtype=None, delimiter=',', skip_header=0).tolist() # test
        gdf = np.array(gdf)
                
    pass