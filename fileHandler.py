import os
import shutil
import traceback
import sys
from tkinter import messagebox  
import pandas as pd  
"""
FUNCTIONS

def get_executable_dir
def copy_file
def create_file_if_missing
def create_dir_if_missing
def create_dir
def save_file
def calculate_full_destination_path
def calculate_full_file_path
def clear_files
def truncate_filename
def get_file_extension
"""

def get_executable_dir():
    """
    Gets the directory of the executable file or script.
    If running as an executable, returns the directory of the executable.
    If running as a script, returns the script's directory.
    """
    try:
        frozen = getattr(sys, 'frozen', False) #If an executable is running the system will be frozen. If the system attribute 'frozen' is true, the function returns true. If not it will return the default value, which has here been set to false
        if frozen:
            return os.path.dirname(sys.executable) #returns the path of the  directory in which the currently running executable is stored
        return os.path.dirname(os.path.realpath(__file__))# realpath returns the absolute path for the currently running script (_file_ sometimes shows the relative path)
    except Exception as e:
        traceback.print_exc() # prints the stack trace of the error on the console
        error_message = f"An error occurred in get_executable_dir: {e}" #An f string allows you to insert variables into the string
        messagebox.showerror("Error", error_message) 
        return None

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

def create_file_if_missing(file_path):
    """
    If the file path passed into the function does not exist, it is created
    """
    try:
        new_file_created = False
        complete_file_path = calculate_full_file_path(file_path)
        
        # Check if the file exists
        file_exists = os.path.exists(complete_file_path)
        
        # Create the file if it does not exist
        if not file_exists:
            with open(complete_file_path, 'w') as f: # When a file is opened using with it will automatically be saved when the with block finishes
                pass  #pass does nothing but is used when python requires a block to not be empty
            new_file_created = True
        
        print('create_file_if_missing 3')
        
        return new_file_created
        
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in create_file_if_missing: {e}"
        messagebox.showerror("Error", error_message)


def create_dir_if_missing(file_path):
    """
    Ensures a folder is created if it does not exist
    """
    try:
        #TK
        print('create_dir_if_missing started')
        folder_created = False
        complete_folder_path = calculate_full_file_path(file_path)
        folder_exists = os.path.exists(complete_folder_path)
        
        if not folder_exists:
            print('folder does not exist')#TK remove log
            os.makedirs(folder_path)
            folder_created = True
        else:#tk remove block
            print('folder exists')

        return folder_created

    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in create_dir_if_missing: {e}"
        messagebox.showerror("Error", error_message)

def create_dir(file_path):
    """
    Ensures a folder is created if it does not exist
    """
    try:
        folder_created = False
        complete_folder_path = calculate_full_file_path(file_path)
        os.makedirs(complete_folder_path)
        folder_created = True

        return folder_created

    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in create_dir_if_missing: {e}"
        messagebox.showerror("Error", error_message)

def save_file(dataframe, file_name, destination_folder="data/results"):
    """
    Saves a pandas DataFrame to an Excel file in the specified destination folder:
     - If the folder does not exist, it is created.
     - Returns the file path of the saved file or None in case of an error.
    """
    try:
        if not isinstance(dataframe, pd.DataFrame):
            messagebox.showerror("Error", "Invalid DataFrame. Please provide a valid pandas DataFrame.")
            return None

        file_path = calculate_full_destination_path(file_name, destination_folder)
        create_dir_if_missing(file_path)
        dataframe.to_excel(file_path, index=False) #saves the dataframe as an excel file. index=false means the index of each row in the database will not be added in a seperate column
        return file_path
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in save_file: {e}"
        messagebox.showerror("Error", error_message)
        return None

def calculate_full_destination_path(file_name, destination_folder):
    """
    Calculates the correct file path dependizng on whether script is being run by python
    or as an executable
    """
    try:
        base_path = get_executable_dir() # Get the path of the currently running script or executable file
        complete_destination_folder = os.path.join(base_path, destination_folder)
        has_file_name = bool(file_name) # Check if file_name has been passed in

        # If there is a file name, append it to the folder path
        if has_file_name:
            file_path = os.path.join(complete_destination_folder, file_name)
        else:
            file_path = complete_destination_folder

        file_path = os.path.normpath(file_path) #makes sure the use of slashes in the file path is consistent
        
        return file_path
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in calculate_full_destination_path: {e}"
        messagebox.showerror("Error", error_message)
        return None

def calculate_full_file_path(file_path):
    """
    Calculates the correct file path depending on whether script is being run by python
    or as an executable
    """
    try:
        base_path = get_executable_dir() # Get the path of the currently running script or executable file
        complete_file_path = os.path.join(base_path, file_path)
        complete_file_path_cleaned = os.path.normpath(complete_file_path) #makes sure the use of slashes in the file path is consistent
        return complete_file_path_cleaned
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in calculate_full_file_path: {e}"
        messagebox.showerror("Error", error_message)
        return None
    
def clear_files(folders=["data/input", "data/results"]):
    """
    Clears all files in the specified folders.
    If a folder exists, deletes all regular files inside it.
    """
    try:
        base_path = get_executable_dir() #path of the currently running script or executable file

        for folder in folders:
            folder_path = os.path.join(base_path, folder)
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path): # listdir returns all the folders and file names in a folder path
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path): #checks the path refers to a file andn not a folder
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