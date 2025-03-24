""" 
This file is part of Gene Matcher.
Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See LICENSE file for details: https://creativecommons.org/licenses/by-nc/4.0/
"""
import sys
sys.dont_write_bytecode = True #stops python from caching files in modules folder
import config
import traceback
from tkinter import messagebox
from modules.gui import setup_gui
from modules.fileHandler import setup_file_structure

def bootstrap_app():
    """
    Dispays the button to see the results file
    """
    try:
        
        setup_file_structure()
        setup_gui()
        
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in bootstrap_app: {e}"
        messagebox.showerror("Error", error_message)


if __name__ == "__main__": #When a python script is run directly, the value of __name__ is set to __main__
    bootstrap_app()