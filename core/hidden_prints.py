'''
Title: hidden_prints.py
Copied: 03 July 2024
Source: https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print
'''
import sys, os
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout