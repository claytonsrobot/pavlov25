'''
Title: CLI.py
Created: 21 May 2024
Author: Clayton Bennett

Purpose: 
Drive Pavlov from the command line. Choose options using command inputs and by editing json configuration files.
It might be good to have one config file driving the others?

Resources: 
https://medium.com/@noransaber685/simple-guide-to-creating-a-command-line-interface-cli-in-python-c2de7b8f5e05
'''
import cmd2
import os
from pprint import pprint
import main
from hidden_prints import HiddenPrints
import time
from datetime import datetime
#import subprocess
from sparklines import sparklines
import gui_customtk_basic
from filemanagement import DirectoryControl
import filemanagement as fm
import environmental
import copy

from directories import Directories
try:
    import psutil # overkill
except:
    pass
import json_handler # pleae migrate the json-handler.py

    
class PavlovCLI(cmd2.Cmd):
    pavlov3d_prettyprint =  """
     ____             _            _____ ____
    |  _ \ __ ___   _| | _____   _|___ /|  _ \\
    | |_) / _` \ \ / / |/ _ \ \ / / |_ \| | | |
    |  __/ (_| |\ V /| | (_) \ V / ___) | |_| |
    |_|   \__,_| \_/ |_|\___/ \_/ |____/|____/

    """
    topography = "▅▃▂▅▆▆▆▆▆▆▄▂▂▃▄▆▅▃▂▁▂▃▅▆▆▅▃▂▅▆▆▆▆▆▆▄▂▂▃▄▆▅▃▂▁"
    prompt = '>> '
    intro = pavlov3d_prettyprint + \
    '''
    
    Welcome to the Pavlov 3D CLI. 
    Type "help" or "h" to see available commands. 
    Type "instructions" or "i" to see a description of workflow.
    Type "gui" or "g" to launch the Graphical User Interface.
    '''

    scene_object = None
    style_object = None
    config_input_object = None
    user_input_object = None
    export_control_object = None
    pointcloud_bool = None
    createFBX_object = None
    export_object = None
    verbose = False

    project_active = None
    last_export_path = None
    all_export_paths = []


    name = "Pavlov3D Command Line Interface"
    def get_version():
        # for later on storing automatically, not worth the squeeze rn
        version = "Version: 2025-02February-05" # manually updated
        return version
    version = get_version()
    
    
    @classmethod
    def initialize_scene_object(cls):
        cls.scene_object = None
    @classmethod
    def link_initial_project_directory(cls):
        #cls.project_active = None
        Directories.set_project_dir(Directories.get_core_dir()+r"/projects/default-sample/")
        print(f"project_active = {Directories.get_project_dir()}")
        # dynamic, points to default-project.json file
        #cls.set_project_active(cls.get_startup_project("./projects/default-project.json")) # pull from config file
        Directories.initialize_startup_project() # pull from config file
    
    @classmethod
    def set_project_active(cls,project_dir):
        #cls.project_active = project_dir
        Directories.set_project_dir(project_dir)
        #print(f"Directories.get_project_dir() = {Directories.get_project_dir()}")
    
    @classmethod
    def get_project_active(cls):
        return Directories.get_project_dir()

    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug = True  # Set the default debug value to True
    """
        #self.name = os.path.basename(__file__).removesuffix('.py')
        self.scene_object = None
        self.style_object = None
        self.config_input_object = None
        self.user_input_object = None
        self.export_control_object = None
    """
        
    def run(self):
        #self.scene_object = None
        self.initialize_scene_object()
        #self.link_initial_project_directory()
        Directories.initialize_startup_project()
        
        self.cmdloop()

    def do_status(self,line):
        "Get a rough idea of what the program has done so far."
        print(f"""\
        Exist:
        scene_object: {self.scene_object != None} :: 1
        style_object: {self.style_object != None} :: 1
        config_input_object: {self.config_input_object != None} :: 2
        user_input_object: {self.user_input_object != None} :: 2
        export_control_object: {self.export_control_object != None} :: 4
        pointcloud_bool: {self.pointcloud_bool != None} :: 5
        createFBX_object: {self.createFBX_object != None} :: 6
        """)

    def do_example(self, line):
        "Show example image of a model."
        pass

    def do_m(self,line):
        """
        Abbreviation for make.
        Examples:
            m scene
            m config
        """
        self.do_make(line)

    def do_make(self,line):
        "The bread and butter. Hint: make scene, or, m scene."
        if line == "scene":
            self.make_scene(None)
        elif line == "config":
            self.makeconfig(None)
        elif line == "skipinterface":
            self.do_skipinterface(None)
        elif line == "data":
            self.import_data(None)
        elif line == "pointcloud":
            self.build_pointcloud(None)
        elif line == "export":
            self.do_export("fbx")
        elif line == "all":
            self.do_main(None)
        elif line =="":
            print("""
            Make what? 
            
            Proper usage examples: 
                make scene
                make config
                make skipinterface
                make data
                make pointcloud
                make export
                  
            "make all" is the same as running "main"
            """) 
        else:
            print(f"*** Unknown syntax: {line}")

    def do_launch(self,line):
        "Futurework. Inteded to use for launching various GUI options. It would be better to just call gui."
        pass

    def do_h(self,line):
        """
        Abbreviation for help.
        Example: h
        """
        self.do_help(line)

    def do_i(self,line):
        """
        Abbreviation for instructions.
        Example: i
        """
        self.do_instructions(line)
        
    def do_instructions(self,line):
        """run 'instructons' to see step-by-step instructions for more control
        Options: basic, b, advanced, adv, a, viewer, view, v")
        Examples:
            i a
            i
            instructions
            i basic
            i adv
        """
        ex = \
        '''
        Options: basic, b, advanced, adv, a, viewer, view, v")
        Examples:
            i a
            i
            instructions
            i basic
            i adv
        '''
        basic =\
        '''
        Basic:
            Run {"main"} to run the program, 
            from beginning to end, with default settings.
            
            The program inputs will be based 
            on the JSON configuration file that 
            is identified in config_entry.json, 
            in the config_input_filename variable.
            Use command "where" to see the program directory.
        '''
        advanced = \
        '''
        Advanced:
            Instead of running "main", you can instead run these commands, in this order:
            1. "make scene"
            2. "make config"
            3. "skipinterface"
            4. "import data"
            5. "make pointcloud"
            6. "make model"
 
        Advanced Numeric:
            Run the only numbers from the Advanced commands.
            Example: "1"
            You can run the program by running 1, 2, 3, 4, 5, 6 separately and in succession.
        '''
        speedrun =\
        '''
        Speedrun (without print statements):
            A. "prep": same as (1) make scene and (2) make config
            B. "no": same as (3) skipinterface
            C. "go": same as (4) make data, (5) make pointcloud, and (6) make export
        '''
        
        if line == "" or line ==None:
            #print(ex)
            print(basic)
            print(advanced)
            #print(speedrun)
            self.do_viewer(None)
        elif line =="basic" or line =="b":
            #print(ex)
            print(basic)
        elif line =="advanced" or line =="adv" or line =="a":
            #print(ex)
            print(advanced)
        elif line =="speedrun" or line =="speed" or line =="s":
            #print(ex)
            print(speedrun)
        elif line == "viewer" or line == "view" or line == "v":
            self.do_viewer(None)

    def do_viewer(self,line):
        view =\
        '''
        To open FBX models generated by Pavlov 3D as they are intended, 
        download and install CAD Assistant by Open Cascade.
        https://www.opencascade.com/products/cad-assistant/
        '''
        print(view)
        
    def do_where(self,line):
        "Print working directory location. This is where import and export files are managed." 
        try:

            print(f"Working directory: {Directories.get_program_dir()}")
            
        except Exception as e: 
            print("Scene not yet created. Run (1) make scene.")
        dev_location = "Pavlov 3D was proudly developed in:\nThe United States, New Zealand, Thailand, Laos, Vietnam, Australia, & Japan."
        print(dev_location)

    def do_when(self,line):
        """
        Print unix time, which represent the time when the scene was generation, via make scene. 
        """
        try:
            time_start = str(datetime.fromtimestamp(float(self.scene_object.unix_start)))
            #print(f"self.scene_object.unix_start = {self.scene_object.unix_start}")
            print(f"Unix time at scene creation: {self.scene_object.unix_start}")
            print(f"Date time at scene creation: {time_start}")
            

            #datetime.fromtimestamp(float(line))
            
        except Exception as e: 
            print("Scene not yet created. Run (1) make scene.")
        print(f"Date time now: {str(datetime.fromtimestamp(float(int(time.time()))))}")
    def do_who(self,line):
        "Who created this?"
        
        #whoami = subprocess.run(["whoami"], capture_output = True, text = True)
        #print(f"whoami: {whoami.stdout.strip()}")
        
        shortcredit = "Clayton Bennett, 2022-2025.\nPavlov Software & Services LLC, incorportated 2023."
        print(shortcredit)

    def do_test(self,line):
        "See CPU frequency."
        try:
            cpu_freq = psutil.cpu_freq()
            print("Current CPU Frequency:", round(cpu_freq.current),"hz, or so.") 
        except:
            pass
    def do_why(self,line):
        "Why use Pavlov?"
        why = "Visualize lots of raw data. Ideal for first-year graduate students after they finish their experiements. See all of your data, everything at once to reveal untold truths." 
        print(f"{why}")

    def do_how(self,line):
        "Prints instructions"
        self.do_instructions(None)

    def do_what(self,line):
        "What?"
        self.pretty_title(None)
    def do_v(self,line):
        "Abbreviation for version"
        self.do_version(None)
    def do_version(self,line):
        "See version."
        print(self.name)
        print(self.version)
        
    def do_about(self,line):
        "A foolish consistency is the hobgoblin of little minds."
        self.pretty_title(None)
        self.do_version(None)

    def do_futurework(self,line):
        "See futurework."
        fw = """
        Project generation and motion between projects
        PDF guide to onfiguration and workflow, and CLI commands
        Group naming problems - no groups should be required.
        Multiple column assignment. example - column_height: "1:4"  
"        Generate .blend file
        Generate threejs model
        Generate GIS model
        Generate .fig for Matlab
        Improve main.prepare_export_directory() to include selection.
        Move Group Title to bottom, (for easier rotation and finding)
        """
        print(fw)

    def do_1(self,line):
        "make scene"
        self.make_scene(None)
    def do_2(self,line):
        "make config"
        self.makeconfig(None)
    def do_3(self,line):
        "skipinterface"
        self.do_skipinterface(None)
    def do_4(self,line):
        "import data, or, make data"
        self.import_data(None)
    def do_5(self,line):
        "make pointcloud, or, build_pointcoud"
        self.build_pointcloud(None)
    def do_6(self,line):
        "export or make export"
        self.do_export("fbx")

    def do_main(self,line):
        "main will run Pavlov with current config_input and config_settings values"
        #print('Warning: main should be converted to a class - now it runs on import')
        print('Running Pavlov....')
        print('Have fun, and may the odds be ever in your favor.')
        #global scene_object
        self.scene_object, self.hierarchy_object, self.createFBX_object = main.main()
        #self.hierarchy_object = copy.deepcopy(self.scene_object.hierarchy_object)
        self.record_export_path()

        #self.scene_object = scene_object

        #self.curve_object = self.hierarchy_object.dict_curve_objects_all[list(self.hierarchy_object.dict_curve_objects_all.keys())[0]]
        #return scene_object
    
    def do_wipe(self,line):
        """
        Resets the session. Arguments are not accepted. 
        Example: wipe
        """
        if line == "":
            self.scene_object,self.style_object,self.hierarchy_object = None,None,None
            self.config_input_object,self.user_input_object = None,None
            self.export_control_object = None
            self.pointcloud_bool = None
            self.createFBX_object = None
            self.exportPNG_object = None
            self.do_status(None)
        else:
            msg=\
        """
        wipe does not accept arguments.
        wipe is meant to reset the session. 
        """
            print(msg)      

    def make_scene(self,line):
        "Instead of running main.main(), independantly make the scene."
        #global scene_object
        request = None
        scene_object,style_object,hierarchy_object = main.set_up(request)
        self.scene_object,self.style_object,self.hierarchy_object = scene_object,style_object,hierarchy_object
        #scene_object = self.scene_object
        print('Built: scene, style, hierarchy')
        print("Hint: Next: (2) make config")


    def makeconfig(self,line):
        "Independantly generate config_input_object & user_input_object"
        try:
            self.config_input_object,self.user_input_object = \
                main.get_configuration(self.scene_object,
                                    self.style_object)
            print("make config, done")
        except Exception as e:
            # if user did not make scene first, that's okay, do it automatially
            self.make_scene(None)
            self.makeconfig(None)
        print("Hint: Next: (3) skipinterface")


    def do_s(self,line):
        "Shorthand for see. Example: s scene"
        self.do_see(line)

    def do_see(self,line):
        """
        See certain dictionaries.

        Examples:
            see scene
            see style
            see config
            see userinput
            see hierarchy
            see exportcontrol
            see createFBX
            s c
            s u
            s h
            s ec
            s sc
            s st
            
        'see scene' is the same as 'eval scene_object -d' 
        """ 
        try:
            if line=="config" or line=="c":
                print(f"config_input_object = ")
                pprint(self.config_input_object.__dict__)
            elif line=="userinput" or line=="u":
                print(f"user_input_object = ")
                pprint(self.user_input_object.__dict__)
            elif line=="scene" or line=="sc" or line=="s":
                print(f"scene_object = ")
                pprint(self.scene_object.__dict__)
            elif line=="style" or line=="st":
                print(f"style_object = ")
                pprint(self.style_object.__dict__)
            elif line=="hiearchy" or line=="h":
                print(f"hierarchy_object = ")
                pprint(self.hierarchy_object.__dict__)
            elif line=="exportcontrol" or line=="ec":
                print(f"export_control_object = ")
                pprint(self.export_control_object.__dict__)
            elif line=="createFBX":
                print(f"createFBX_object = ")
                pprint(self.createFBX_object.__dict__)
            elif line == "":
                self.do_help("see")
            else:
                print("see input is unknown")
        except:
            print("Unable to fulfill request. The variable you're looking for may not exist yet. Hint: i")
            pass
    
        
    """
    def do_launch_default_interface(self,line):
        "Independantly determine the gui_object (or lack thereof, if use_gui is None)"
        self.interface_object = main.determine_interface(self.style_object,
                                        self.config_input_object,
                                        self.user_input_object)
        launch_interface()
    """
    """ 
    def launch_interface(self):
        main.run_interface(self.style_object,
                           self.interface_object,
                            self.user_input_object,
                            self.config_input_object)
    """
    """    
    def do_simple(self,line):
    #def do_launch_simple(self,line):
        if self.scene_object is None:
            self.do_prep(None)
        "launch the simple gui, regardless of default interface"
        from gui_simple import Gui
        self.interface_object = Gui()
        self.launch_interface()
    """

    """    
    def do_dev(self,line):
    #def do_launch_gui_developer(self,line):
        if self.scene_object is None:
            self.do_prep(None)
        "launch the developer gui, regardless of default interface"
        from gui import Gui
        self.interface_object = Gui()
        self.launch_interface()
    """

    """
    def do_cli(self,line):
    #def do_launch_control_cli(self,line):
        "launch the separate control CLI, regardless of default interface"
        from control_cli import ControlCLI
        self.interface_object = ControlCLI()
        self.launch_interface()
    """

    def do_prep(self,line):
        "Run (1) make scene and (2) make config. Hide print."
        with HiddenPrints():
            self.make_scene(None)
            self.makeconfig(None)

    def do_skipinterface(self,line):
        "Skip interface (3), use direct json file. Rather than editing defaults with a GUI."
        #try:
        self.user_input_object.pull_config_input_object(self.config_input_object)
        
        self.build_grouping(None) # jammed in here for now - need to process when a gui is used as well
        
        print("Hint: Next: (4) make data, or, import data ")
        #except Exception as e:
        #    print("See instructions for necessary steps.")
        
        

        
    def do_no(self,line):
        "(3) skipinterface, hide print"
        with HiddenPrints():
            self.do_skipinterface(None)
        
    def do_go(self,line):
        "Run (4) import data , (5) make pointcloud, and (6) make export. Hide print."

        try:
            print("Generating model...")
            with HiddenPrints():
                self.import_data(None)
                self.build_pointcloud(None)
                self.export_model(None)
            print("Model exported :)")
        except Exception as e:
            print("Export failure.")
            print("See instructions for necessary steps.")

    def do_import(self,line):
        "Future work."
        #try:
        if line == "data":
            self.import_data(None)
        #except Exception as e:
        #    "Try again"
    
    def import_data(self,line):
        "Independantly import data (4). Generates export_control_object. Requires scene_object, style_object, and user_input_object to already exist."
        #try:
        print(f"\nself.scene_object = {self.scene_object}")
        self.export_control_object = main.import_data(self.scene_object,
                                                self.style_object,
                                                self.user_input_object,
                                                self.hierarchy_object)
        print(f"\nself.scene_object = {self.scene_object}")
        print("Hint: Next: (5) make pointcloud")
        #except Exception as e:
        #    print("If the import fails for pyinstaller, ensure that the import plugin is registered in style.py")
        #    print("Failed to import data. See instructions for necessary steps.")
        
    """
    def do_preview2d(self,line):
        "Independantly generate png of imported data"                                                                   
        main.png_preview(self.scene_object,
                         self.user_input_object,
                         self.export_control_object.export_name)
    """

    def build_grouping(self,line):
        # jam in do_3(None), skipinterface for now
        main.build_grouping(self.hierarchy_object,self.user_input_object)

    def build_pointcloud(self,line):
        "Independantly build the point cloud"  
        #try:
        main.build_point_cloud(self.scene_object,
                            self.style_object,
                            self.user_input_object,
                            self.hierarchy_object)
        print(f'subprocesses:\n\
                .construct_scene_heirarchy\n\
                .build_ticks\n\
                .build_texts\n\
                .layout_spatial\n\
                .build_fences\n\
                ')
        
        self.pointcloud_bool = True
        print("Hint: Next: (6) make export")
        #except Exception as e:
        #    print("Failed to build pointcloud.")
        #    pass

    
    """
    def do_preview3d(self,line):
        "Independantly generate scene preview in PyGame"                  
        main.preview_scene(scene_object)
    """
    def do_export(self,line):
        """
        Generate export. 
        Examples: 
            export fbx
            export fbx -glb
            export plot
            export plot -pdf
            export plot -png 
            export plot -svg
            export blend

        plot option defaults to pdf
        """ 
        #try:
        if True:
            if "fbx" in line:
                self.createFBX_object = self.export_model(None)
                self.record_export_path()
            elif "plot" in line:
                print("createPlot.py Under constructions") 
            else:
                print("Hint: help export")
            print("Hint: open --last, or, o -l") #
        #except Exception as e:
        #    print("Export failure. Model not yet fully prepared.")
        #    pass

    def record_export_path(self):
        self.last_export_path = self.scene_object.filepath
        self.all_export_paths.append(self.last_export_path)
        print(f"self.all_export_paths = {self.all_export_paths}")
    def export_model(self,line):
        "Independantly generate export" 
    
        self.createFBX_object = main.generate_export(self.scene_object,
                            self.style_object,
                            self.user_input_object)
        return self.createFBX_object
        #except Exception as e:
        #    print("See instructions for necessary steps.")
    ''' End main. element access'''
    


    eval_parser = cmd2.Cmd2ArgumentParser()
    eval_parser.add_argument("-d","--dict", nargs = "?", default=False, const=True, help ="See dictionary of object")
    eval_parser.add_argument("-k","--keys", nargs = "?", default=False, const=True, help ="See Keys of object")
    #@cmd2.with_argparser(eval_parser)
    def do_eval(self,line):
        """
        See known variables. Use -d flag to see dictionary. 
        Examples:
            eval scene_object -d
            eval scene_object.exportdir
            eval scene_object --keys
            eval scene_object -k

        Security issue.
        """
        try:
            if line == "--all" or line =="-a":
                pprint(eval("self.__dict__"))
            elif not("-d" in line) and not("-k" in line):
                pprint(eval("self."+line))
            elif "-d" in line:
                line_clean = line.replace("-d","")
                pprint(eval("self."+line_clean+".__dict__"))
            elif "-k" in line:
                
                line_clean = line.replace("-k","")
                print("keys for line_clean:")
                #pprint(eval("self."+line_clean+".keys()"))
                key_list = list(eval("self."+line_clean+".__dict__.keys()"))
                pprint(key_list)
        except Exception as e:
            print(f"self.{line} is not a known variable")
    def do_e(self,line):
        print(eval(line))

    config_parser = cmd2.Cmd2ArgumentParser()
    config_parser.add_argument('-l','--list',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. This will not include project diretories saved elsewhere, until some future date when a registration file will track those recent locations.')
    config_parser.add_argument('-le','--listexternal',nargs = "?", default=False, const=True, help='see project directories in the external-project-register.json file') 
    config_parser.add_argument('-t','--tree',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. ')
    config_parser.add_argument('-n','--new', nargs = "?",const="config_"+str(int(time.time())), default=False,help='Create new project directory, and make it the active directory.')
    config_parser.add_argument('-s','--sample', nargs = "?",const="sample-config_"+str(int(time.time())), default=False,help='Generate a sample proect directory, complete with sample files.')
    #config_parser.add_argument('-d','--destroy',nargs = "?", default=False, const=True, help='User is able to destroy existing project directory, when th ')
    config_parser.add_argument('-o','--open',help='Access an existing project directory.')
    config_parser.add_argument('-c','--current',nargs = "?",default=False, const=True,help='See current project.')
    config_parser.add_argument('-cc','--copy',nargs = "?",default=False, const=True,help='Copy current project. New name is hardcoded.')
    @cmd2.with_argparser(config_parser)
    def do_config(self,line):
        "inspect and change values from config_input.json"

    groupmap_parser = cmd2.Cmd2ArgumentParser()
    groupmap_parser.add_argument('-l','--list',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. This will not include project diretories saved elsewhere, until some future date when a registration file will track those recent locations.')
    groupmap_parser.add_argument('-t','--tree',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. ')
    groupmap_parser.add_argument('-n','--new', nargs = "?",const="groupmap_"+str(int(time.time())), default=False,help='Create new project directory, and make it the active directory.')
    groupmap_parser.add_argument('-s','--sample', nargs = "?",const="sample-config_"+str(int(time.time())), default=False,help='Generate a sample proect directory, complete with sample files.')
    #groupmap_parser.add_argument('-d','--destroy',nargs = "?", default=False, const=True, help='User is able to destroy existing project directory, when th ')
    groupmap_parser.add_argument('-o','--open',help='Access an existing project directory.')
    groupmap_parser.add_argument('-c','--current',nargs = "?",default=False, const=True,help='See current project.') 
    groupmap_parser.add_argument('-cc','--copy',nargs = "?",default=False, const=True,help='Copy current project. New name is hardcoded.')
    @cmd2.with_argparser(groupmap_parser)
    def do_groupmap(self,line):
        "inspect and change values from config_input.json"
        

    def do_exit(self,line):
        "Same as quit"
        true = self.do_quit(None)
        return true
        
    def do_quit(self,line):
        "Quit Pavlov CLI."
        return True # returning true quits the program
    
    def do_documentation(self,line):
        "See README.md."
        #return False
        print("Future work.")

    def do_license(self,line):
        "See the license for Pavlov. BSD 3-clause."
        bsd3 = """
        Copyright 2025 George Clayton Bennett

        Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

        1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

        3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        """
        autodesk_clause = """
        Autodesk Clause:
        This software contains Autodesk® FBX® code developed by Autodesk, Inc. Copyright 2008 Autodesk, Inc. All rights, reserved. Such code is provided "as is" and Autodesk, Inc. disclaims any and all warranties, whether express or implied, including without limitation the implied warranties of merchantability, fitness for a particular purpose or non-infringement of third party rights. In no event shall Autodesk, Inc. be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of such code.
        """
        print(bsd3)
        print(autodesk_clause)

    def do_copyright(self,line):
        "See copyright information."
        cr = """\
        Copyright 2025 George Clayton Bennett

        Autodesk Clause:
        This software contains Autodesk® FBX® code developed by Autodesk, Inc. 
        Copyright 2008 Autodesk, Inc. All rights, reserved. 
        Such code is provided "as is" and Autodesk, Inc. disclaims any and all warranties, 
        whether express or implied, including without limitation the implied warranties of merchantability, 
        fitness for a particular purpose or non-infringement of third party rights.
        In no event shall Autodesk, Inc. be liable for any direct, indirect, incidental, special, exemplary, 
        or consequential damages (including, but not limited to, procurement of substitute goods or services; 
        loss of use, data, or profits; or business interruption) however caused and on any theory of liability, 
        whether in contract, strict liability, or tort (including negligence or otherwise) 
        arising in any way out of such code.
        """
        
        print(cr)

    def do_credits(self,line):
        "see credits"
        credit =\
        """
        Clayton Bennett, 2022-2025.
        Pavlov Software & Services LLC, incorportated 2023.

        The Pavlov Project began at the University of Idaho, at the AgMEQ Laboratory.
        Sample data comes courtesy of Dr. Daniel Robertson.
        
        Pavlov 3D was proudly developed in the United States, New Zealand, Thailand, Laos, Vietnam, Australia, and Japan.

        For software tools, thank you to:
        The Python Software Foundation
        The Blender Software Foundation
        Autodesk
        MathWorks
        Open Cascade
        Khronos Group
        Don McCurdy (https://gltf-viewer.donmccurdy.com/)
        
        Pavlov 3D development for 2022-2025 was funded by:
        Dr. Daniel Robertson of the AgMEQ Laboratory at the University of Idaho in Moscow, Idaho, USA
        Mike & Rebecca McKee of Remarkable Motorcycles in Queenstown, Otago, New Zealand
        Dale & Bronwyn Burrows of Franz Josef Wilderness Tours in Franz Josef, West Coast, New Zealand
        SWP Commercial Roofing in Christchurch, Canterbury, New Zealand
        Pete Syme of Alchemy All Metal Fabricators in Cairns, Queensland, Australia
        City of Memphis in Memphis, Tennessee, USA

        Autodesk Clause (required):
        This software contains Autodesk® FBX® code developed by Autodesk, Inc. 
        Copyright 2008 Autodesk, Inc. All rights, reserved. 
        Such code is provided "as is" and Autodesk, Inc. disclaims any and all warranties, 
        whether express or implied, including without limitation the implied warranties of merchantability, 
        fitness for a particular purpose or non-infringement of third party rights.
        In no event shall Autodesk, Inc. be liable for any direct, indirect, incidental, special, exemplary, 
        or consequential damages (including, but not limited to, procurement of substitute goods or services; 
        loss of use, data, or profits; or business interruption) however caused and on any theory of liability, 
        whether in contract, strict liability, or tort (including negligence or otherwise) 
        arising in any way out of such code.

        The Autodesk FBX SDK can be obtained for Mac, Linux, or Windows at this URL:
        https://aps.autodesk.com/developer/overview/fbx-sdk
        """
        self.pretty_title(None)
        print(credit)
    
    def do_g(self,line):
        self.do_guic(line)

    ## Not useful, customtkinter is dead, error showing. 
    ## pip install freesimplegui
    ## import freesimplegui as psg
    # def do_gui(self,line):
    #     """
    #     Launch GUI. Futurework.
    #     Defaults to developer mode. Dependency: PySimpleGui. Secondary: TKinter.
    #     For basic mode, use flag: -b. For developer mode, use flag: -d
    #     """
    #     print("Starting the GUI.")
    #     print("To continue using the CLI, quit the GUI.")
    #     try:
    #         app = gui_customtk_basic.App()
    #         app.pass_in_cli_object(self)
    #         #app = App()
    #         app.mainloop()
    #         #app.quit()
            
    #         if self.style_object.use_GUI is True:
    #             do_launch_gui = str(input("Do you want to launch the Pavlov GUI? (y/N)"))
    #             if do_launch_gui.lower() == "y":
    #                 self.do_select_gui_mode() # this is outdated CB 14Dec24 
    #     except:
    #         pass
        
    
    
    def do_guic(self,line):
        "Wokin progress. Run classic developer mode FreeSimpleGUI."
        if not(self.scene_object is None) and not(self.user_input_object is None): 
            from gui import Gui
            interface_object = Gui()
            interface_object.assign_style_object(self.style_object) 
            interface_object.assign_config_input_object(self.config_input_object)
            interface_object.assign_user_input_object(self.user_input_object,self)
            interface_object.run_and_get_inputs()# user_input_object instantiated inside
        else:
            print("Scene and User Input objets do not exist yet.\nHint: 1, 2")
    def do_guics(self,line):
        "Wokin progress. Run classic simple mode FreeSimpleGUI."
        if not(self.scene_object is None) and not(self.user_input_object is None): 
            from gui_simple import Gui
            interface_object = Gui()
            interface_object.assign_style_object(self.style_object) 
            interface_object.assign_config_input_object(self.config_input_object)
            interface_object.assign_user_input_object(self.user_input_object,self)
            interface_object.run_and_get_inputs()# user_input_object instantiated inside
        else:
            print("Scene and User Input objets do not exist yet.\nHint: 1, 2")

    def do_geometry(self,line):
        "Show a sample of 1 bar, or a few, with current export plugin"
        print("futurework")

    edit_parser = cmd2.Cmd2ArgumentParser()
    edit_parser.add_argument("-c","--config",help ="")
    @cmd2.with_argparser(edit_parser)
    def do_edit(self,args):
        "edit the user_input_object. Once you do this, you must run 4,5,6 again."

        if args.config is not None:
            print(f"args.config = {args.config}")
            key = args.config.split("=")[0]
            print(f"key = {key}")
            new_value = args.config.split("=")[1]
            print(f"new_value = {new_value}")
            if key in list(self.user_input_object.__dict__.keys()):
                self.user_input_object.__dict__[key] =  new_value



    '''
    
    def do_select_gui_mode(self,line):
        "choose gui in simple mode, developer mode, or none"
        gui_mode = str(input("Developer mode (D) or Lite Mode (L)? "))
        if gui_mode.lower() == 'd':
            do_gui_developer_mode = True 
            do_gui_lite_mode = False
        elif gui_mode.lower() == 'l':
            do_gui_developer_mode = False
            do_gui_lite_mode = True
        #return True
    '''
    def do_o(self,line):
        "open, abbreviated"
        self.do_open(line)
    open_parser = cmd2.Cmd2ArgumentParser()
    open_parser.add_argument('-f','--filepath',help='open file')
    open_parser.add_argument("-a","--allnew", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-l","--last", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-c","--config", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-e","--entry", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-b","--browser", nargs = "?", const=Directories.get_program_dir(), default=False, help ="")
    open_parser.add_argument("-g","--guide", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-m","--groupmap", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-p","--project", nargs = "?", default=False, const=True, help ="")

    @cmd2.with_argparser(open_parser)
    def do_open(self,args):
        """
        Open files with the system's default app.
        Include the file extension. 
        Provide the entire path or the filename in the current directory.

        If you are trying to open an FBX file, ensure CAD Assistant is installed.
        Hint: viewer

        If you do not like to default program that it opening your file, change it on your system using: Choose defaults by file type. 

        Examples:
            open C:\\user\\Documents\\pavlov_test.fbx
            open pavlov_awesome.fbx
            open pavlov_hooray.glb
            open exports\\pavlov_stellar.glb

        """
        #print(args.__dict__)
        if args.last is True:
            print(f"args.last = {args.last}")
            fm.openfile(self.last_export_path)

        elif args.filepath is not None:
            fm.openfile(args.filepath)

        elif args.allnew is True:
            if len(self.all_export_paths) ==0:
                print("No export files have yet been generated.")
                pass
            else:
                for filepath in self.all_export_paths:
                    fm.openfile(filepath)

        elif args.config is True:
            fm.openfile(self.config_input_object.config_input_path)

        elif args.entry is True:
            fm.openfilegui(self.config_input_object.config_entry_filepath)

        elif args.browser is not None and args.browser is not False:
            #print(f"args.browser = {args.browser}")
            #fm.opendir(self.config_input_object.script_dir)
            fm.opendir(args.browser)

        elif args.project is True:
            #print(f"args.browser = {args.browser}")
            #fm.opendir(self.config_input_object.script_dir)
            fm.opendir(Directories.get_project_dir())

        # style guide pdf, for what input can be used in the cofiguration files, and the expected keys
        elif args.guide is True:
            fm.openfile(self.config_input_object.config_guide_filepath)

        elif args.groupmap is True:
            fm.openfile(self.config_input_object.groupmap_filepath) # shouldP

        else:
            self.do_help("open")

            
         
            

    #open_parser = cmd2.Cmd2ArgumentParser()
    #open_parser.add_argument('-f','--file',help='open file')
    #@cmd2.with_argparser(open_parser)

    def pretty_title(self,line):
        """
        try:
            string = "Pavlov3D"
            prettystring = pyfiglet.figlet_format(string)
            print(prettystring)
            
        except:
            #pass
            prettystring = ""
        """
        print(self.pavlov3d_prettyprint)
        
        #return prettystring
        
    def do_unix2time(self,line):
        """
        See unix time as datetime
        Output: YYY-MM-DD HH:MM:SS
        Decimal places in a unix time value represent partial seconds, base 10, with direct correlation.

        Examples:
            unix2time 1734202184.912056
            unix2time 1734202184
        """
        
        try:
            datetime_object = datetime.fromtimestamp(float(line))
            print(datetime_object)
        except Exception as e:
            self.do_help("unix2time")

    def do_webapp(self,line):
        """
        Show URL for Pavlov 3D web app.
        """
        print("https://pavlov3d.world")

    def do_video(self,line):
        """
        Show URL for Pavlov 3D tutorial video.
        """
        url = "https://youtu.be/ttBwGudNsxk"
        print(f"{url}")   

    def do_p(self,line):
        self.do_preview("scene")

    preview_parser = cmd2.Cmd2ArgumentParser()
    preview_parser.add_argument('-s','--scene',nargs = "?", default=False, const=True, help='Preview the scene.')
    preview_parser.add_argument('-c','--curve',nargs = "?", default=False, const=True, help='Preview a certain curve. ')
    preview_parser.add_argument('-g','--group', nargs = "?",default=False,help='Preview a certain group.')
    preview_parser.add_argument('-sub','--subgroup', nargs = "?", default=False, const=True,help='Preview a certain subgroup.')
    @cmd2.with_argparser(preview_parser)
    def do_preview(self,args):
        "Preview"
        """
        Preview the model, once the pointcloud is built. 
        Importing matplotlib takes the cli.exe from 21 mb to 34 mb.
        Options:
            Preview just one curve in 3D, to demonstrate export geometry.
            Preview one or more curves in 2D, , with basic plotting.
            Preview all curves in 2D, with basic plotting.
            Preview all curves in 3D, with basic plotting.

        Examples:
            preview scene
            preview scene -2D -xy
            preview scene -2D -xz
            preview scene -2D -yz
            preview scene -3D
            preview curve -2D -i 0
            preview curve -2D -i 2:8
        """
        
        if self.pointcloud_bool==True:
            #try:
            if args.scene is True:
                main.preview_scene3D(self.scene_object)
            elif args.curve is not None:
                i=args.curve
                main.preview_curve3D(self.scene_object,i)
            else:
                self.do_help("preview")
            #except:
            #    print("preview does not function in this version of the Pavlov 3D CLI.")
        else:
            print("The pointcloud is not prepared. Hint: i")
    
    project_parser = cmd2.Cmd2ArgumentParser()
    project_parser.add_argument('-l','--list',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. This will not include project diretories saved elsewhere, until some future date when a registration file will track those recent locations.')
    project_parser.add_argument('-le','--listexternal',nargs = "?", default=False, const=True, help='see project directories in the external-project-register.json file') 
    project_parser.add_argument('-t','--tree',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. ')
    project_parser.add_argument('-n','--new', nargs = "?",const="project_"+str(int(time.time())), default=False,help='Create new project directory, and make it the active directory.')
    project_parser.add_argument('-s','--sample', nargs = "?",const="sample-project_"+str(int(time.time())), default=False,help='Generate a sample proect directory, complete with sample files.')
    project_parser.add_argument('-d','--destroy',nargs = "?", default=False, const=True, help='User is able to destroy existing project directory, when th ')
    project_parser.add_argument('-o','--open',help='Access an existing project directory.')
    project_parser.add_argument('-c','--current',nargs = "?",default=False, const=True,help='See current project.')
    project_parser.add_argument('-cc','--copy',nargs = "?",default=False, const=True,help='Copy current project. New name is hardcoded.')
    @cmd2.with_argparser(project_parser)
    def do_project(self,args):
        "Manage project directories"
        #print(f"args.sample = {args.sample}")
        #print(f"args.new = {args.new}")
        if args.tree is True:
            fm.tree("./projects/")

        elif args.list is True:
            #pprint(DirectoryControl.walk(args.list))
            pprint(DirectoryControl.walk(Directories.get_program_dir()+"/projects/"))
        
        elif args.listexternal is True:
            json_filepath = Directories.get_program_dir()+"\\projects\\external_project_register.json"
            data_tuple = json_handler.create_tuple_from_json(json_filepath)
            print(f"data_tuple = {data_tuple}")

        elif args.current is True:
            print(f"Current project: {Directories.get_project_dir()}")
            
        elif args.new is not None and args.new is not False:
            dir_project_new = DirectoryControl.create_directory_with_structure(args.new,option="empty")
            #dir_project_new = DirectoryControl.create_directory(args.new)
            self.set_project_active(project_dir=dir_project_new)
            
        elif args.sample is not None and args.sample is not False:
            dir_project_new = DirectoryControl.create_directory_with_structure(args.sample,option="sample")
            #dir_project_new = DirectoryControl.create_directory(args.new)
            self.set_project_active(project_dir=dir_project_new) 
            
        elif args.open is not None:
            # Assess if the input textstring is a whole path or is a relative path.
            # A relative path will look in only the ./projects/ directory. 
            self.set_project_active(project_dir=args.open)
            # notes: [[]] https://realpython.com/python-pathlib/

        elif args.copy is True:
            DirectoryControl.copy_project_directory(Directories.get_project_dir(),option="empty")

        

        elif args.destroy is not None and args.destroy is not False:
            
            # deleting directly is not effective
            if False:
                DirectoryControl.destroy_directory(args.destroy)
            else:
                print(f"Manually delete: {args.destroy}")
                #instead, open the browser location for the user to delete
                self.do_open(f"-b projects")
        else:
            self.do_help("project")
    def do_p(self,line):
        " Abbreviation for project" 
        self.do_project(line)
    def do_projects(self,line):
        " Alis for project" 
        self.do_project(line)
    

    def do_ls(self,args):
        print(os.getcwd())
        print("\nDirectories:")
        for entry in os.listdir(os.getcwd()):
            if os.path.isdir(entry):
                print(f"\t{entry}")
        print("\nFiles:")
        for entry in os.listdir(os.getcwd()):
            if os.path.isfile(entry):
                print(f"\t{entry}")

    def do_cd(self,args):
        os.chdir(args)
        print(os.getcwd())
        

    template_cmd2_parser = cmd2.Cmd2ArgumentParser()
    template_cmd2_parser.add_argument('-n','--new',help='create new project directory')
    template_cmd2_parser.add_argument('-o','--open',help='access existing project directory')
    template_cmd2_parser.add_argument('--destroy',help='destroy existing project directory')
    template_cmd2_parser.add_argument('-t','--tree',help='print tree using library: null')
    @cmd2.with_argparser(template_cmd2_parser)
    def do_template_cmd2(self,args):
        if args.tree is not None:
            print(f"os.getcwd() =  {os.getcwd()}")
            self.do_tree(None)
        if args.destroy is not None:
            DirectoryControl.destroy_directory(args.destroy)
        else:
            self.do_help("template_cmd2")

    spark_parser = cmd2.Cmd2ArgumentParser()
    spark_parser.add_argument('-a','--all',nargs = "?", default=False, const=True,help='')
    spark_parser.add_argument('-t','--time',nargs = "?", default=False, const=True,help='')
    spark_parser.add_argument('-d','--depth',nargs = "?", default=False, const=True,help='')
    spark_parser.add_argument('-he','--height',help='')
    spark_parser.add_argument('-i','--index',help='')
    spark_parser.add_argument('-s','--scaled',help='')
    @cmd2.with_argparser(spark_parser)
    def do_spark(self,args):
        """
        Spark graph preview. Use time, height, depth, or other options.
        
        Examples:
            spark height -all
            spark index 1
        """

        #if line.startswith("time") and "-all" in line:
        if args.time is True:
            #and "-all" in line:
            print("Time values")
            self.sparkarray_direction(self.scene_object.vectorArray_time)

        #elif line.startswith("height") and "-all" in line:
        elif args.height is not None:
            #and "-all" in line:
            if args.height is True:
                print("Height values")
                self.sparkarray_direction(self.scene_object.vectorArray_height)
            else:
                i = int(args.height)
                key = list(self.hierarchy_object.dict_curve_objects_all)[i]
                curve_object = self.hierarchy_object.dict_curve_objects_all[key]
                vector = curve_object.dict_data_vectors_raw["height"]
                all = [x-min(vector) for x in vector]
                print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
                for line in sparklines(all,num_lines=1):
                    print(line)
        

        #elif line.startswith("depth") and "-all" in line:
        elif args.depth is True:
            print("Depth values")
            self.sparkarray_direction(self.scene_object.vectorArray_depth)

        #elif line.startswith("index"):
        elif args.index is not None:
            i = int(args.index)
            #i = int(line.split("index")[1])
            print(self.scene_object.names[i])
            print(f"i = {i}")

            print("-----")
            print("Time values")
            print(f"Header: {self.scene_object.headers_time[i]}")
            vector = self.scene_object.vectorArray_time[i]
            all = [x-min(vector) for x in vector]
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)
            
            print("-----")
            print("Height values")
            print(f"Header: {self.scene_object.headers_height[i]}")
            vector = self.scene_object.vectorArray_height[i]
            all = [x-min(vector) for x in vector]
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)

            print("-----")
            print("Depth values")
            print(f"Header: {self.scene_object.headers_depth[i]}")
            print(self.scene_object.headers_depth[i])
            vector = self.scene_object.vectorArray_depth[i]
            all = [x-min(vector) for x in vector]
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)
            print("-----")

            """
            print("Depth values")
            vector = self.scene_object.vectorArray_depth[i]
            all = [x-min(vector) for x in vector]
            for line in sparklines(all,num_lines=1):
                print(line)
            """

        elif args.scaled is not None:
            print(f"args.scaled = {args.scaled}")
            i = int(args.scaled)
            print(self.scene_object.names[i])
            print(f"i = {i}")
            print("-----")
            print("Scaled Height values")
            key = list(self.hierarchy_object.dict_curve_objects_all)[i]
            curve_object = self.hierarchy_object.dict_curve_objects_all[key]
            vector = curve_object.dict_data_vectors_scaled["height"]
            #vector = self.scene_object.vectorArray_height[i]
            all = [x-min(vector) for x in vector]
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)
        else:
            self.do_help("spark")

    def sparkarray_direction(self,array):
        for i,vector in enumerate(array):
            print(self.scene_object.names[i])
            all = [x-min(vector) for x in vector]
            print(f"n = {i}")       
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)
    
    def sparkvector_direction(self,vector):
        i = int(line.split("-index")[1])
        print(self.scene_object.names[i])
        all = [x-min(vector) for x in vector]
        print(f"i = {i}")
        print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}")
        for line in sparklines(all,num_lines=1):
            print(line)

    def do_query(self,line):
        #Conversational characterization of data.
        hint_string = 'At any time you may see the default sample setting by typing [default].\nAlso, type quit to quit. This word, quit, cannot be a group name.\n   '
        print(f"{hint_string}")
        self.dict_query = self.characterization_mapping(self.characterization_query())


    def characterization_query(self):
        dict_query = dict()
        dict_query["data_file_single_or_multiple"] = str(input("Is your data in [one] single file or in [multiple] files? :: "))
        dict_query["points_or_curves_or_meshes"] = str(input("Would you characterize each data source as a [point], a [curve], or a [mesh]? :: "))
        dict_query["source_multiplicity_per_file"] = str(input(f"Is there [one] {dict_query['points_or_curves_or_meshes']} or [multiple] in each imported data file? :: "))
        dict_query["import_data_filetype"] = str(input("What filetype is/are your imported data file(s)? [FBX,CSV,XLSX,XLS]:: "))
        print("To choose an export style, please edit configuration JSON file or make a new one, and point to it with the config_entry.json file in your project. You can edit it with this command: open --config, open --entry. For guidance, use open --guide. ")
        return dict_query   
    
    def characterization_mapping(characterization_query):
        #relate raw responses to useful configuration values
        dict_query = characterization_query
        return dict_query
    
    def no_args(args):

        #major error 19 January 2025 - blockage - drop
        # There has to be a better way to say "if you only typed the command with no arguments"
        bool_are_there_args = args.cmd2_statement.__dict__['_Cmd2AttributeWrapper__attribute'].args 
        print(f"bool_are_there_args = {bool_are_there_args}")
        return "" == bool_are_there_args
    
    def do_tree(self,line):
        # show file tree below current working directory
        print(os.getcwd())
        os.system("tree")
        #subprocess.call("tree")

    def do_clear(self,line):
        
        if environmental.windows():
            os.system('cls')
        else:
            os.system('clear')

    def do_htree(self,line):
        "Hierarchy tree, text."
        self.hierarchy_object.print_hierarchy_tree()
        #self.hierarchy_object.print_hierarchy_by_lineage()

    def do_hhtree(self,line):
        "Hierarchy tree, fancy."
        #self.hierarchy_object.print_hierarchy_tree()
        self.hierarchy_object.print_hierarchy_by_lineage()
    
    def do_stree(self,line):
        "Sibling tree."
        self.hierarchy_object.print_hierarchy_tree_sibling()
    def do_sstree(self,line):
        "Sibling tree, fancy."
        self.hierarchy_object.print_hierarchy_previous_siblings_by_lineage()
    def do_cctree(self,line):
        "Cousin tree."
        #self.hierarchy_object.print_hierarchy_tree_cousins()
        self.hierarchy_object.print_hierarchy_cousins_by_lineage()

    def do_dorsl(self,line):
        self.hierarchy_object.print_hierarchy_data_origins_relative_to_supergroup_by_lineage()

    def do_psl(self,line):
        self.hierarchy_object.print_hierarchy_place_in_supergroup_by_lineage()

    topo_parser = cmd2.Cmd2ArgumentParser()
    #topo_parser.add_argument('-t','--topo',nargs = "?", default=False, const=True, help='See topgraphy string, to test terminal capacity.')
    topo_parser.add_argument('-v','--vector', help='Example: topo -v [0,10,1,9,2,8,3,7,4,6,5,5,5,6,7,8,9,10,8,6,4,2,0,10,0,10]') 
    @cmd2.with_argparser(topo_parser)
    def do_topo(self,args):
        "Example: topo -v [0,10,1,9,2,8,3,7,4,6,5,5,5,6,7,8,9,10,8,6,4,2,0,10,0,10]"
        #if args.topo is True:
        #    print(self.topography)
        if args.vector is not None:
            for line in sparklines(eval(args.vector),num_lines=1):
                print(line)
            print("-----")
        else:
            print(self.topography)


    project_parser = cmd2.Cmd2ArgumentParser()
    project_parser.add_argument('-l','--list',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. This will not include project diretories saved elsewhere, until some future date when a registration file will track those recent locations.')
    project_parser.add_argument('-le','--listexternal',nargs = "?", default=False, const=True, help='see project directories in the external-project-register.json file') 
    project_parser.add_argument('-t','--tree',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. ')
    project_parser.add_argument('-n','--new', nargs = "?",const="project_"+str(int(time.time())), default=False,help='Create new project directory, and make it the active directory.')
    project_parser.add_argument('-s','--sample', nargs = "?",const="sample-project_"+str(int(time.time())), default=False,help='Generate a sample proect directory, complete with sample files.')
    project_parser.add_argument('-d','--destroy',nargs = "?", default=False, const=True, help='User is able to destroy existing project directory, when th ')
    project_parser.add_argument('-o','--open',help='Access an existing project directory.')
    project_parser.add_argument('-c','--current',nargs = "?",default=False, const=True,help='See current project.')
    project_parser.add_argument('-cc','--copy',nargs = "?",default=False, const=True,help='Copy current project. New name is hardcoded.')
    @cmd2.with_argparser(project_parser)
    def do_project(self,args):
        "Manage project directories"
        #print(f"args.sample = {args.sample}")
        #print(f"args.new = {args.new}")
        if args.tree is True:
            fm.tree("./projects/")

        elif args.list is True:
            #pprint(DirectoryControl.walk(args.list))
            pprint(DirectoryControl.walk(Directories.get_program_dir()+"/projects/"))
        
        elif args.listexternal is True:
            json_filepath = Directories.get_program_dir()+"\\projects\\external_project_register.json"
            data_tuple = json_handler.create_tuple_from_json(json_filepath)
            print(f"data_tuple = {data_tuple}")

        elif args.current is True:
            print(f"Current project: {Directories.get_project_dir()}")
            
        elif args.new is not None and args.new is not False:
            dir_project_new = DirectoryControl.create_directory_with_structure(args.new,option="empty")
            #dir_project_new = DirectoryControl.create_directory(args.new)
            self.set_project_active(project_dir=dir_project_new)
            
        elif args.sample is not None and args.sample is not False:
            dir_project_new = DirectoryControl.create_directory_with_structure(args.sample,option="sample")
            #dir_project_new = DirectoryControl.create_directory(args.new)
            self.set_project_active(project_dir=dir_project_new) 
            
        elif args.open is not None:
            # Assess if the input textstring is a whole path or is a relative path.
            # A relative path will look in only the ./projects/ directory. 
            self.set_project_active(project_dir=args.open)
            # notes: [[]] https://realpython.com/python-pathlib/

        elif args.copy is True:
            DirectoryControl.copy_project_directory(Directories.get_project_dir(),option="empty")


    
if __name__=='__main__':
    Directories.initilize_program_dir()
    PavlovCLI.initialize_scene_object()
    #PavlovCLI.link_initial_project_directory()
    Directories.initialize_startup_project()
    PavlovCLI().cmdloop()
