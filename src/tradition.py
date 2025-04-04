from src.curve import Curve
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
        for entity_name in data.get("entities", []):
            entity = Entity(entity_name)
            curve_object = Curve(name=entity_name)
            group.entities.add(entity)
            group.progeny.add(entity)
        return group
    elif "entities" in data:
        # Process entities directly if found (shouldn't happen in currentformat)
        for entity_name in data["entities"]:
            return Entity(entity_name)
        

def test():
    # Example JSON Input
    json_data = {
        "group": "imports",
        "entities": [],
        "groups": [
            {
                "group": "test1",
                "entities": [],
                "groups": [
                    {
                        "group": "2024-07July-02 to 2024-07July-16",
                        "entities": [
                            "AIC4021.csv",
                            "AIC4122.csv",
                            "AIC4243.csv",
                            "Evonik-PAA4.csv",
                            "Ratio-PAA5.csv"
                        ],
                        "groups": []
                    },
                    {
                        "group": "2024-07July-16 to 2024-07July-30",
                        "entities": [
                            "AIC4025.csv",
                            "AIC4126.csv",
                            "AIC4247.csv",
                            "Evonik-PAA7.csv",
                            "Ratio-PAA7.csv"
                        ],
                        "groups": []
                    },
                    {
                        "group": "2024-07July-30 to 2024-08Aug-13",
                        "entities": [
                            "AIC4028.csv",
                            "AIC4128.csv",
                            "AIC4248.csv",
                            "Evonik-PAA8.csv",
                            "Ratio-PAA8.csv"
                        ],
                        "groups": []
                    }
                ]
            },
            {
                "group": "test2",
                "entities": [],
                "groups": [
                    {
                        "group": "2024-07July-02 to 2024-07July-16-2",
                        "entities": [
                            "AIC402.csv",
                            "AIC412.csv",
                            "AIC424.csv",
                            "Evonik-PAA.csv",
                            "Ratio-PAA.csv"
                        ],
                        "groups": []
                    },
                    {
                        "group": "2024-07July-16 to 2024-07July-30-2",
                        "entities": [
                            "AIC402.csv",
                            "AIC412.csv",
                            "AIC424.csv",
                            "Evonik-PAA.csv",
                            "Ratio-PAA.csv"
                        ],
                        "groups": []
                    },
                    {
                        "group": "2024-07July-30 to 2024-08Aug-13-2",
                        "entities": [
                            "AIC402.csv",
                            "AIC412.csv",
                            "AIC424.csv",
                            "Evonik-PAA.csv",
                            "Ratio-PAA.csv"
                        ],
                        "groups": []
                    }
                ]
            }
        ]
    }

    # Process the JSON
    root_group = build_tradition(json_data)

    # Print structure for debugging
    def print_group(group, level=0):
        print("  " * level + f"Group: {group.name}")
        print("  " * level + f"  Entities: {[entity.name for entity in group.entities]}")
        for child in group.children:
            print_group(child, level + 1)

    print_group(root_group)
if __name__ == "__main__":
    test()
