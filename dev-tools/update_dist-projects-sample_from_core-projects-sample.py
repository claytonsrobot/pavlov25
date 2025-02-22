'''
Author: Clayton Bennett with the assistance of Microsoft Co-Pilot
Generated: 17 February 2025
Purpose: Regularly update the sample direcotry from the core directory to the dist directory.

Details:
##Directories
- [[directories/inno\|inno]] is a directory which holds .iss scripts for running in Inno Installer to generate a Setup Installation Exectuable, referencing the contents of the [[directories/dist\|dist]] directory.
- The [[directories/dist\|dist]] directory holds the proper file strucuture to run the Pavlov3D CLI portable EXE. 
This portable EXE is generated by running pyinstaller on the [[directories/core\|core]] directory.
The setup EXE can be found in project-dir/inno/Outputs.

Into the [[directories/dist\|dist directory), a dev (Clayton) can or must manually place all necessary files and directories (other than the EXE file generated by Pyinstaller in the [[directories/dist\|dist]] directory in order for it to run properly. 
Inno will wrap everything in the [[directories/dist\|dist] directory as instructed by the .iss file. 
This additonal content includes the project directory, as it is seen in core. 
However, core has extra weight in it - what ships with the sample should be clean, and therefore requires manual oversigh rather than copying. 
There should be an easy way to update all config files (grouping, pointer files, toml, json, user input config) without carrying any export or excessive import files. 
Basically i need a script that will regularly update the sample direcotry from the core directory to the dist directory.
'''
import os
import shutil
from pathlib import Path

# Define the source and target directories
core_dir = Path("core")
dist_dir = Path("dist/sample")

# List of config files to update
config_files = [
    "config.toml",
    "config.json",
    "user_input_config.toml",
    "grouping.toml",
    "pointer_files.toml"
]

def update_sample_dir():
    # Ensure the target directory exists
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy each config file from core to dist
    for config_file in config_files:
        source_file = core_dir / config_file
        target_file = dist_dir / config_file
        
        if source_file.exists():
            shutil.copy2(source_file, target_file)
            print(f"Copied {source_file} to {target_file}")
        else:
            print(f"Warning: {source_file} does not exist")

if __name__ == "__main__":
    update_sample_dir()
