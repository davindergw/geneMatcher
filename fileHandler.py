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
        
        complete_destination_folder = os.path.join(base_path, destination_folder) # add the folder name onto the destination path to create the path to the folder the file is to be copied to
        create_dir_if_missing(complete_destination_folder)
        
        destination_path = os.path.join(complete_destination_folder, os.path.basename(source_path)) #os.path.basename gets the filname from the end of the path. This is added to the destination folder path to create the full path for the new file
        shutil.copy(source_path, destination_path) # actually copies the file from one path to another
        return destination_path
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in copy_file: {e}"
        messagebox.showerror("Error", error_message)
        return None

def create_dir_if_missing(folder_path):
    """
    Checks if a folder exists and creates it if it does not.
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in create_dir_if_missing: {e}"
        messagebox.showerror("Error", error_message)

def save_file(dataframe, file_name, destination_folder="results"):
    """
    Saves a pandas DataFrame to an Excel file in the specified destination folder.
    If the folder does not exist, it is created.
    Returns the file path of the saved file or None in case of an error.
    """
    try:
        if not isinstance(dataframe, pd.DataFrame):
            messagebox.showerror("Error", "Invalid DataFrame. Please provide a valid pandas DataFrame.")
            return None

        base_path = get_executable_dir() #gets the path of the currently running script or executable file
        
        complete_destination_folder = os.path.join(base_path, destination_folder) # create the path for the destination folder being saved to by adding the folder name onto the path of the currently running script or executable file
        create_dir_if_missing(complete_destination_folder)
        
        file_path = os.path.join(complete_destination_folder, file_name) #add the file name onto the path of the destination folder
        dataframe.to_excel(file_path, index=False) #saves the dataframe as an excel file. index=false means the index of each row in the database will not be added in a seperate column
        return file_path
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in save_file: {e}"
        messagebox.showerror("Error", error_message)
        return None
    
def clear_files(folders=["results", "data"]):
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

