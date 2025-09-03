# tests/test_user_input_priority_chain.py
import pytest
from types import SimpleNamespace
from pavlov3d.user_input import UserInput


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


def test_priority_chain(user_input, sample_cij, mock_interface_object):
    # Step 1: load config
    config_input_object = SimpleNamespace(
        loaded_config=sample_cij,
        grouping_algorithm="group-by-text",
        loaded_grouping={"group_names": ["G1"], "subgroup_names": ["SG1"]},
    )
    user_input.pull_config_input_object(config_input_object)

    # Step 2: initially, plugins unresolved
    assert user_input.import_function is None
    assert user_input.export_function_list == []
    assert user_input.color_function == []

    # Step 3: simulate GUI dropdown override
    user_input.import_style_dropdown = ["dropdown_import"]
    user_input.export_style_dropdown = ["dropdown_export"]
    user_input.color_style_dropdown = ["dropdown_color"]

    # Step 4: determine plugins (GUI mode)
    user_input.determine_which_plugins_to_use(gui_mode=True)

    # Step 5: check GUI override took precedence
    assert user_input.import_function == "import_from_dropdown"
    assert "export_from_dropdown" in user_input.export_function
    assert "color_from_dropdown" in user_input.color_function

    # Step 6: simulate runtime override
    # e.g., manually replace import plugin at runtime
    user_input.import_style_plugin = ["import_plugin_runtime"]
    user_input.determine_which_plugins_to_use(gui_mode=False)

    # Check that runtime override took precedence (not GUI dropdown)
    assert user
