'''
Title: numeric_islands_object.py
Author: Clayton Bennett
Created: January 2024

Purpose: facilitate the sorting of filenames prior to import, when numbers might throw off the order by having missing leading zeros.

Class object instances are only created within this file.
Only the script is imported elsewhere, 
to call investigate_numeric_islands as the entry point.
'''
import re
import os
class NumericIslands:
    style_object=None
    user_input_object=None
    
    def __init__(self,name):
        self.name = name
        self.sortable_name = None
        #self.dict_contents = dict()
        self.list_island_start = None
        self.list_island_stop = None
        self.list_island_contents = None
        self.island_count = 0

    def add_island(self,island_start=None,island_stop=None,island_contents=None):
        if self.list_island_start is None:
            self.list_island_start=[island_start]
        else:
            self.list_island_start.append(island_start)

        if self.list_island_stop is None:
            self.list_island_stop=[island_stop]
        else:
            self.list_island_stop.append(island_stop)
    
        if self.list_island_contents is None:
            self.list_island_contents=[island_contents]
        else:
            self.list_island_contents.append(island_contents)
        
        self.island_count+=1
    
    @classmethod
    def add_class_attributes(cls,style_object,user_input_object):
        cls.style_object=style_object
        cls.user_input_object=user_input_object

cls = NumericIslands
def check_until_not_numeric(name,j):
    j_new=j
    numbers_found=''

    while j_new<len(name) and name[j_new].isnumeric():
        numbers_found =str(numbers_found+name[j_new])
        j_new+=1
    return j_new,numbers_found      

def equalize_numeric_island_lengths(dict_numeric_islands):
    #cls.style_object.dict_numeric_islands_og = dict_numeric_islands

    # approach for adding a leading zero to all single digit numerical islands
    # for each numeric island tha that has a length less than the target length, add that number of zeros to the contents
    # The start are stop tidbits should reference the original name
    
    names_sortable=[]
    for island_object in dict_numeric_islands.values():
        island_object.name_sortable=island_object.name
        sum_delta=0
        for i,island in enumerate(list(island_object.list_island_contents)):

            if len(island)<cls.style_object.n_numeric_island_size_target_after_leading_zero_insertion:
                n_add = cls.style_object.n_numeric_island_size_target_after_leading_zero_insertion-len(island)
                zeros_str = n_add*'0'
                replacement_island=str(zeros_str+island)
                island_object.list_island_contents[i]=replacement_island # this works
                a=island_object.list_island_start[i]+sum_delta
                b=island_object.list_island_stop[i]+sum_delta
                sum_delta+=n_add
                island_object.name_sortable=island_object.name_sortable[0:a]+replacement_island+island_object.name_sortable[b:]
            else:
                print("Error3.0, Numeric Islands")
        names_sortable.append(island_object.name_sortable)
    cls.style_object.dict_numeric_islands_final = dict_numeric_islands
    '''
    n=1
    # try 4, regex, add two zeros to one digit numbers or one zero to two digit numbers
    names_sortable=[]
    pattern = r'\b\d{n}\b'
    for key,island_object in dict_numeric_islands.items():
        island_object.name_sortable=island_object.name
        
        island_object.name_sortable = re.sub(pattern, lamdba x: f'0{x.group(0)}',island_object.name_sortable)
        names_sortable.append(island_object.name_sortable)
        '''
    return names_sortable

def investigate_numeric_islands(names,style_object,user_input_object):
    cls.add_class_attributes(style_object,user_input_object)
    dict_numeric_islands = dict()
    for i,name in enumerate(names):

        if not(any(char.isnumeric() for char in name)):
            dict_numeric_islands[i]=None
            # or pass ?

        else:
            j=0 # letter index
            while j<len(name):
                # first, go through all names, not editing, just recording what you find about numeric islands
                c=name[j]
                if c.isnumeric():
                    if not(i in dict_numeric_islands):
                        # make numeric island object instance, one for each filename
                        dict_numeric_islands[i]=NumericIslands(name = name)
                    else:
                        pass
                        print("Error1.0,Numeric Islands")
                    j_new,numbers_found = check_until_not_numeric(name,j)
                    #print(f'numbers_found = {numbers_found}')
                    if numbers_found == '':
                        print("How do we manage when no numbers are found?")
                    
                    dict_numeric_islands[i].add_island(island_start=j,island_stop=j_new,island_contents=numbers_found)    
                    j=j_new
                else:
                    j = j+1
            


    #return dict_numeric_islands
    names_sortable = equalize_numeric_island_lengths(dict_numeric_islands)
    return names_sortable

def natural_key(filepath):
    """
    Key function for natural sorting. Extracts numbers within a filepath
    and ensures they are sorted numerically while preserving non-numeric parts.

    Parameters:
    ----------
    filepath : str
        The filepath to be analyzed.

    Returns:
    -------
    List[Union[str, int]]
        A list of strings and integers for sorting purposes.
    """
    # Split the filepath into parts (strings and numbers)
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', filepath)]

def get_sorted_filenames_and_filepaths(filepaths):
    """
    Sorts filenames naturally while preserving their correlation with filepaths.

    Parameters:
    ----------
    filepaths : List[str]
        A list of filepaths.

    Returns:
    -------
    Tuple[List[str], List[str]]
        A tuple containing:
        - A naturally sorted list of filenames.
        - A list of filepaths ordered to match the sorted filenames.
    """
    # Create pairs of (filename, filepath) for sorting
    filename_filepath_pairs = [(os.path.basename(filepath), filepath) for filepath in filepaths]

    # Sort pairs by the natural order of filenames
    sorted_pairs = sorted(filename_filepath_pairs, key=lambda pair: natural_key(pair[0]))

    # Extract the sorted filenames and filepaths
    sorted_filenames = [pair[0] for pair in sorted_pairs]
    sorted_filepaths = [pair[1] for pair in sorted_pairs]

    return sorted_filenames, sorted_filepaths