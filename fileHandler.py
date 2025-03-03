import os
import shutil
import traceback
import sys
from tkinter import messagebox  # Importing messagebox for showing warnings and error dialogs in GUI
import pandas as pd  # Importing pandas for dataframe operations

def get_executable_dir():
    """
    Gets the directory of the executable file or script.
    If running as an executable, returns the directory of the executable.
    If running as a script, returns the script's directory.
    """
    try:
        frozen = getattr(sys, 'frozen', False) #If an executable is running the system will be frozen. If the system attribute 'frozen' is true, the function returns true. If not it will return the default value, which has here been set to false
        if frozen:
            return os.path.dirname(sys.executable) #returns the path of the  directory in which the currently running executabl
        return os.path.dirname(os.path.realpath(__file__))# realpath returns the absolute path for the currently running script, as if this is not used _file_ sometimes shows the relative path
    except Exception as e:
        traceback.print_exc() # prints the stack trace o the error on the console
        error_message = f"An error occurred in get_executable_dir: {e}" #An f string allows you to insert variables into the string
        messagebox.showerror("Error", error_message) # displays the error in a notification box
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

        base_path = get_executable_dir() #function retrieves the path of the currently running script or executable file
        if base_path is None:
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

def create_dir_if_missing(file_path):
    """
    Ensures the folder for the given file or folder path exists.
    - If `file_path` is a file, it creates the parent folder.
    - If `file_path` is a folder, it ensures the folder exists.
    """
    try:
        # Check if the given path is a folder
        is_folder = os.path.isdir(file_path)
        
        # Determine the folder path to check
        if is_folder:
            folder_path = file_path
        else:
            folder_path = os.path.dirname(file_path)
        
        # Check if the folder exists
        folder_exists = os.path.exists(folder_path)
        
        # Create the folder if it does not exist
        if not folder_exists:
            os.makedirs(folder_path)

    except Exception as e:
        # Print the error traceback
        traceback.print_exc()

        # Prepare an error message
        error_message = f"An error occurred in create_dir_if_missing: {e}"

        # Show the error message in a pop-up
        messagebox.showerror("Error", error_message)

def save_file(dataframe, file_name, destination_folder="data/results"):
    """
    Saves a pandas DataFrame to an Excel file in the specified destination folder.
    If the folder does not exist, it is created.
    Returns the file path of the saved file or None in case of an error.
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
    Calculates the correct file path depending on whether script is being run by python
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

