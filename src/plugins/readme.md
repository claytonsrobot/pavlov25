There are three expected plugin file classes in this folder:
export_plugin_
color_plugin_
import_plugin_


There's not reason you cannot also have other style management plugins, like depth_plugin_ etc, for style things that need to be called.
The risk in this:
This is for algorithms that will reliably expand and change.
Halfwidth_time, for example, only has a few possible approaches, so this isn't the place for it.

Delete the outdated style exports once the plugin version have been fully integrated and are operational through testing.

16 Feb 2024: Add an import style


07 January 2025:
- filetype should be inherent (read explicity listed) in each import plugin. 