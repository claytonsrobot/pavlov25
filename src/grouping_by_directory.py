"""
Title: grouping_by_string.py
Author: Clayton Bennett
Created: 20 January 2024

Purpose:
Classic Pavlov grouping
""" 
from src import tradition
import os
from pathlib import Path
import src.json_handler
from src.hierarchy import get_group_filelist_from_loaded_grouping
from src.hierarchy import get_group_subgrouplist_from_loaded_grouping, assume_scene_directory_is_called_imports_in_intermediate_loaded_grouping
from src.directories import Directories
from src.hierarchy import Hierarchy
class Vars:
    # pass, with clarity :)
    comp_char = "/" #compound character
def assign_group_membership_for_complete_hierarchy_v0(hierarchy_object, loaded_grouping):

    # Use the existing json stucture, rather than "in" text based stuff.
    # 
    # Better yet,
    # add objects to groups
    # at conception of the groups, rather than later adding.
    
    #c_key: curve_object_key
    #g_key: group_object_key
    tally_of_curve_objects_assigned_to_a_group = 0
    # Starting with the curve_objects and then working up allows max and min values to be passed upward,like a classroom champion game of rock-paper-scissors
    # This relies on a naming convention grouping paradigm: groups are based on text flags that are present in filenames
    for t_key,tier_object in reversed(hierarchy_object.dict_tier_objects.items()):
        for g_key,group in tier_object.dict_group_objects.items():
            for c_key,curve_object in hierarchy_object.dict_curve_objects_all.items():
                if t_key+1 in hierarchy_object.dict_tier_objects and len(hierarchy_object.dict_tier_objects[t_key+1].dict_curve_objects)>0:
                    # are you at the bottom tier? Yes with the highest t_key value and with curve_objects in it.
                    # if data objects are in the tier, we assume it is the bottom tier (with the highest t_key value)
                    # to keep this true, subgroups with key 'none' will need to be created to hold data objects that are in a (higher)supergroup but have no relevant provided (immediate)super/group
                    for filename in get_group_filelist_from_loaded_grouping(loaded_grouping=loaded_grouping, group_name=group.simple_name.lower()):
                        #print(f"filename.lower() = {filename.lower()}")
                        #print(f"os.path.basename(filename).lower() = {os.path.basename(filename).lower()}")
                        
                        if os.path.basename(filename).lower()==c_key.lower():
                            group.add_curve_object(curve_object,c_key)
                            tally_of_curve_objects_assigned_to_a_group += 1 # once complete, will equal len(hierarchy_object.dict_curve_object_all.keys()). If it doesn't, there are 'none' type subgroups, where a curve_object fits into a stated group but none of its stated subgroups
                            # develop further how subgroups are added for 'none'. Add a 'none' to every group, then remove it later?
                        else:
                            pass
                        
                elif t_key+1 in hierarchy_object.dict_tier_objects and len(hierarchy_object.dict_tier_objects[t_key+1].dict_group_objects)>0:
                    # you are not at the bottom tier, and there are more groups to explore
                    for s_key,subgroup in hierarchy_object.dict_tier_objects[t_key+1].dict_group_objects.items():
                        if (
                            get_group_subgrouplist_from_loaded_grouping(loaded_grouping = loaded_grouping, group_name = group.simple_name.lower()) is not None
                            and subgroup.simple_name.lower() in get_group_subgrouplist_from_loaded_grouping(loaded_grouping = loaded_grouping, group_name = group.simple_name.lower()) 
                            ):
                            group.add_subgroup(subgroup,s_key) # need to check for redundancy, especially becuase this loop cycles through each curve name     
                else:              
                    print('problem==True')
    
    # check for curve_objects that have not been assigned a supergroup

def assign_curve_objects_to_groups(hierarchy_object, loaded_grouping):
    def traverse_directories(group_hierarchy, parent_group=None):
        # Iterate through each directory
        for directory in group_hierarchy.get("directories", []):
            group_name = directory.get("directory", "")
            # Find the corresponding group in the hierarchy object
            group = hierarchy_object.dict_group_objects_all.get(group_name)

            # Assign curve objects to the group by matching filenames
            if group:
                for curve_key, curve_object in hierarchy_object.dict_curve_objects_all.items():
                    if any(
                        curve_key.lower() == filename.lower()
                        for filename in directory.get("files", [])
                    ):
                        group.add_curve_object(curve_object, curve_key)

            # Recursive call for subdirectories
            traverse_directories(directory, group)

    # Start traversing the loaded grouping hierarchy
    traverse_directories(loaded_grouping)

