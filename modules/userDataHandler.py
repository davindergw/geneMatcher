""" 
This file is part of Gene Matcher.
Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See LICENSE file for details: https://creativecommons.org/licenses/by-nc/4.0/
"""
import config
import os
import traceback
from tkinter import messagebox

"""
FUNCTIONS

def read_number_from_file
def write_number_to_file
def increment_number_in_file
def track_uses
"""

def read_number_from_file(file_path):
    """Reads a number from a text file. Returns 0 if the file does not exist or is empty."""
    try:

        with open(config.NUMBER_OF_USES_FILE, "r") as file: #open file in read mode. which ensures file is closed properly, even if an error occurs
            content = file.read().strip()
            if content.isdigit():  # Check if the content is a valid integer
                number = int(content) 
            else:
                number = 0  # Default to 0 if content is not a valid number

            return number  
    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"An error occurred in read_number_from_file: {e}")
        return 0

def write_number_to_file(file_path, number):
    """Wipes the file clean and writes a new number to it."""
    try:
        with open(file_path, "w") as file:
            file.write(str(number))  # Write the new number as a string

    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"An error occurred in write_number_to_file: {e}")

def track_use():
    """Reads the number, increments it by 1, and writes it back to the file."""
    try:
        number = read_number_from_file(config.NUMBER_OF_USES_FILE)
        number += 1  
        write_number_to_file(config.NUMBER_OF_USES_FILE, number)
        return number

    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"An error occurred in increment_number_in_file: {e}")
        return None