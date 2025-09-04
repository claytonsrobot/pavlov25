from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


class ConfigManager:
    def __init__(self):
        self.config = ExportConfig()

    def pull_values(self, export_control_object, gui_object=None):
        base = _to_dict(export_control_object)
        overrides = _to_dict(gui_object) if gui_object else {}

        # Downhill merge: gui overrides export object
        merged = {**base, **overrides}

        # Validate & coerce into typed config
        self.config = ExportConfig(**merged)

        return self.config
    
    def pull_values(self, export_control_object: Any, gui_overrides: Optional[Dict[str, Any]] = None):# -> ExportConfig:
        base = _to_dict(export_control_object)
        overrides = gui_overrides or {}
        merged = {**base, **overrides}
        self.config = ExportConfig(**merged)
        return self.config
    
class ExportConfig(BaseModel):
    axis_rotation_degrees_THD_CCW_time: List[float] = Field(default_factory=lambda: [45, 0, 0])
    axis_rotation_degrees_THD_CCW_height: List[float] = Field(default_factory=lambda: [45, 0, 90])
    axis_rotation_degrees_THD_CCW_depth: List[float] = Field(default_factory=lambda: [45, 90, 0])

    tick_numbering_rotation_degrees_THD_CCW_time: List[float] = Field(default_factory=lambda: [0, 0, 0])
    tick_numbering_rotation_degrees_THD_CCW_height: List[float] = Field(default_factory=lambda: [90, 90, 0])
    tick_numbering_rotation_degrees_THD_CCW_depth: List[float] = Field(default_factory=lambda: [0, 90, 90])


def get_gui_export_overrides(user_input_object) -> Dict[str, Any]:
    """
    Return a dict of override values taken from the GUI export-control window, if present and enabled.
    Defensive: returns {} if interface or window is not available.
    """
    try:
        iface = getattr(user_input_object, "interface_object", None)
        if not iface:
            return {}
        if not getattr(iface, "export_control_override", False):
            return {}
        win = getattr(iface, "export_control_window_object", None)
        if not win:
            return {}
        # collect keys we care about; be careful not to pull everything blindly
        keys = [
            "axis_rotation_degrees_THD_CCW_time",
            "axis_rotation_degrees_THD_CCW_height",
            "axis_rotation_degrees_THD_CCW_depth",
            "tick_numbering_rotation_degrees_THD_CCW_time",
            "tick_numbering_rotation_degrees_THD_CCW_height",
            "tick_numbering_rotation_degrees_THD_CCW_depth",
        ]
        overrides = {}
        for k in keys:
            if hasattr(win, k):
                overrides[k] = getattr(win, k)
        return overrides
    except Exception:
        # swallow only to be defensive — prefer to log in real app
        return {}
    
def apply_config_to_user_input(user_input_object, config: ExportConfig, *, keep_as_list=True):
    """
    Copy fields from config into user_input_object attributes.
    If keep_as_list is False, you can coerce to e.g. tuples or strings — but keep lists by default.
    """
    data = config.model_dump() if hasattr(config, "model_dump") else config.dict()
    for k, v in data.items():
        setattr(user_input_object, k, v)


def _to_dict(obj):
    """Coerce object into dict, whether it's already a dict, dataclass, or has __dict__."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):          # pydantic v2
        return obj.model_dump()
    if hasattr(obj, "dict"):                # pydantic v1
        return obj.dict()
    if hasattr(obj, "__dataclass_fields__"):  # dataclass
        return {k: getattr(obj, k) for k in obj.__dataclass_fields__}
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Cannot convert {type(obj)} to dict")

def to_dict(model):
    """Return dict from Pydantic v1 or v2 model."""
    if hasattr(model, "model_dump"):   # v2
        return model.model_dump()
    if hasattr(model, "dict"):         # v1
        return model.dict()
    raise TypeError(f"Not a Pydantic model: {type(model)}")

def to_json(model, **kwargs):
    """Return JSON string from Pydantic v1 or v2 model."""
    if hasattr(model, "model_dump_json"):  # v2
        return model.model_dump_json(**kwargs)
    if hasattr(model, "json"):             # v1
        return model.json(**kwargs)
    raise TypeError(f"Not a Pydantic model: {type(model)}")

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
