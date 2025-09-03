# tests/test_config_manager.py

import types
from types import SimpleNamespace

import pytest

from pavlov3d.config_manager import (
    ExportConfig,
    ConfigManager,
    _to_dict,
    get_gui_export_overrides,
    apply_config_to_user_input,
)


def test_export_config_defaults_are_lists_of_three_floats():
    cfg = ExportConfig()
    # rotation fields exist and are lists of length 3
    assert isinstance(cfg.axis_rotation_degrees_THD_CCW_time, list)
    assert len(cfg.axis_rotation_degrees_THD_CCW_time) == 3
    assert all(isinstance(x, (int, float)) for x in cfg.axis_rotation_degrees_THD_CCW_time)

    assert isinstance(cfg.tick_numbering_rotation_degrees_THD_CCW_depth, list)
    assert len(cfg.tick_numbering_rotation_degrees_THD_CCW_depth) == 3


def test__to_dict_with_various_input_shapes():
    # 1) dict input
    src = {"axis_rotation_degrees_THD_CCW_time": [1, 2, 3]}
    assert _to_dict(src) == src

    # 2) pydantic model input
    p = ExportConfig(axis_rotation_degrees_THD_CCW_time=[11, 12, 13])
    pd = _to_dict(p)
    assert isinstance(pd, dict)
    assert pd["axis_rotation_degrees_THD_CCW_time"] == [11, 12, 13]

    # 3) plain object with __dict__
    class Fake:
        def __init__(self):
            self.axis_rotation_degrees_THD_CCW_time = [7, 8, 9]
            self.extra = "x"

    f = Fake()
    fd = _to_dict(f)
    assert fd["axis_rotation_degrees_THD_CCW_time"] == [7, 8, 9]
    assert fd["extra"] == "x"


def test_configmanager_pull_values_merges_plugin_and_gui_override():
    # Fake legacy plugin object (attributes)
    class FakePlugin:
        def __init__(self):
            self.axis_rotation_degrees_THD_CCW_time = [45, 0, 0]
            self.axis_rotation_degrees_THD_CCW_height = [45, 0, 90]
            self.tick_numbering_rotation_degrees_THD_CCW_time = [0, 0, 0]

    plugin = FakePlugin()

    # GUI override dict (only overrides time rotation)
    gui_overrides = {"axis_rotation_degrees_THD_CCW_time": [30, 0, 0]}

    cm = ConfigManager()
    cfg = cm.pull_values(plugin, gui_overrides)

    # assert that override applied
    assert cfg.axis_rotation_degrees_THD_CCW_time == [30, 0, 0]
    # assert that other defaults from plugin are preserved
    assert cfg.axis_rotation_degrees_THD_CCW_height == [45, 0, 90]
    # tick defaults should still be present
    assert cfg.tick_numbering_rotation_degrees_THD_CCW_time == [0, 0, 0]


def test_get_gui_export_overrides_when_enabled(monkeypatch):
    # Build fake user_input_object with nested interface and window objects
    export_win = SimpleNamespace(
        axis_rotation_degrees_THD_CCW_time=[10, 20, 30],
        axis_rotation_degrees_THD_CCW_height=[1, 2, 3],
        axis_rotation_degrees_THD_CCW_depth=[4, 5, 6],
        tick_numbering_rotation_degrees_THD_CCW_time=[0, 0, 0],
        tick_numbering_rotation_degrees_THD_CCW_height=[90, 90, 0],
        tick_numbering_rotation_degrees_THD_CCW_depth=[0, 90, 90],
    )
    iface = SimpleNamespace(export_control_override=True, export_control_window_object=export_win)
    user_input = SimpleNamespace(interface_object=iface)

    overrides = get_gui_export_overrides(user_input)
    # Only keys we listed should be present and equal to values from export_win
    assert overrides["axis_rotation_degrees_THD_CCW_time"] == [10, 20, 30]
    assert overrides["axis_rotation_degrees_THD_CCW_height"] == [1, 2, 3]
    assert "nonexistent_key" not in overrides


def test_apply_config_to_user_input_sets_attributes():
    cfg = ExportConfig(
        axis_rotation_degrees_THD_CCW_time=[3, 2, 1],
        tick_numbering_rotation_degrees_THD_CCW_depth=[9, 9, 9],
    )
    user_input = SimpleNamespace()
    apply_config_to_user_input(user_input, cfg)

    # After applying, attributes should be available on the user_input object
    assert hasattr(user_input, "axis_rotation_degrees_THD_CCW_time")
    assert user_input.axis_rotation_degrees_THD_CCW_time == [3, 2, 1]

    assert user_input.tick_numbering_rotation_degrees_THD_CCW_depth == [9, 9, 9]
