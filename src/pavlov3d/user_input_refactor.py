"""
Title: user_input.py (refactored)
Author: Clayton Bennett
Date: 02 Sep 2025

Purpose:
Drop-in replacement for messy plugin resolution and state handling.
Uses a priority-chain configuration model:
    1. Defaults
    2. Config file / config_input object
    3. Environment (optional, could be layered in)
    4. GUI overrides (dropdowns, manual input)
    5. Runtime adjustments (last overrides)
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from pavlov3d import filter_files as ff
from pavlov3d import environment
import src.pavlov3d.grouping_by_string
import src.pavlov3d.grouping_by_directory
import src.pavlov3d.config_input
from pavlov3d.directories import Directories


# -----------------------------
# Plugin Resolver
# -----------------------------
class PluginResolver:
    """Centralized logic for checking and resolving plugin references."""

    def __init__(self, style_object, interface_object=None):
        self.style_object = style_object
        self.interface_object = interface_object

    def normalize_plugins(self, plugins: Optional[List[str]]) -> List[str]:
        """Ensure all plugin references are normalized with proper prefix."""
        if plugins is None:
            return []
        normalized = []
        for plugin in plugins:
            if not plugin or plugin == "":
                continue
            if plugin.startswith("plugins."):
                normalized.append(plugin)
            elif plugin.startswith(("color_plugin_", "import_plugin_", "export_plugin_")):
                normalized.append("src.pavlov3d.plugins." + plugin)
            else:
                print(f"[PluginResolver] Unexpected plugin name: {plugin}")
                normalized.append(plugin)
        return normalized

    def resolve_single(self, plugin: Optional[str], dropdown: Optional[str], default: Any, dictionary: Dict[str, Any]) -> Any:
        """Resolve a single plugin from explicit string, dropdown, or default."""
        if not plugin:
            return dictionary.get(dropdown, default)
        if self._check_full_path(plugin) or self._check_plugin_in_dir(plugin):
            return plugin
        return dictionary.get(dropdown, default)

    def resolve_multiple(self, plugins: List[str], dropdown: Optional[str], default: Any, dictionary: Dict[str, Any]) -> List[Any]:
        """Resolve multiple plugin options, de-duped."""
        results = []
        for plugin in plugins:
            if not plugin:
                results.append(dictionary.get(dropdown, default))
            elif self._check_full_path(plugin) or self._check_plugin_in_dir(plugin):
                results.append(plugin)
            else:
                results.append(dictionary.get(dropdown, default))
        return self._dedupe(results) or [default]

    def _check_plugin_in_dir(self, plugin_filename: str) -> bool:
        if environment.pyinstaller():
            return True
        filename = plugin_filename if plugin_filename.endswith(".py") else plugin_filename + ".py"
        if filename.startswith("plugins."):
            filename = filename.replace("plugins.", "")
        plugins_directory = Path(Directories.get_core_dir()) / "plugins"
        py_files = [file for file in os.listdir(plugins_directory) if file.endswith(".py")]
        return filename in py_files

    @staticmethod
    def _check_full_path(filepath: str) -> bool:
        if not filepath.endswith(".py"):
            filepath += ".py"
        return os.path.isfile(os.path.normpath(filepath))

    @staticmethod
    def _dedupe(items: List[Any]) -> List[Any]:
        seen = []
        for x in items:
            if x not in seen:
                seen.append(x)
        return seen


# -----------------------------
# UserInput (backward-compatible)
# -----------------------------
class UserInput:
    gui_object = None
    style_object = None
    interface_object = None

    @classmethod
    def assign_interface_object(cls, interface_object):
        cls.interface_object = interface_object
        print("[UserInput] Interface object assigned")

    @classmethod
    def assign_style_object(cls, style_object):
        cls.style_object = style_object
        cls.scene_object = getattr(style_object, "scene_object", None)
        print("[UserInput] Style object assigned")

    def __init__(self):
        self.name = os.path.basename(__file__).removesuffix(".py")
        self.instance_name = "user_input_object"

        # -----------------------------
        # Core state (backward compatible)
        # -----------------------------
        self.filenames: List[str] = []
        self.filepaths: List[str] = []
        self.dict_groups_tiers: Dict[str, Any] = {}
        self.group_names: List[str] = []
        self.subgroup_names: List[str] = []
        self.stack_direction_list: List[str] = []

        # -----------------------------
        # Column / data mapping
        # -----------------------------
        self.column_time: Optional[str] = None
        self.column_height: Optional[str] = None
        self.column_depth: Optional[str] = None
        self.column_color: Optional[str] = None
        self.columns_metadata: List[str] = []
        self.data_start_idx: int = 0

        # -----------------------------
        # Plugin system
        # -----------------------------
        self.import_style_plugin: List[str] = []
        self.export_style_plugin: List[str] = []
        self.color_style_plugin: List[str] = []
        self.import_style_dropdown: Optional[List[str]] = None
        self.export_style_dropdown: Optional[List[str]] = None
        self.color_style_dropdown: Optional[List[str]] = None

        # Resolved plugin functions
        self.import_function = None
        self.export_function = None
        self.export_function_list: List[Any] = []
        self.color_function: List[Any] = []

        # Filetype / import options
        self.filetype_allowed_list: List[str] = []

        # Runtime options / flags
        self.keep_true_destroy_false_unassigned_curves: bool = False
        self.real_true_normalized_false_scale: bool = False

        # Plugin resolver
        self.resolver = PluginResolver(self.style_object, self.interface_object)

    def __str__(self):
        return self.name

    # -----------------------------
    # Config input mapping
    # -----------------------------
    def pull_config_input_object_(self, config_input_object):
        print("[UserInput] Pulling config_input_object")

        cij = getattr(config_input_object, "loaded_config", {})
        self.dict_config = dict(cij)

        # Grouping setup
        if getattr(config_input_object, "grouping_algorithm", None) != "group-by-directory":
            gj = getattr(config_input_object, "loaded_grouping", {"group_names": [], "subgroup_names": []})
            self.group_names = gj.get("group_names", [])
            self.subgroup_names = gj.get("subgroup_names", [])

        self.stack_direction_list = [
            cij.get('stack_direction_groups', ""),
            cij.get('stack_direction_subgroups', ""),
            cij.get('stack_direction_curves', ""),
        ]
        self.stack_direction_groups = cij['stack_direction_groups']
        self.stack_direction_subgroups = cij['stack_direction_subgroups']
        self.stack_direction_curves = cij['stack_direction_curves']

        # Plugins (always normalize to lists)
        self.import_style_plugin = cij.get("import_style_plugin", "").split(";")
        self.export_style_plugin = cij.get("export_style_plugin", "").split(";")
        self.color_style_plugin = cij.get("color_style_plugin", "").split(";")

        # Resolve file paths
        if getattr(self.scene_object, "request", None) and self.scene_object.request is not None:
            self.filenames = ff.snip_filenames_from_request_session(
                self.scene_object.request.session.get("list_csv_uploads", [])
            )
            self.filepaths = self.scene_object.request.session.get("list_csv_uploads", [])
        elif getattr(config_input_object, "grouping_algorithm", None) != "group-by-directory":
            self.filetype_allowed_list = self.extract_filetypes_allowed_list_from_import_plugin()
            self.filenames = ff.get_filelist_filetyped(self.filetype_allowed_list, Directories.get_import_dir())
            self.filepaths = [str(Directories.get_import_dir() / f) for f in self.filenames]

    def pull_config_input_object(self, config_input_object):
        print("[UserInput] Pulling config_input_object")
        cij = config_input_object.loaded_config
        self.dict_config = dict(cij)

        # Grouping setup
        if config_input_object.grouping_algorithm != "group-by-directory":
            gj = config_input_object.loaded_grouping
            self.group_names = gj.get("group_names", [])
            self.subgroup_names = gj.get("subgroup_names", [])

        self.stack_direction_list = [
            cij.get('stack_direction_groups'),
            cij.get('stack_direction_subgroups'),
            cij.get('stack_direction_curves'),
        ]

        # Plugins (always normalize to lists)
        self.import_style_plugin = cij.get("import_style_plugin", "").split(";")
        self.export_style_plugin = cij.get("export_style_plugin", "").split(";")
        self.color_style_plugin = cij.get("color_style_plugin", "").split(";")

        # Resolve file paths
        if getattr(self.scene_object, "request", None) is not None:
            self.filenames = ff.snip_filenames_from_request_session(
                self.scene_object.request.session["list_csv_uploads"]
            )
            self.filepaths = [
                str(Path(f)) for f in self.scene_object.request.session["list_csv_uploads"]
            ]
        elif config_input_object.grouping_algorithm != "group-by-directory":
            self.filetype_allowed_list = self.extract_filetypes_allowed_list_from_import_plugin()
            self.filenames = ff.get_filelist_filetyped(
                self.filetype_allowed_list, Directories.get_import_dir()
            )
            self.filepaths = [str(Directories.get_import_dir() / f) for f in self.filenames]

        # -----------------------------
        # Populate dict_groups_tiers depending on algorithm
        # -----------------------------
        if config_input_object.grouping_algorithm == "group-by-text":
            self.dict_groups_tiers = src.pavlov3d.grouping_by_string.define_groups(
                self.group_names, self.subgroup_names
            )
        elif config_input_object.grouping_algorithm == "group-by-directory":
            self.dict_groups_tiers = src.pavlov3d.grouping_by_directory.define_groups(
                loaded_grouping=config_input_object.loaded_grouping
            )
            print(f"[UserInput] dict_groups_tiers = {self.dict_groups_tiers}")
        else:
            print("[UserInput] Unknown grouping_algorithm; exiting")
            sys.exit()

    # -----------------------------
    # Plugin resolution
    # -----------------------------
    def determine_which_plugins_to_use(self, gui_mode=False):
        self.import_style_plugin = self.resolver.normalize_plugins(self.import_style_plugin)
        self.export_style_plugin = self.resolver.normalize_plugins(self.export_style_plugin)
        self.color_style_plugin = self.resolver.normalize_plugins(self.color_style_plugin)

        if gui_mode:
            self._check_plugins()

    def _check_plugins(self):
        self.import_function = self.resolver.resolve_single(
            plugin=self.import_style_plugin[0] if self.import_style_plugin else None,
            dropdown=(self.import_style_dropdown[0] if self.import_style_dropdown else None),
            default=getattr(self.style_object, "default_import_function", None),
            dictionary=getattr(self.interface_object, "import_style_dictionary", {}),
        )
        self.export_function = self.resolver.resolve_multiple(
            plugins=self.export_style_plugin,
            dropdown=(self.export_style_dropdown[0] if self.export_style_dropdown else None),
            default=getattr(self.style_object, "default_export_function", None),
            dictionary=getattr(self.interface_object, "export_style_dictionary", {}),
        )
        self.color_function = self.resolver.resolve_multiple(
            plugins=self.color_style_plugin,
            dropdown=(self.color_style_dropdown[0] if self.color_style_dropdown else None),
            default=getattr(self.style_object, "default_color_function", None),
            dictionary=getattr(self.interface_object, "color_style_dictionary", {}),
        )

    # -----------------------------
    # Helpers
    # -----------------------------
    def extract_filetypes_allowed_list_from_import_plugin(self):
        if not self.import_style_plugin:
            return []
        plugin = self.import_style_plugin[0]
        if not plugin.startswith("src.pavlov3d.plugins."):
            plugin = "src.pavlov3d.plugins." + plugin
        PluginClass = self.style_object.assign_plugin_dynamically(plugin)
        import_function_object = PluginClass()
        return getattr(import_function_object, "filetype_allowed_list", [])
