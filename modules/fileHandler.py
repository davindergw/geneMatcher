""" 
This file is part of Gene Matcher.
Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See LICENSE file for details: https://creativecommons.org/licenses/by-nc/4.0/
"""
import config
import config
import os
import shutil
import traceback
import sys
import config
from tkinter import messagebox  
import pandas as pd  
"""
FUNCTIONS

def setup_file_structure
def copy_file
def save_file
def clear_files
def truncate_filename
def get_file_extension
"""

def setup_file_structure():
    """
    Ensures required folders and files exist for the application.
    """
    try:
        # Create necessary folders
        for folder in config.ALL_FOLDERS:
            os.makedirs(folder, exist_ok=True)

        # Create the number_of_uses file if it doesn't exist
        if not os.path.exists(config.NUMBER_OF_USES_FILE):
            with open(config.NUMBER_OF_USES_FILE, "w") as f:
                f.write("0")  # Initialize with zero uses

    except Exception as e:
        traceback.print_exc() 
        messagebox.showerror("Error", f"An error occurred in setup_file_structure: {e}") 

def copy_file(source_path, destination_folder):
    """
    Copies a file to the specified destination folder.
    If the folder does not exist, it is created.
    Returns the path of the copied file or None in case of an error.
    """
    try:
        if not source_path:
            messagebox.showwarning("No File", "Please select an Excel file before submitting.")
            return None
        
        file_name = os.path.basename(source_path)
        destination_path = calculate_full_destination_path(file_name, destination_folder)
        create_dir_if_missing(destination_path)
        shutil.copy(source_path, destination_path) # actually copies the file from one path to another
        return destination_path
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in copy_file: {e}"
        messagebox.showerror("Error", error_message)
        return None


def save_file(dataframe, file_name, destination_folder):
    """
    Saves a pandas DataFrame to an Excel file in the specified destination folder:
     - If the folder does not exist, it is created.
     - Returns the file path of the saved file or None in case of an error.
    """
    try:
        os.makedirs(destination_folder, exist_ok=True)  # Ensure the folder exists
        file_path = os.path.join(destination_folder, file_name)
        file_extension = get_file_extension(file_name)

        if file_extension in [".xls", ".xlsx"]:
            dataframe.to_excel(file_path, index=False)
        elif file_extension in [".ods"]:
            dataframe.to_excel(file_path, index=False, engine='odf')

        os.chmod(file_path, 0o666)  # Grant read & write permissions to the owner and others
        
        return file_path

    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in save_file: {e}"
        messagebox.showerror("Error", error_message)
        return None

    
def clear_files():
    """
    Clears all files in the specified folders.
    If a folder exists, deletes all regular files inside it.
    """
    try:
        #app_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script/executable
        
        results_folder = config.RESULTS_FOLDER

        for filename in os.listdir(results_folder):  # Get all files in the folder
            file_path = os.path.join(results_folder, filename)  
            
            if os.path.isfile(file_path): # Ensure it's a file before deleting
                os.remove(file_path)

    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in clear_files: {e}"
        messagebox.showerror("Error", error_message)

def truncate_filename(filename, max_length=20):
    """
    Truncates the filename and adds '...' if it exceeds the max length.
    """
    try:
        if len(filename) > max_length:
            truncated_filename = filename[:max_length - 3] + "..."

            return truncated_filename

        return filename
    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in truncate_filename: {e}"
        messagebox.showerror("Error", error_message)

def get_file_extension(file_path):
    """
    Returns the lowercase file extension of a given file path.
    """
    try:
        file_name, file_extension = os.path.splitext(file_path) #split text returns a tuple containing the filename and its extension

        file_extension = file_extension.lower()

        return file_extension
    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in get_file_extension: {e}"
        messagebox.showerror("Error", error_message)