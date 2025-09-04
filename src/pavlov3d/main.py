#! python3
'''
Title: main.py
Author: Clayton Bennett
Date Created: 22 February 2023
Date of servicable version: 12 June 2024
Date of notable version: 05 February 2025

Instructions:
Call and run Pavlov (FBX SDK version) to generate FBX files.
Open the exported FBX/GLB file in the CAD Assistant desktop program, from Open Cascase :)

Important knowledge:
BIN encoding allows conversion to .glb files, while ASCII encoding is user-readable.
An FBX file exported to BIN is ~30% larger than an ASCII,
but this doesn't matter once converted to GLB, those are the same size, about half of the FBX ASCII original.
Compressing FBX and GLB files reduces size to something like 15%, which is fantastic for email.
Blender import of published file takes a long time, how disappointing.

Futurework for this fork (FBX SDK) of Pavlov:
Add 3D pyplot preview.
Embed images ("videoclip textures" according to the Autodesk FBX SDK)
Run C++ FBX code.
Publish directly to GLB, possibly using Khronos or Microsoft tools.
Check out the Fabcebook FBX2GLB github page - it may be better than the Khronos/Blender file converter used here.
Look into assimp tools.
Animation - not supported by CAD Assistant unfortunately. So, if there was animation, how would we view it?

Future plans for Pavlov on the whole:
Then, full migration to three.js for .glb file generation in web.
I have not involved interpolation or any data compression, because it is not in keeping with the goal "preceding analysis visualization".
However, a specialized viewer/editor program in the future may be capable of hosting analysis functionality catered to certrain subject matters.

Framed comments:
15 October 2023: Recent success in establishing axes and ticks. The tick and axes line algorithm represents the groundwork for text annotation.
24 November 2023: Calculate curve_object_diameter after each relevant feature addition, outward growth.

Next:
Include label within radius - center on side. Same goes for any embedded jpg/png images.
Animation should be able to export. Passable to FBX, to Blender, to GLB.
Possibly organize models into a ring or ellipse, and have them each rotate while they also revolve.
Save these (ring vs diagonal) as different poses, somehow. Poses include alignment, like diagoal vs all in a row. Feasible?
In pygame preview, allow users to create additonal poses by dragging/moving each object.
Use metadata feature in OpenCascade CADAssistant.
Animation to call individual objects into tight collection vs dispersed/exploded view.
Animation to go to one of 3 bins.
Swap bottom view to top view. Change fence side and direction facing of labels. Change plotting orientation? ugh, my heart.
In JSON config file, allow for: "column_height":"1:5","column_depth":"6:10",

Assumptions:
Data orgin of a group is coincident with the data origin of its first child.
'''

#import numpy as np
import os
import time
import copy
import pprint
#import uniqueUnixFilename

from pavlov3d.scene import Scene
from pavlov3d.style import Style
from pavlov3d.import_lib import ImportLib
from pavlov3d.scale import Scale, MultipleAxesScalingAlgorithm 
#from converter import converter as Convert
from pavlov3d.preview import Preview as Preview

from pavlov3d import pngMaker
from pavlov3d import messaging
from pavlov3d.config_input import ConfigInput
from pavlov3d.config_manager import ConfigManager, get_gui_export_overrides

from pavlov3d.user_input import UserInput
from pavlov3d.datapoint import DataPoint
from pavlov3d.curve import Curve

from pavlov3d.ticks import Ticks
from pavlov3d.fences import Fences 
from pavlov3d.hierarchy import Hierarchy
from pavlov3d.text_translation import TextTranslationIntermediate

from pavlov3d import translation
from pavlov3d import environment
from pavlov3d.directories import Directories
if environment.vercel():
    from pavlov3d import vercel_blob

def main():
    request = None  # django artifact
    print('Running main .....')
    global scene_object
    scene_object, style_object, hierarchy_object = set_up(request)
    
    config_input_object,user_input_object = \
        get_configuration(scene_object, style_object)

    interface_object = determine_interface(style_object,config_input_object,user_input_object)

    run_interface(style_object,interface_object,user_input_object,config_input_object)

    if config_input_object.grouping_algorithm == "group-by-text" or (None is None):
        build_grouping(hierarchy_object,user_input_object,loaded_grouping = config_input_object.loaded_grouping)
    
    export_control_object = import_data(scene_object,style_object,user_input_object,hierarchy_object)
                                        
    png_preview(scene_object,user_input_object,export_control_object)
                  
    build_point_cloud(scene_object,style_object,user_input_object,hierarchy_object)
    if False: 
        preview_scene(scene_object)

    createFBX_object = generate_export(scene_object,style_object,export_control_object)

    return scene_object, hierarchy_object, createFBX_object