def assign_subgroups_to_groups(hierarchy_object, loaded_grouping):
    def traverse_directories(group_hierarchy, parent_group=None):
        # Iterate through each directory
        for directory in group_hierarchy.get("directories", []):
            group_name = directory.get("directory", "")
            # Find the corresponding group in the hierarchy object
            group = hierarchy_object.dict_group_objects_all.get(group_name)

            # If there’s a parent group, establish the subgroup relationship
            if parent_group and group:
                parent_group.add_subgroup(group, group_name)

            # Recursive call for subdirectories
            traverse_directories(directory, group)

    # Start traversing the loaded grouping hierarchy
    traverse_directories(loaded_grouping)

def assign_group_membership_for_complete_hierarchy_v2(hierarchy_object, loaded_grouping):
    def assign_to_groups_v1(tier_object, loaded_grouping):
        """
        Helper function to assign curve objects and subgroups to groups within a tier object.
        """
        for group_key, group_object in tier_object.dict_group_objects.items():
            # Assign curve objects to groups based on loaded_grouping
            for curve_key, curve_object in hierarchy_object.dict_curve_objects_all.items():
                if any(
                    curve_key.lower() == filename.lower()
                    for filename in get_group_filelist_from_loaded_grouping(
                        loaded_grouping=loaded_grouping, group_name=group_object.simple_name.lower()
                    )
                ):
                    group_object.add_curve_object(curve_object, curve_key)

            # Assign subgroups recursively if the group exists in loaded_grouping
            for subgroup_key, subgroup_object in group_object.dict_subgroups.items():
                if subgroup_key in get_group_subgrouplist_from_loaded_grouping(
                    loaded_grouping=loaded_grouping, group_name=group_object.simple_name.lower()
                ):
                    group_object.add_subgroup(subgroup_object, subgroup_key)

    # Traverse through all tiers in the hierarchy
    for tier_key, tier_object in hierarchy_object.dict_tier_objects.items():
        assign_to_groups_v1(tier_object, loaded_grouping)


def assign_group_membership_for_complete_hierarchy_v3(hierarchy_object, loaded_grouping):
    def assign_to_groups_v3(tier_object, loaded_grouping):
        """
        Helper function to assign curve objects and subgroups to groups within a tier object.
        """
        for group_key, group_object in tier_object.dict_group_objects.items():
            # Assign curve objects to groups based on loaded_grouping
            for curve_key, curve_object in hierarchy_object.dict_curve_objects_all.items():
                if any(
                    curve_key.lower() == os.path.splitext(filename)[0].lower()
                    for filename in get_group_filelist_from_loaded_grouping(
                        loaded_grouping=loaded_grouping, group_name=group_object.simple_name.lower()
                    )
                ):
                    group_object.add_curve_object(curve_object, curve_key)

            # Assign subgroups recursively if the group exists in loaded_grouping
            for subgroup_key, subgroup_object in group_object.dict_subgroups.items():
                if subgroup_key in get_group_subgrouplist_from_loaded_grouping(
                    loaded_grouping=loaded_grouping, group_name=group_object.simple_name.lower()
                ):
                    group_object.add_subgroup(subgroup_object, subgroup_key)

    # Traverse through all tiers in the hierarchy
    for tier_key, tier_object in hierarchy_object.dict_tier_objects.items():
        assign_to_groups_v3(tier_object, loaded_grouping)

