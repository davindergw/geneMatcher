import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import traceback
from documentGenerator import generate_document
from fileHandler import copy_file, clear_files, save_file
# Initialize a variable to store the file path
source_file_path = None

# Function to handle file selection
def select_file():
    global source_file_path
    source_file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xls *.xlsx")]
    )
    if source_file_path:
        status_label.config(text=f"Selected: {os.path.basename(source_file_path)}")
    else:
        status_label.config(text="No file selected")

def process_file():
    try:
        if not source_file_path:
            messagebox.showwarning("No File", "Please select a file before submitting.")
            return

        # Now, source_file_path holds the path to the file that was selected by the user
        dataFile = copy_file(source_file_path, "data")
        resultFile = generate_document(dataFile)
        savedResultsFile = save_file(resultFile, 'results.xlsx', destination_folder="results")
        #print('resultFile', resultFile)

    except Exception as e:
        print("An error occurred:")
        print(str(e))
        traceback.print_exc()
        messagebox.showerror("Error", f"An error occurred: {e}")



# Function to set up the GUI
def setup_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Gene Matcher")
    root.geometry("400x250")

    # Create the file selection button
    drag_drop_label = tk.Label(
        root, text="Drag and drop your Excel file or click below to select it:", pady=10
    )
    drag_drop_label.pack()

    select_button = tk.Button(root, text="Select File", command=select_file)
    select_button.pack(pady=10)

    select_button = tk.Button(root, text="Clear Files", command=clear_files)
    select_button.pack(pady=10)

    # Create the Submit button
    submit_button = tk.Button(root, text="Submit", command=process_file)
    submit_button.pack(pady=20)

    # Label to display status
    global status_label
    status_label = tk.Label(root, text="No file selected", fg="gray")
    status_label.pack(pady=10)

    # Run the GUI event loop
    root.mainloop()

# Run the GUI setup when the main program starts
if __name__ == "__main__":
    setup_gui()