def set_up(request):
    '''0) Set up program'''
    # what is request? It is part of the django implementation, in the views.py file
    # filepath = request.session["current_fbx_export"] ; this is expected in prepare export director, using session variable
    # Change this to a commonly used run time counter. Do not use time.time

    scene_object = Scene()
    style_object = Style()
    scene_object.assign_style_object(style_object) # cls
    style_object.assign_scene_object(scene_object) # cls 
    scene_object.assign_program_start_timestamp(time.time())
    scene_object.assign_request(request) # cls

    Hierarchy.assign_scene_object(scene_object)
    hierarchy_object = Hierarchy() # instance
    scene_object.assign_hierarchy_object(hierarchy_object)
    style_object.assign_hierarchy_object(hierarchy_object)
    DataPoint.assign_style_object(style_object)
    DataPoint.assign_text_string("this is the same DataPoint class")
    prepare_export_filepath(scene_object,request)

    return scene_object, style_object, hierarchy_object

def get_configuration(scene_object, style_object):
    '''1) Run GUI, select data'''

    # check if do not have pysimplegui, take default inputs (from config or from gui default) and skip GUI 
    config_input_object = ConfigInput()
    config_input_object.assign_scene_object(scene_object) # cls
    scene_object.assign_config_input_object(config_input_object) # cls
    loaded_config, loaded_grouping = config_input_object.define_and_load_default_config_input()

    
    #user_input_object = user_input_class()
    user_input_object = UserInput()
    user_input_object.assign_style_object(style_object) # cls

    scene_object.assign_user_input_object(user_input_object) # cls
    style_object.assign_user_input_object(user_input_object) # cls
    scene_object.hierarchy_object.assign_user_input_object(user_input_object)
    
    return config_input_object,user_input_object

def determine_interface(style_object,config_input_object,user_input_object):
    #interface_list = ['json','gui_simple','gui_developer','control_cli']

    if style_object.interface_choice == 'gui_simple' or style_object.interface_choice == 'gui_developer':
    #if style_object.use_GUI is True:
        #if style_object.developer_mode_gui is True:
        if style_object.interface_choice == 'gui_developer':
            from pavlov3d.gui import Gui
        #else:
        elif style_object.interface_choice == 'gui_simple':
            from pavlov3d.gui_simple import Gui
        print('gui_object load\n')
        gui_object = Gui()        
        control_cli_object = None
        interface_object = copy.copy(gui_object)
        
    elif style_object.interface_choice == 'control_cli':
        from control_cli import ControlCLI
        control_cli_object = ControlCLI()
        gui_object = None
        interface_object = copy.copy(control_cli_object)
        
    elif style_object.interface_choice == 'json':
        control_cli_object = None
        gui_object = None
        interface_object = None
        
    else:
        control_cli_object = None
        gui_object = None
        interface_object = None

    return interface_object #gui_object, control_cli_object

def run_interface(style_object,interface_object,user_input_object,config_input_object):
    # i nede the top CLI to call a different CLI,
    # which can also be called here, without routing to the top cli with a circular reference
        
    #user_input_object = gui_object.run_and_get_inputs()# user_input_object instantiated inside
    if not(interface_object is None):
        interface_object.assign_style_object(style_object) 
        interface_object.assign_config_input_object(config_input_object)
        interface_object.assign_user_input_object(user_input_object)
        user_input_object.assign_interface_object(interface_object) # revers this: user input comes first
        interface_object.run_and_get_inputs()# user_input_object instantiated inside
    else:
        user_input_object.pull_config_input_object(config_input_object) # direct pull, no interface

def build_grouping(hierarchy_object,user_input_object,loaded_grouping):
    print("main.build_grouping(hierarchy_object,user_input_object,loaded_grouping)")
    hierarchy_object.cycle_through_filenames_intialize_curves() # curve initialization
    hierarchy_object.build_tiers_and_groups_objects(user_input_object,loaded_grouping)

