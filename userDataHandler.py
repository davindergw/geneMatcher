import os
import traceback
from tkinter import messagebox
from fileHandler import calculate_full_destination_path, calculate_full_file_path, create_file_if_missing, create_dir_if_missing

def read_number_from_file(file_path):
    """Reads a number from a text file. Returns 0 if the file does not exist or is empty."""
    try:
        full_file_path = calculate_full_destination_path(None, file_path)

        with open(full_file_path, "r") as file: #open file in read mode. with ensures file is closed properly, even if an error occurs
            content = file.read().strip()
            if content.isdigit():  # Check if the content is a valid integer
                number = int(content)  # Convert to an integer
            else:
                number = 0  # Default to 0 if content is not a valid number

            return number  # Return the final result

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

def increment_number_in_file(file_path):
    """Reads the number, increments it by 1, and writes it back to the file."""
    try:
        number = read_number_from_file(file_path)
        number += 1  # Increment by 1
        write_number_to_file(file_path, number)
        return number

    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"An error occurred in increment_number_in_file: {e}")
        return None

def track_uses():
    """
    Increments the number in the numberOfUses file
    """
    try:
        numberOfUses_file_path = calculate_full_file_path("data/user/numberOfUses.txt")
        user_folder_created = create_dir_if_missing("data/user")
        new_file_created = create_file_if_missing(numberOfUses_file_path)
        numberOfUses = increment_number_in_file(numberOfUses_file_path)
        return numberOfUses
        
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in track_uses: {e}"
        messagebox.showerror("Error", error_message)
