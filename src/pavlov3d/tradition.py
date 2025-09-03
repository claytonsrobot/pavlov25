
from pavlov3d.curve import Curve
from pavlov3d import numeric_islands
class Tradition:
    """Careful. This whole thing assumes a JSON structure has been captured to represent a file structure, but it doesn't actually check the paths."""
    root_group = None
    @classmethod
    def set_root_group(cls,group):
        cls.root_group = group
    @classmethod
    def get_root_group(cls):
        return cls.root_group

class Group:
    """
    The Group class represents a hierarchical collection of groups and entities
    within the defined directory structure. This class facilitates managing 
    relationships, such as immediate children, all descendants (progeny), and 
    parent groups.

    Attributes:
    ----------
    name : str
        The name of the group, corresponding to a directory in the structure.
    entities : set
        A set of Entity objects directly associated with this group (files in the directory).
    children : set
        A set of Group or Entity objects that are direct descendants of this group.
    progeny : set
        A set containing all descendants of this group, including both groups and entities.
    parents : set
        A set of parent groups for this group.

    Methods:
    -------
    add_child(child):
        Adds a child (Group or Entity) to the current group, updating both
        immediate children and the list of all progeny.
    """
    def __init__(self, name):
        self.name = name
        self.entities = set()  # Files within the group
        self.children = set()  # Immediate subgroups
        self.progeny = set()   # All descendants (groups and entities)
        self.parents = set()   # Parent groups
    
    def add_child(self, child):
        self.children.add(child)
        self.progeny.add(child)
        if isinstance(child, Group):
            self.progeny.update(child.progeny)

class Entity:
    def __init__(self, name, position=None):
        self.name = name
        self.position = position
        self.cousins = set()  # Cousins in sibling groups
        self.cousin_flight = set()  # Cousins with shared position
        self.second_cousins = set()
        self.second_cousin_flight = set()

def build_tradition(data, parent=None):
    # Create either a Group or an Entity based on the structure
    if "group" in data:
        group = Group(data["group"])
        if parent:
            parent.add_child(group)
            group.parents.add(parent)
        for subgroup_data in data.get("groups", []):
            build_tradition(subgroup_data, group)
        for entity_data in data.get("entities", []):
            entity = Entity(entity_data["name"])
            entity.path = entity_data["path"] 
            #curve_object = Curve(name=entity_data["name"])
            group.entities.add(entity)
            group.progeny.add(entity)
        Tradition.set_root_group(group)
        return group
    elif "entities" in data:
        # Process entities directly if found (shouldn't happen in currentformat)
        for entity_data in data.get("entities", []):
            entity = Entity(entity_data["name"])
            entity.path = entity_data["path"]  # Assign relative path
            return entity

        
def get_sorted_entity_filenames(group):
    """
    Traverses the entire group hierarchy to collect and sort all entity relative filepaths.

    Parameters:
    ----------
    group : dict
        The root group to start traversing from.

    Returns:
    -------
    List[str]
        A naturally sorted list of relative filepaths from all entities within the hierarchy.
    """
    entity_filepaths = []

    def traverse(current_group):
        # Add all entities' relative paths in the current group
        for entity in current_group.entities:
            entity_filepaths.append(entity.path)

        
        # Recursively traverse child groups
        for child_group in current_group.children:  # Assuming `children` is a set of Group objects
            if isinstance(child_group, Group):  # Only traverse sub-groups
                traverse(child_group)

    
    # Start traversal from the root group
    traverse(group)

    # Return the naturally sorted list of relative filepaths
    sorted_filenames, sorted_filepaths = numeric_islands.get_sorted_filenames_and_filepaths(entity_filepaths)
    return sorted_filenames, sorted_filepaths

def test():
    # Example JSON Input
    json_data_filepaths = {
        "group": "imports",
        "path": "imports",
        "entities": [],
        "groups": [
            {
                "group": "test1",
                "path": "imports/test1",
                "entities": [],
                "groups": [
                    {
                        "group": "2024-07July-02 to 2024-07July-16",
                        "path": "imports/test1/2024-07July-02 to 2024-07July-16",
                        "entities": [
                            {
                                "name": "AIC4021.csv",
                                "path": "imports/test1/2024-07July-02 to 2024-07July-16/AIC4021.csv"
                            },
                            {
                                "name": "AIC4122.csv",
                                "path": "imports/test1/2024-07July-02 to 2024-07July-16/AIC4122.csv"
                            }
                        ],
                        "groups": []
                    },
                    {
                        "group": "2024-07July-16 to 2024-07July-30",
                        "path": "imports/test1/2024-07July-16 to 2024-07July-30",
                        "entities": [
                            {
                                "name": "AIC4025.csv",
                                "path": "imports/test1/2024-07July-16 to 2024-07July-30/AIC4025.csv"
                            },
                            {
                                "name": "AIC4126.csv",
                                "path": "imports/test1/2024-07July-16 to 2024-07July-30/AIC4126.csv"
                            }
                        ],
                        "groups": []
                    }
                ]
            },
            {
                "group": "test2",
                "path": "imports/test2",
                "entities": [],
                "groups": [
                    {
                        "group": "2024-07July-02 to 2024-07July-16-2",
                        "path": "imports/test2/2024-07July-02 to 2024-07July-16-2",
                        "entities": [
                            {
                                "name": "AIC402.csv",
                                "path": "imports/test2/2024-07July-02 to 2024-07July-16-2/AIC402.csv"
                            },
                            {
                                "name": "AIC412.csv",
                                "path": "imports/test2/2024-07July-02 to 2024-07July-16-2/AIC412.csv"
                            }
                        ],
                        "groups": []
                    }
                ]
            }
        ]
    }


    # Process the JSON
    root_group = build_tradition(json_data_filepaths)

    # Print structure for debugging
    def print_group(group, level=0):
        print("  " * level + f"Group: {group.name}")
        print("  " * level + f"  Entities: {[entity.name for entity in group.entities]}")
        for child in group.children:
            print_group(child, level + 1)

    print_group(root_group)
    
    # Example usage of get_sorted_entity_filenames)
    sorted_filenames, sorted_filepaths = get_sorted_entity_filenames(root_group)
    print(sorted_filenames) 
    print(sorted_filepaths)
if __name__ == "__main__":
    test()