# -----------------------------
# import_data orchestrator
# -----------------------------
def import_data(scene_object, style_object, user_input_object, hierarchy_object):
    user_input_object.determine_which_plugins_to_use()  # toggle
    
    importer = _run_import(scene_object, style_object, user_input_object)
    _normalize(hierarchy_object, style_object)
    _populate_scene(scene_object, importer)
    export_control = _prepare_exports(scene_object, style_object, user_input_object)
    
    return export_control

def _run_import(scene_object, style_object, user_input_object):
    import_function_object = load_import_plugin_object(
        scene_object, style_object, user_input_object
    )

    print("Begin import...")
    import_function_object.run_import()
    print("Import complete.")

    return import_function_object

def _normalize(hierarchy_object, style_object):
    print("hierarchy_object.dict_curve_objects_all.values()")
    MultipleAxesScalingAlgorithm.normalize_all_curve_objects(
        set(hierarchy_object.dict_curve_objects_all.values())
    )
    style_object.calculate_halfwidths_and_directions()
    # yes scale should be after import and before passing values to scene_object 
    # no, boooo, do it before assignment to curve objects and datapoints
    # well, should the datapoints know their unscaled values? i suppose they would have to for proper labeling.....hmmmm.
    # yes, datapoints should know their unscaled values, for labeling
    # but, curve objects should only know their scaled values, for layout and spacing

def _populate_scene(scene_object, importer):
    scene_object.populate_basic_data(
        importer.names,
        importer.vectorArray_time,
        importer.vectorArray_height,
        importer.vectorArray_depth,
        importer.headers_time,
        importer.headers_height,
        importer.headers_depth,
    )

    # Optional: halfwidths & directions were commented out in original
    # scene_object.populate_halfwidth_data(...)
    # scene_object.populate_direction_data(...)
    """
    scene_object.populate_halfwidth_data(\
            import_function_object.vectorArray_halfwidth_time,
            import_function_object.vectorArray_halfwidth_height,
            import_function_object.vectorArray_halfwidth_depth,
            import_function_object.average_halfwidth_time,
            import_function_object.average_halfwidth_height,
            import_function_object.average_halfwidth_depth)
    
    scene_object.populate_direction_data(\
            import_function_object.vectorArray_direction)
    """
    messaging.print_data_range(scene_object)

def _prepare_exports(scene_object, style_object, user_input_object):
    export_plugin_list = style_object.prepare_export_modules()
    export_control_object = export_plugin_list[0]  # for text angling only

    ###user_input_object.pull_values_from_export_control_object(export_control_object)


    # -----------------------------
    # Modern replacement for old pull_values_from_export_control_object
    # -----------------------------
    cm = ConfigManager()
    gui_overrides = get_gui_export_overrides(user_input_object)
    merged_config = cm.pull_values(export_control_object, gui_overrides)
    # Now merged_config is a validated ExportConfig instance

    # If user_input_object still needs attributes, optionally cast:
    user_input_object.config = merged_config
    
    if hasattr(merged_config, "model_dump"):         # Pydantic v2
        items = merged_config.model_dump().items()
    else:                                            # Pydantic v1
        items = merged_config.dict().items()

    for key, value in items:
        setattr(user_input_object, key, value)


    TextTranslationIntermediate.assign_style_object(style_object)
    TextTranslationIntermediate.prepare_text()

    export_control_object.export_name = scene_object.filename_FBX
    return export_control_object



def load_import_plugin_object(scene_object,style_object,user_input_object):
    print("main.load_import_plugin_object()")
    import_lib_object = ImportLib()
    import_function_object = style_object.prepare_import_module() # set user_input_object.import_style
    import_function_object.assign_scene_object_etc(scene_object)
    import_function_object.assign_user_input_object(user_input_object)
    import_function_object.assign_import_lib_object(import_lib_object)
    import_function_object.assign_config_input_object(scene_object.config_input_object)

    import_function_object.pass_in_DataPoint_class(DataPoint)
    Curve.pass_in_scene_object(scene_object)
    import_function_object.pass_in_Curve_class(Curve)
    return import_function_object

