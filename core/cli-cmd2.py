#!/usr/bin/env python
"""
Title: cli.py
Author: Clayton Bennett
Created: 19 December 2024

Purpose: 
Run Command line interface to access methods from other tools in the directory. 
"""
import cmd2
#import argparse
import os
#from xlsx_viewer import xlsx
#from pprint import pprint
from pathlib import Path
import shutil


class CLI(cmd2.Cmd):
    prompt = ">>>"

    def do_xlsx(self, line):
        """
        Examples: 
            xlsx
            xlsx C:\\Users\\user\\Downloads\\example.xlsx
        Paste full file path.
        """
        x = r'C:\Users\george.bennett\OneDrive - City of Memphis\Documents\Henry-17Dec\Maxson Lagoon Temps 2021-0d4f0053-7459-43b1-85d6-70dfa082cdc1'
        print(line)
        self.xlsx = xlsx(line)

    def do_eval(self, line):
        """
        Evaluate variables and expressions.
        WARNING: This is a security issue.

        Example:
            eval self.df
        """
        print(line)
        print(eval(line))

    def do_see(self, line):
        """
        See known variables attached to the CLI class instance.
        WARNING: This is a security issue.

        Example:
            see df
        """
        clean = r"self."+line
        print(eval(clean))

    project_parser = cmd2.Cmd2ArgumentParser()
    project_parser.add_argument('-n','--new',help='create new project directory')
    project_parser.add_argument('-o','--open',help='access existing project directory')
    project_parser.add_argument('--destroy',help='destroy existing project directory')

    @cmd2.with_argparser(project_parser)
    def do_project(self,args):
        "Manage project directories"
        #print(f"args = {args}")
        #print(f"args.new = {args.new}")
        if args.new is not None:
        #if hasattr(args,'new'):
            DirectoryControl.create_directory(args.new)
            #Path(args.new).mkdir(parents=True, exist_ok=True)
            #os.mkdir(args.new)
        if args.destroy is not None:
            DirectoryControl.destroy_directory(args.destroy)


        
class DirectoryControl:
#def dircon():
    @staticmethod
    #def create_directory(self,path):
    def create_directory(path):
        directory = Path(path) 
        if directory.exists(): 
            print(f"The directory '{path}' already exists.") 
        else: 
            directory.mkdir(parents=True, exist_ok=True) # default 0o755 rwxrwxr-x
            #directory.mkdir(parents=True, exist_ok=True,mode=0o755) # rwxrwxr-x
            #directory.mkdir(parents=True, exist_ok=True,mode=0o777) # rwxrwxrwx
            DirectoryControl.populate_fresh_project_directory()
            print(f"The directory '{path}' has been created.") 
    
    @staticmethod
    #def populate_fresh_project_directory(self):
    def populate_fresh_project_directory():
        pass
    @staticmethod
    #def destroy_directory(self,path):
    def destroy_directory(path):
        if not(os.path.exists(path)):
            print("Path not found.")
            return True
        confirm = str(input("Confirm destroy directory (Y/n): "))
        if confirm.lower()=="y":
            shutil.rmtree(path)
            try:
                shutil.rmtree(path)
            except:
                print("There is a problem, likely with permission.")
                print("Directory not destroyed.")
            else:
                print("Directory destroyed.")
            return None
            
        else:
            print("Directory not destroyed.")
            return False

        
if __name__ == '__main__':
    cli = CLI()
    cli.cmdloop()