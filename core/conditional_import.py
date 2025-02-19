'''
Title: conditionally_imported_libraries.py
Author: Clayton Bennett
Created: 9 Feburay 2024

Purpose: Embrace the OOP.
'''


class conditional_import:
    def __init__(self):
        self.name = 'conditional_import'
        self.libraries = dict()

    def add_module(self,module):
        #self.module = module
        print(f'str(module)={str(module)}')
        self.libraries.update({str(module),module})