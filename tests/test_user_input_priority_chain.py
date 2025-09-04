# tests/test_user_input_priority_chain.py
import pytest
from types import SimpleNamespace
from pavlov3d.user_input import UserInput
from pavlov3d.directories import Directories


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
    
@pytest.fixture(autouse=True)
def mock_directories_paths(tmp_path, monkeypatch):
    # Mock project folder
    Directories.project = tmp_path
    (tmp_path / "plugins").mkdir(parents=True, exist_ok=True)
    
    # Patch get_core_dir to return the tmp_path
    monkeypatch.setattr(Directories, "get_core_dir", lambda cls=None: tmp_path)
    
    # Patch get_import_dir as well if tests pull files
    monkeypatch.setattr(
        Directories,
        "get_import_dir",
        lambda cls=None: tmp_path / "imports"
    )
    (tmp_path / "imports").mkdir(parents=True, exist_ok=True)

@pytest.fixture
def sample_cij():
    return {
    "import_style_plugin": "import_plugin_test",
    "export_style_plugin": "export_plugin_test1;export_plugin_test2",
    "color_style_plugin": "color_plugin_test",
    "stack_direction_groups": "group",
    "stack_direction_subgroups": "subgroup",
    "stack_direction_curves": "curve",
    "column_time": "time",
    "column_height": "height",
    "column_depth": "depth",
    "column_color": "color",
    "columns_metadata": "metadata",
    "data_start_idx": 0,
    "file_encoding": "utf-8"
}


@pytest.fixture
def user_input(mock_style_object, mock_interface_object):
    UserInput.assign_style_object(mock_style_object)
    UserInput.assign_interface_object(mock_interface_object)
    return UserInput()


#def test_priority_chain(user_input, sample_cij, mock_interface_object):
def test_priority_chain(user_input, sample_cij, mock_directories_paths):
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

    # Step 5: check that GUI dropdown override took precedence
    assert user_input.import_function == "import_from_dropdown"
    assert "export_from_dropdown" in user_input.export_function
    assert "color_from_dropdown" in user_input.color_function

    # Step 6: simulate runtime override (manual plugin assignment)
    user_input.import_style_dropdown = []  # clear GUI override
    user_input.import_style_plugin = ["import_plugin_runtime"]
    user_input.determine_which_plugins_to_use(gui_mode=False)

    assert user_input.import_function == "import_plugin_runtime"
    
    # Step 7: check that runtime override now took precedence
    assert user_input.import_function == "import_plugin_runtime"

