from pydantic import BaseModel, Field
from typing import Optional, List


class ConfigManager:
    def __init__(self):
        self.config = ExportConfig()

    def pull_values(self, export_control_object, gui_object=None):
        base = to_dict(export_control_object)
        overrides = to_dict(gui_object) if gui_object else {}

        # Downhill merge: gui overrides export object
        merged = {**base, **overrides}

        # Validate & coerce into typed config
        self.config = ExportConfig(**merged)

        return self.config
    
class ExportConfig(BaseModel):
    axis_rotation_degrees_THD_CCW_time: List[float] = Field(default_factory=lambda: [45, 0, 0])
    axis_rotation_degrees_THD_CCW_height: List[float] = Field(default_factory=lambda: [45, 0, 90])
    axis_rotation_degrees_THD_CCW_depth: List[float] = Field(default_factory=lambda: [45, 90, 0])

    tick_numbering_rotation_degrees_THD_CCW_time: List[float] = Field(default_factory=lambda: [0, 0, 0])
    tick_numbering_rotation_degrees_THD_CCW_height: List[float] = Field(default_factory=lambda: [90, 90, 0])
    tick_numbering_rotation_degrees_THD_CCW_depth: List[float] = Field(default_factory=lambda: [0, 90, 90])



def to_dict(obj):
    """Coerce object into dict, whether it's already a dict, dataclass, or has __dict__."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):          # pydantic v2
        return obj.model_dump()
    if hasattr(obj, "dict"):                # pydantic v1
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Cannot convert {type(obj)} to dict")


if __name__ == "__main__":

    export_control_object = ExportConfig(
    axis_rotation_degrees_THD_CCW_time=45.0,
    tick_numbering_rotation_degrees_THD_CCW_height=90.0,
    )

    gui_object = {
        "axis_rotation_degrees_THD_CCW_time": 30.0  # overrides
    }

    cm = ConfigManager()
    final = cm.pull_values(export_control_object, gui_object)

    print(final.model_dump_json(indent=2))
