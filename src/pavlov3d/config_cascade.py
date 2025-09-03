"""
Title: config_cascade.py
Created: 2025-09-03
Author: Clayton Bennett
"""

import os
import json
import tomllib   # Python 3.11+. For 3.9/3.10, use `import toml`
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


# ------------------------
# Core Cascade Orchestrator
# ------------------------
class ConfigCascade:
    def __init__(self, defaults: Dict[str, Any]):
        self.defaults = defaults
        self.sources: List[Dict[str, Any]] = []

    def add_source(self, source: Dict[str, Any]):
        """Add a config layer. Later layers override earlier ones."""
        if source:
            self.sources.append(source)

    def resolve(self) -> Dict[str, Any]:
        """Merge defaults + all sources into one dictionary."""
        merged = dict(self.defaults)
        for source in self.sources:
            merged.update({k: v for k, v in source.items() if v is not None})
        return merged


# ------------------------
# File Config Source (JSON)
# ------------------------
class FileConfigSourceJSON:
    def __init__(self, filename: Path):
        self.filename = Path(filename)
        self.loaded: Optional[Dict[str, Any]] = None

    def load(self) -> Dict[str, Any]:
        if not self.filename.exists():
            return {}
        with open(self.filename, "r", encoding="utf-8") as f:
            self.loaded = json.load(f)
        return self.loaded

    def save(self, data: Dict[str, Any]):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


# ------------------------
# File Config Source (TOML)
# ------------------------
class FileConfigSourceTOML:
    def __init__(self, filename: Path):
        self.filename = Path(filename)
        self.loaded: Optional[Dict[str, Any]] = None

    def load(self) -> Dict[str, Any]:
        if not self.filename.exists():
            return {}
        with open(self.filename, "rb") as f:  # binary mode for tomllib
            self.loaded = tomllib.load(f)
        return self.loaded

    def save(self, data: Dict[str, Any]):
        # `tomllib` is read-only — for saving, you need `tomli-w` or `toml` package
        import tomli_w
        with open(self.filename, "wb") as f:
            tomli_w.dump(data, f)


# ------------------------
# GUI Config Source
# ------------------------
class GUIConfigSource:
    def __init__(self, gui_object):
        self.gui = gui_object

    def load_from_gui(self) -> Dict[str, Any]:
        """Pull current state from GUI controls."""
        return {key: widget.Get() for key, widget in self.gui.main_window.items()}

    def apply_to_gui(self, data: Dict[str, Any]):
        """Push state into GUI controls, where keys match."""
        for key, value in data.items():
            if key in self.gui.main_window:
                self.gui.main_window[key].update(value)

    def save_snapshot(self, filename: Path):
        """Save GUI state to JSON with metadata."""
        snapshot = self.load_from_gui()
        snapshot.update({
            "date": str(datetime.date.today()),
            "saved_by": "Clayton Bennett, probably"
        })
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=4)


# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    # Defaults
    defaults = {
        "project_id": "demo",
        "import_filetype_dropdown": "csv",
        "stack_direction_groups": "vertical"
    }

    cascade = ConfigCascade(defaults)

    # Load JSON config
    json_source = FileConfigSourceJSON("user_config.json")
    cascade.add_source(json_source.load())

    # Load TOML config
    toml_source = FileConfigSourceTOML("user_config.toml")
    cascade.add_source(toml_source.load())

    # Environment overrides
    env_overrides = {
        "project_id": os.getenv("PROJECT_ID"),
        "data_directory": os.getenv("DATA_DIR"),
    }
    cascade.add_source(env_overrides)

    # Final resolved state
    final_config = cascade.resolve()
    print("Resolved config:", final_config)