def assign_group_membership_for_complete_hierarchy_v4(hierarchy_object, loaded_grouping):
    """
    Assigns curve objects to groups and organizes subgroups based on the structured `loaded_grouping`.
    """
    group_mapping = {}
    
    # Step 1: Preprocess `loaded_grouping` to create a structured mapping
    for group_name, data in loaded_grouping.items():
        if not isinstance(data, dict):
            print(f"Warning: Expected dictionary for group '{group_name}', but got {type(data)}. Skipping.")
            continue
        
        group_mapping[group_name] = {
            "curve_objects": set(data.get("files", [])),  # Adjusted key from 'curve_objects' to 'files'
            "subgroups": set(data.get("directories", []))  # Adjusted key from 'subgroups' to 'directories'
        }
    
    # Step 2: Assign curve objects to their respective groups
    for group_name, data in group_mapping.items():
        if group_name in hierarchy_object.dict_group_objects_all:
            group = hierarchy_object.dict_group_objects_all[group_name]
            for curve_key in data["curve_objects"]:
                if curve_key in hierarchy_object.dict_curve_objects_all:
                    curve_object = hierarchy_object.dict_curve_objects_all[curve_key]
                    group.add_curve_object(curve_object, curve_key)
    
    # Step 3: Assign subgroups to their parent groups
    for group_name, data in group_mapping.items():
        if group_name in hierarchy_object.dict_group_objects_all:
            parent_group = hierarchy_object.dict_group_objects_all[group_name]
            for subgroup_name in data["subgroups"]:
                if subgroup_name in hierarchy_object.dict_group_objects_all:
                    subgroup = hierarchy_object.dict_group_objects_all[subgroup_name]
                    parent_group.add_subgroup(subgroup, subgroup_name)
    
    # Step 4: Handle unassigned curve objects (optional)
    unassigned_group = hierarchy_object.dict_group_objects_all.get("none")
    if unassigned_group:
        for curve_key, curve_object in hierarchy_object.dict_curve_objects_all.items():
            if not any(curve_key in data["curve_objects"] for data in group_mapping.values()):
                unassigned_group.add_curve_object(curve_object, curve_key)

def assign_group_membership_for_complete_hierarchy_v5(hierarchy_object, loaded_grouping):
    """
    Recursively processes `loaded_grouping` and assigns curve objects to groups while organizing subgroups.
    """
    def process_directory(directory_data, parent_group=None):
        if not isinstance(directory_data, dict) or "directory" not in directory_data:
            print(f"Warning: Skipping invalid directory data: {directory_data}")
            return
        
        group_name = directory_data["directory"]
        group_name = assume_scene_directory_is_called_imports_in_intermediate_loaded_grouping(group_name)
        #if group_name not in hierarchy_object.dict_group_objects_all:
        #    hierarchy_object.dict_group_objects_all[group_name] = GroupObject(group_name)  # Assuming GroupObject exists
        print(f"group_name = {group_name}")
        current_group = hierarchy_object.dict_group_objects_all[group_name]
        print(f"current_group = {current_group}")
        if parent_group:
            parent_group.add_subgroup(current_group, group_name)
        
        for file_name in directory_data.get("files", []):
            if file_name in hierarchy_object.dict_curve_objects_all:
                curve_object = hierarchy_object.dict_curve_objects_all[file_name]
                current_group.add_curve_object(curve_object, file_name)
        
        for subdirectory in directory_data.get("directories", []):
            process_directory(subdirectory, current_group)
    
    process_directory(loaded_grouping)

def assign_group_membership_for_complete_hierarchy(hierarchy_object, loaded_grouping):
    """
    Recursively processes `loaded_grouping` and assigns curve objects to groups while organizing subgroups.
    """
    def find_group(group_name):
        for existing_group in hierarchy_object.dict_group_objects_all.values():
            if existing_group.simple_name == group_name:
                return existing_group
    
    def process_directory(directory_data, parent_group=None):
        if not isinstance(directory_data, dict) or "directory" not in directory_data:
            print(f"Warning: Skipping invalid directory data: {directory_data}")
            return
        
        group_name = directory_data["directory"]
        group_name = assume_scene_directory_is_called_imports_in_intermediate_loaded_grouping(group_name)
        current_group = find_group(group_name)
        print(f"group_name = {group_name}")
        print(f"current_group = {current_group}")
        
        if parent_group:
            parent_group.add_subgroup(current_group, group_name)
        
        for file_name in directory_data.get("files", []):
            if file_name in hierarchy_object.dict_curve_objects_all:
                curve_object = hierarchy_object.dict_curve_objects_all[file_name]
                current_group.add_curve_object(curve_object, file_name)
        
        for subdirectory in directory_data.get("directories", []):
            process_directory(subdirectory, current_group)
    
    process_directory(loaded_grouping)

def walk_loaded_grouping():
    assign_supergroup()
    assign_child()
    assign_cousin()
    assign_uncle
    
