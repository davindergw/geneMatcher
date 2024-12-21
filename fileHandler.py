import os
import shutil
import traceback
import sys
from tkinter import messagebox
import pandas as pd

def get_executable_dir():
    # Check if running from a frozen executable (PyInstaller)
    # getattr allows you to retrieve the value for a given object attribute
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)  # Path to the directory of the executable
    else:
        return os.path.dirname(os.path.realpath(__file__))  # Path to the directory of the script

# Assuming you have other functions like `generate_document` defined elsewhere
def copy_file(source_path, destination_folder):
    if not source_path:
        messagebox.showwarning("No File", "Please select an Excel file before submitting.")
        return None  # Return None explicitly when no file is selected

    try:
        print("1")
        
        base_path = get_executable_dir()
        complete_destination_folder = base_path + '\\' + destination_folder
        
        # Create the 'data' folder if it doesn't exist
        if not os.path.exists(complete_destination_folder):
            os.makedirs(destination_folder)

        # Save the file to the 'data' folder
        file_name = os.path.basename(source_path)
        destination_path = os.path.join(complete_destination_folder, file_name)
        shutil.copy(source_path, destination_path)

        return destination_path  # Return the path of the saved file

    except Exception as e:
        # Print the full error message and stack trace to the console
        print("An error occurred in save_file:")
        print(str(e))
        traceback.print_exc()  # This will print the stack trace to the console
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None  # Return None explicitly when an error occurs
def save_file(dataframe, file_name, destination_folder="results"):
    """
    Save a DataFrame to a file in the specified destination folder.

    Args:
        dataframe (pd.DataFrame): The pandas DataFrame to save.
        file_name (str): The name of the file to save (including extension, e.g., 'output.xlsx').
        destination_folder (str): The folder where the file will be saved. Defaults to 'results'.

    Returns:
        str: The full path of the saved file, or None if an error occurred.
    """
    try:
        # Get the base directory depending on the execution context
        base_path = get_executable_dir()
        complete_destination_folder = os.path.join(base_path, destination_folder)

        # Ensure the destination folder exists
        os.makedirs(complete_destination_folder, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(complete_destination_folder, file_name)

        # Save the DataFrame to the file
        if file_name.endswith(".xlsx"):
            dataframe.to_excel(file_path, index=False)
        elif file_name.endswith(".csv"):
            dataframe.to_csv(file_path, index=False)
        else:
            raise ValueError("Unsupported file format. Please use '.xlsx' or '.csv'.")

        print(f"File saved successfully at: {file_path}")
        return file_path

    except Exception as e:
        # Handle errors gracefully
        print("An error occurred in save_file:")
        print(str(e))
        traceback.print_exc()
        messagebox.showerror("Error", f"An error occurred while saving the file: {e}")
        return None


def clear_files(folders=["results", "data"]):
    try:
        base_path = get_executable_dir()  # Get the base path for the executable or script
        
        # Iterate over each folder provided
        for folder in folders:
            folder_path = os.path.join(base_path, folder)  # Use base_path to determine the full folder path
            
            if os.path.exists(folder_path):
                # Loop through all files in the folder
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        # Check if it's a file (not a subdirectory) and delete it
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
            else:
                print(f"Folder {folder} does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting files: {e}")