def prepare_export_filepath(scene_object,request):
    '''
    1c) Prepare temp directory and export filename
    '''
    if request != None:
        #filepath = request.session["current_fbx_export"] # the filename wil be chopped off - this is just to get the 
        export_dir = os.path.dirname(request.session["current_fbx_export"]) # the filename wil be chopped off - this is just to get the 
        
    else: # for running cli.py locally
        export_dir = Directories.get_project_dir() / "exports"

    scene_object.exportdir = export_dir
    scene_object.filename_FBX = 'pavlov_'+str(int(scene_object.unix_start)) +'.fbx'
    scene_object.filepath = scene_object.exportdir / scene_object.filename_FBX
    return None

def png_preview(scene_object,user_input_object,export_control_object):

    '''
    3) Plot preview
    '''
    if user_input_object.pngShow or user_input_object.pngExport:
        pngMaker.preview(scene_object,
                         user_input_object.pngShow,
                         user_input_object.pngExport,
                         scene_object.export_name)

def build_point_cloud(scene_object,style_object,user_input_object,hierarchy_object):

    construct_heirarchy(scene_object,style_object,user_input_object,hierarchy_object)
    #print("SUCCESS A:construct_heirarchy")
    build_ticks(scene_object,style_object)
    #print("SUCCESS B:build_ticks")
    build_texts(scene_object,style_object)
    #print("SUCCESS C:build_texts")
    layout_spatial(scene_object,style_object,hierarchy_object)
    #print("SUCCESS D:layout_spatial")
    build_fences(scene_object)
    #print("SUCCESS E:build_fences")

    return True
def construct_heirarchy(scene_object,style_object,user_input_object,hierarchy_object):
    
    # hierarchy_object.build_tiers_and_groups_objects(user_input_object) # i moved this higher becuase group membership is needed for something in the axes_labels_machine or the title_machine
    # Group hierarchy and membership is established, based on gui values for groups and subgroups        
    
    # 30 January 2025, something is happening out of order here
    
    hierarchy_object.apply_curve_object_spans()
    hierarchy_object.apply_group_object_spans() # failuremode: group_object.span_relative_to_self_data_origin, the tier 2 group "December" has this attribue, while the tier 1 attribute "Maxson" does not
    hierarchy_object.group_padding_assignment()
    hierarchy_object.step_through_hierarchy_bottom_up(hierarchy_object.determine_characteristic_length_for_group) # is this working?

    style_object.prepare_curve_and_group_elements_from_export_style(user_input_object.export_function) # needs characteristic length
    ######
    return True
    
def build_ticks(scene_object,style_object):
    '''
    5) Create axes_arrays
    '''
    ticks_object = Ticks()
    ticks_object.assign_scene_object(scene_object)
    if style_object.consistent_tick_size is True:
        tick_size = ticks_object.determine_consistent_tick_size()
        style_object.tick_size = tick_size
        ticks_object.generate_consistent_ticks(tick_size)
        style_object.use_consistent_tick_size_as_consistent_padding(2*tick_size)
    else:
        ticks_object.generate_ticks() # totally chuck this? not now, don't over optimize quite yet. But yes, excess code is a problem. We probably don't need this. cull later.

    return True
    '''
    () texts_arrays
    Done after object translation / origin assignment
    Group and subgroup labels (and fencelines) will not fit into the len(vectorArray_time) paradigm
    '''


def build_texts(scene_object, style_object):
    # group_label_machine was shoved into translation.py, look at changing that, CB 2 Feb 2025 
    from pavlov3d.axes_labels_machine import AxesLabelsMachine # axisLabel is imported into axesLabels
    from pavlov3d.title_machine import TitleMachine
    from pavlov3d.tick_numbering_machine import TickNumberingMachine

    # title has to go first, to sus out proper sizing.
          
    curve_title_machine = TitleMachine()
    curve_title_machine.assign_scene_object_etc(scene_object)
    text_height_minimum = curve_title_machine.determine_best_text_height()
    curve_title_machine.generate_title_for_each_curve(text_height_minimum)

    axes_labels_machine = AxesLabelsMachine()
    axes_labels_machine.assign_scene_object_etc(scene_object)
    axes_text_height_minimum = axes_labels_machine.determine_best_text_height()
    if style_object.include_curve_object_axis_labels == True:
        axes_labels_machine.generate_axes_labels_for_each_curve()    

    tick_numbering_machine = TickNumberingMachine()
    tick_numbering_machine.assign_scene_object_etc(scene_object)
    #tick_numbering_machine.generate_tick_numbering_for_the_highest_value_on_all_three_axes_for_curves_with_a_max_dimension()
    tick_numbering_machine.generate_tick_numbering_for_all_curves()


    for curve_object in scene_object.hierarchy_object.dict_curve_objects_all.values():
        curve_object.calculate_span_10April24()

    #for group_object in scene_object.hierarchy_object.dict_group_objects_most.values():
    #    group_object.calculate_span_12April24()
    #    print('main: is this the right spot to bottom-up calculate  group spans?')
    #    # you cannot call this here, because the span of a group must respect stacking
    #    # translation.calculate_spans_bottom_up() is the right place
    #   really, the money is in how group diameter is calculated

    return True