class Group:
    def __init__(self, name):
        self.name = name
        self.children = set()  # Immediate children
        self.progeny = set()   # All descendants
        self.parents = set()

class Entity:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.cousins = set()
        self.cousin_flight = set()
        self.second_cousins = set()
        self.second_cousin_flight = set()

def process_json(json_data):
    # Parse JSON and build group/entity objects
    groups = {}
    entities = {}
    # Walk the JSON structure recursively
    def assign_relationships(data, parent=None):
        if data["type"] == "group" or data["type"] == "directory":
            group = Group(data["name"])
            groups[data["name"]] = group
            if parent:
                parent.children.add(group)
                parent.progeny.add(group)
            for child in data["children"]:
                assign_relationships(child, group)
        elif data["type"] == "entity" or data["type"] == "file":
            entity = Entity(data["name"], data["position"])
            entities[data["name"]] = entity
            if parent:
                parent.children.add(entity)
                parent.progeny.add(entity)
            # Assign cousins and other relationships later
    assign_relationships(json_data)
    return groups, entities

def example():
    # Example usage
    json_data = {
        # JSON structure as input
    }
    groups, entities = process_json(json_data)

def define_groups(loaded_grouping):
    "Walk the loaded grouping and "
    #hierarchy_object = Hierarchy()
    #hierarchy_object.walk_loaded_grouping(loaded_grouping)
    root_group = tradition.build_tradition(loaded_grouping)
    #return hierarchy_object
    return True
def get_group_names_and_subgroup_names_and_file_names_from_import_directory_hierarchy(directory):
    # assumes three tiers - in future make modular to any size
    #directory = cls.get_import_dir()
    print(f"directory = {directory}")
    group_names = check_first_level_import_directory_names(directory)
    subgroup_names = check_second_level_import_directory_names(directory,group_names)
    file_paths, file_names = check_third_level_import_file_names(directory,group_names,subgroup_names)
    return group_names, subgroup_names, file_paths, file_names

def check_first_level_import_directory_names(directory):
    # looks at tree in grouping directory to assess group names 
    # cls.get_import_dir() # path of top layer
    #group_names = [x[1] for x in os.walk(cls.get_import_dir())]
    group_names = next(os.walk(directory))[1]
    print(f"group_names = {group_names}")
    return group_names

def check_second_level_import_directory_names(directory,group_names):
    subgroup_names = []
    for group_name in group_names:
        subgroups_of_group = next(os.walk(directory+group_name))[1]
        subgroup_names.extend(subgroups_of_group)
    print(f"subgroup_names = {subgroup_names}")
    return subgroup_names

def check_third_level_import_file_names(directory,group_names,subgroup_names):
    file_paths = []
    file_names = []
    for group_name in group_names:
        for subgroup_name in subgroup_names: 
            try:
                directory_pathlib = Path(directory) / group_name / subgroup_name
                for file_path in directory_pathlib.iterdir(): # special chars make it go whack
                    if file_path.is_file():
                        file_paths.append(str(file_path))
                        filename = os.path.basename(str(file_path).replace('\\', '/'))
                        file_names.append(filename)
            except Exception as e:
                print(f"Error processing directory: {directory_pathlib}. Error: {e}")
    return file_paths, file_names



def generate_directory_structure(path):
    # Extract the root folder's name
    folder_name = os.path.basename(os.path.abspath(path))
    #structure = {"group": folder_name, "entities": [], "groups": []}
    structure = {"group": folder_name, "path": path, "entities": [], "groups": []}

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            if item != "desktop.ini":
                #structure["entities"].append(item)
                structure["entities"].append({"name": item, "path": item_path})
        elif os.path.isdir(item_path):
            structure["groups"].append(generate_directory_structure(item_path))

    return structure

def call(directory_path): # example
    # Replace 'your_directory_path' with the path to the directory you want to analyze
    output_file = Directories.get_group_by_directory_intermediate_export_json_filepath()
    # Step 1: Generate the directory structure with files appearing first
    directory_structure = generate_directory_structure(directory_path)
    # Step 2: Export the structure to a JSON file
    src.json_handler.export_to_json(directory_structure, output_file)
    print(f"JSON file '{output_file}' has been created!")
    return directory_structure
