"""
Title: directories.py
Author: Clayton Bennett
Created: 29 January 2025
Updated: 02 Sep 2025

Purpose:
Centralized directory management for Pavlov3D projects.
Migrates away from environment.py for folder handling.
Implements pathlib.Path internally and returns Paths.

Example usage:
from pavlov3d.directories import Directories

Directories.initilize_program_dir()
Directories.initialize_startup_project()
import_dir = Directories.get_import_dir()  # returns Path object
"""

import os
import inspect
from pathlib import Path
from typing import Union
from pavlov3d import toml_utils
from pavlov3d import environment


class Directories:
    """Class for managing project directories and paths."""

    # Core directories
    root: Path = None
    core: Path = None
    project: Path = None

    # Optional subdirectories (legacy placeholders)
    configs: Path = None
    exports: Path = None
    imports: Path = None
    groupings: Path = None

    # -----------------------------
    # Setters
    # -----------------------------
    @classmethod
    def set_root_dir(cls, path: Union[str, Path]):
        """Set root directory of the project workspace."""
        cls.root = Path(path)
        print(f"[Directories] root set to: {cls.root}")

    @classmethod
    def set_core_dir(cls, path: Union[str, Path]):
        """Set core source directory (typically src/pavlov3d)."""
        cls.core = Path(path)
        print(f"[Directories] core set to: {cls.core}")

    @classmethod
    def set_project_dir(cls, path: Union[str, Path]):
        """
        Set project directory.
        Accepts full path or project name inside root/projects.
        """
        print(f"[Directories] set_project_dir called with: {path}")
        path = Path(path)

        if path.is_dir():
            cls.project = path
        else:
            relative_path = cls.get_root_dir() / "projects" / path
            print(f"[Directories] attempting relative path: {relative_path}")
            if relative_path.is_dir():
                cls.project = relative_path
            else:
                raise FileNotFoundError(f"Project directory not found: {path}")

        print(f"[Directories] Project directory set: {cls.project}")

    # -----------------------------
    # Getters (return Path objects)
    # -----------------------------
    @classmethod
    def get_root_dir(cls) -> Path:
        """Return root directory as Path."""
        return cls.root

    @classmethod
    def get_core_dir(cls) -> Path:
        """Return core directory as Path."""
        return cls.core

    @classmethod
    def get_program_dir(cls) -> Path:
        """Return core directory (alias)."""
        return cls.get_core_dir()

    @classmethod
    def get_project_dir(cls) -> Path:
        """Return project directory as Path."""
        return cls.project

    @classmethod
    def get_config_dir(cls) -> Path:
        """Return configs directory inside project."""
        return cls.project / "configs"

    @classmethod
    def get_export_dir(cls) -> Path:
        """Return exports directory inside project."""
        return cls.project / "exports"

    @classmethod
    def get_import_dir(cls) -> Path:
        """
        Return imports directory as Path.
        Handles local vs web (vercel) paths.
        """
        if environment.vercel():
            # web app blob storage
            print(f"environment.vercel() = {environment.vercel()}")
            folder = Path(cls.scene_object.blob_dir) / "csv_uploads_pavlovdata"
            return folder
        return cls.project / "imports"

    @classmethod
    def get_groupings_dir(cls) -> Path:
        """Return groupings directory inside configs."""
        return cls.get_config_dir() / "groupings"

    @classmethod
    def get_intermediate_group_structure_export_dir(cls) -> Path:
        """Return intermediate export folder path."""
        return cls.get_groupings_dir() / "intermediate_group_structure_export"

    @classmethod
    def get_group_by_directory_intermediate_export_json_filepath(cls) -> Path:
        return cls.get_intermediate_group_structure_export_dir() / "group_by_directory_intermediate_export.json"

    @classmethod
    def get_group_by_spreadsheet_intermediate_export_json_filepath(cls) -> Path:
        return cls.get_intermediate_group_structure_export_dir() / "group_by_spreadsheet_intermediate_export.json"

    @classmethod
    def get_group_by_text_intermediate_export_json_filepath(cls) -> Path:
        return cls.get_intermediate_group_structure_export_dir() / "group_by_text_intermediate_export.json"

    # -----------------------------
    # Initialization
    # -----------------------------
    @classmethod
    def initilize_program_dir(cls):
        """
        Set root and core directories based on current file location.
        Should be called at CLI or other entry points.
        """
        cls.set_root_dir(Path(inspect.getfile(inspect.currentframe())).resolve().parents[2])
        cls.set_core_dir(Path(inspect.getfile(inspect.currentframe())).resolve().parent)
        print(f"[Directories] core directory initialized: {cls.get_core_dir()}")

    @classmethod
    def initialize_startup_project(cls):
        """
        Load default project from TOML and set project directory.
        """
        print("[Directories] Initializing startup project")
        filename_default_project_entry = Path("./projects/default-project.toml")
        loaded_entry = toml_utils.load_toml(str(filename_default_project_entry))
        cls.set_project_dir(loaded_entry["project_directory"])

    # -----------------------------
    # Utility
    # -----------------------------
    @staticmethod
    def check_file(filepath: Union[str, Path]) -> Path:
        """Check if a file exists; raise SystemExit if not."""
        path = Path(filepath)
        if not path.is_file():
            print(f"[Directories] File does not exist: {path}")
            raise SystemExit
        return path