def layout_spatial(scene_object, style_object,hierarchy_object):
    '''
    4) Organize the scene
    Scene, groups, curve_objects
    Group labels and fences
    '''

    color_function_list = style_object.prepare_color_modules()
    print(f"color_function_list check = {color_function_list}")
    style_object.set_color_function_list(color_function_list)
    export_function_list = style_object.prepare_export_modules()
    style_object.set_export_function_list(export_function_list)
    print("\ntranslation.calculate_placement_bottom_up()")
    hierarchy_object.step_through_hierarchy_bottom_up(translation.calculate_placement_bottom_up) # ERROR 30January2025, #failuremode: ?
    print("\ntranslation.calculate_span_relative_to_scene_minimum_edge_at_zero_height_plane_top_down()")
    hierarchy_object.step_through_hierarchy_top_down(translation.calculate_span_relative_to_scene_minimum_edge_at_zero_height_plane_top_down)

    return True

def build_fences(scene_object):
    '''
    6++) groups fence lines arrays
    '''
    fences_object = Fences()
    fences_object.assign_scene_object_etc(scene_object)  
    fences_object.generate_fences()
    return True

def preview_scene3D(scene_object):
    '''
    7) Pyplot/pygame preview should go here
    '''
    preview_object = Preview()
    preview_object.assign_scene_object_etc(scene_object)
    #preview_object.build()
    #preview_object.show()
    if True:
        preview_object.preview_scene3D(scene_object)

def preview_curve3D(scene_object):
    preview_object = Preview()
    preview_object.assign_scene_object_etc(scene_object)
    if True:
        preview_object.preview_curve(scene_object)

def generate_export(scene_object,style_object,export_control_object):
    '''
    8) FBX Generate
    '''
    if True:
        
        createFBX_object = \
                     style_object.prepare_publishing_module(\
                        export_control_object,
                        )# return the createFBX instance # this should take custom script names (full or single) and known style keys, 
        # A scripter/dev could input a different plugin name, into style_object.prepare_export_module(), to control the export without assignment in the gui

        unix_mark = time.time()
        mark_time = round(unix_mark-scene_object.unix_start,2)
        print("Creating FBX export file ... mark",mark_time,"sec")
        createFBX_object.generate_model()
        createFBX_object.lSdkManager.Destroy() # memory management, this was on;y passed up to troubleshoot variables from the command window
        if environment.vercel():
            #scene_object.filesize_FBX = round(os.path.getsize(scene_object.filepath)/(1024),3)
            pass
        elif environment.pyinstaller():
            scene_object.filesize_FBX = round(os.path.getsize(scene_object.filepath)/(1024),3)
        else:
            scene_object.filesize_FBX = round(os.path.getsize(scene_object.filepath)/(1024),3)
            pass
            #scene_object.filesize_FBX = vercel_blob.head(scene_object.filesize_FBX, options={'token': os.environ.get('BLOB_READ_WRITE_TOKEN')})["size"]
        print("Export: ", scene_object.filename_FBX,",",scene_object.filesize_FBX,"KB")
        '''
        9) Convert file, using Blender converter. Try the Facebook conversion.
        '''
        if False:
            converter_object = Convert()
            converter_object.assign_scene_object_etc(scene_object)
            converter_object.check_request_and_do()

    '''
    8b) DXF generate
    '''
    #from createDXF_ import CreateDXF
    #createDXF_object = CreateDXF()
    unix_mark = time.time()
    mark_time = round(unix_mark-scene_object.unix_start,2)
    print("Total time:",    mark_time, "sec")
    return createFBX_object



if __name__ == "__main__":
    #global scene_object # redundantly called in main()
    Directories.initilize_program_dir()
    main()



