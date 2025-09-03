# tests/test_user_input.py
import pytest
from types import SimpleNamespace

from pavlov3d.user_input import UserInput, PluginResolver


# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture
def mock_style_object():
    class MockStyle:
        default_import_function = "default_import"
        default_export_function = "default_export"
        default_color_function = "default_color"

        def assign_plugin_dynamically(self, plugin_name):
            class PluginStub:
                filetype_allowed_list = ["csv", "gpx"]
            return PluginStub

        scene_object = SimpleNamespace(request=None)

    return MockStyle()


@pytest.fixture
def mock_interface_object():
    return SimpleNamespace(
        import_style_dictionary={"dropdown_import": "import_from_dropdown"},
        export_style_dictionary={"dropdown_export": "export_from_dropdown"},
        color_style_dictionary={"dropdown_color": "color_from_dropdown"},
    )


@pytest.fixture
def sample_cij():
    return {
        "import_style_plugin": "import_plugin_test",
        "export_style_plugin": "export_plugin_test1;export_plugin_test2",
        "color_style_plugin": "color_plugin_test",
        "stack_direction_groups": "group",
        "stack_direction_subgroups": "subgroup",
        "stack_direction_curves": "curve",
    }


@pytest.fixture
def user_input(mock_style_object, mock_interface_object):
    UserInput.assign_style_object(mock_style_object)
    UserInput.assign_interface_object(mock_interface_object)
    return UserInput()


# -----------------------------
# Tests
# -----------------------------

def test_pull_config_input_object(user_input, sample_cij):
    # Mock a config_input_object
    config_input_object = SimpleNamespace(
        loaded_config=sample_cij,
        grouping_algorithm="group-by-text",
        loaded_grouping={"group_names": ["G1"], "subgroup_names": ["SG1"]},
    )

    user_input.pull_config_input_object(config_input_object)

    # Check that config was loaded
    assert user_input.dict_config["import_style_plugin"] == "import_plugin_test"
    assert user_input.dict_config["export_style_plugin"] == "export_plugin_test1;export_plugin_test2"
    assert user_input.stack_direction_list == ["group", "subgroup", "curve"]

def test_determine_plugins_no_gui(user_input, sample_cij):
    config_input_object = SimpleNamespace(
        loaded_config=sample_cij,
        grouping_algorithm="group-by-text",
        loaded_grouping={"group_names": ["G1"], "subgroup_names": ["SG1"]},
    )
    user_input.pull_config_input_object(config_input_object)
    
    # Before plugin resolution
    assert user_input.import_function is None

    # Resolve plugins without GUI
    user_input.determine_which_plugins_to_use(gui_mode=False)

    # Check that plugins were normalized
    assert all(p.startswith("src.pavlov3d.plugins.") for p in user_input.import_style_plugin)
    assert all(p.startswith("src.pavlov3d.plugins.") for p in user_input.export_style_plugin)
    assert all(p.startswith("src.pavlov3d.plugins.") for p in user_input.color_style_plugin)


def test_determine_plugins_gui(user_input, mock_interface_object, sample_cij):
    # Prepare config input object
    config_input_object = SimpleNamespace(
        loaded_config=sample_cij,
        grouping_algorithm="group-by-text",
        loaded_grouping={"group_names": ["G1"], "subgroup_names": ["SG1"]},
    )
    user_input.pull_config_input_object(config_input_object)

    # Add dropdown overrides
    user_input.import_style_dropdown = ["dropdown_import"]
    user_input.export_style_dropdown = ["dropdown_export"]
    user_input.color_style_dropdown = ["dropdown_color"]

    user_input.determine_which_plugins_to_use(gui_mode=True)

    # Confirm resolved functions point to interface_object dictionaries
    assert user_input.import_function == mock_interface_object.import_style_dictionary["dropdown_import"]
    assert "export_from_dropdown" in user_input.export_function
    assert "color_from_dropdown" in user_input.color_function

def test_extract_filetypes_allowed_list(user_input, sample_cij):
    config_input_object = SimpleNamespace(
        loaded_config=sample_cij,
        grouping_algorithm="group-by-text",
        loaded_grouping={"group_names": ["G1"], "subgroup_names": ["SG1"]},
    )
    user_input.pull_config_input_object(config_input_object)
    filetypes = user_input.extract_filetypes_allowed_list_from_import_plugin()
    assert filetypes == ["csv", "gpx"]
