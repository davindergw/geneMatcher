import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import traceback
from documentGenerator import generate_document
from fileHandler import copy_file, clear_files, save_file, truncate_filename

# Initialize a variable to store the file path
source_file_path = None
status_label = None
status_label = None
prev_width = None  #the width of a window before a change was made to the size of the app window
window_width = None

def adjust_font(event=None):
    """ 
    Adjusts the font size based on the actual window width.
    """
    try:
        min_font_size = 12
        max_font_size = 16
        width_factor = 30

        if root_window.winfo_exists():
            window_width = root_window.winfo_width()
            new_size = window_width // width_factor
            new_size = max(min_font_size, min(new_size, max_font_size))

            new_font = ("Arial", new_size)

            # Apply the new font size to widgets
            select_button.config(font=new_font)
            submit_button.config(font=new_font)
            status_label.config(font=new_font)
            results_button.config(font=new_font)

    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", f"An error occurred in adjust_font: {e}")

def select_file():
    """
    Open a file dialog to allow the user to select an Excel file.
    The selected file's path is stored in the global variable 'source_file_path'.
    """
    try:
        global source_file_path # the global keyword needs to be used so that the global variable defined out of the function can be modified
        global status_label

        filetypes = [
            ("Excel files", "*.xls *.xlsx") #first element is a description of the file type. The next element is a list of permitted file types
        ]
        
        source_file_path = filedialog.askopenfilename(filetypes=filetypes) # Opens the file dialog for the user to select a file. Once the user has selected a file, the file path is returned

        if source_file_path:
            file_name = os.path.basename(source_file_path) #gets the filename on the end of the file path
            file_name_truncated = truncate_filename(file_name)
            status_label.config(text=f"Selected: {file_name_truncated}")
        else:
            status_label.config(text="No file selected")

        # Force Tkinter to refresh layout after file dialog closes
        root_window.update_idletasks() 
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in select_file: {e}"
        messagebox.showerror("Error", error_message)

def submit():
    """
    carries out the tasks that need to be performed when the submit button is pressed:

        - Process the file
        - Record the number of times the user has used the app
        - Display a donation request if uses are a multiple of 50
    """
    try:
        track_uses()
        results_file = process_file()
        display_results_file_link(results_file)
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in submit: {e}"
        messagebox.showerror("Error", error_message)

def track_uses():
    """
    Process the selected file by copying it, generating a document from it, 
    and saving the results to the specified folder.
    """
    try:
        test_variable = True
        
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in track_uses: {e}"
        messagebox.showerror("Error", error_message)


def process_file():
    """
    Process the selected file by copying it, generating a document from it, 
    and saving the results to the specified folder.
    """
    try:
        if not source_file_path: # global keyword is not needed as the global variable is not being modified
            messagebox.showwarning("No File", "Please select a file before submitting.")
            return
        clear_files()
        # Step 1: Copy the selected file to the "imput" folder
        dataFile = copy_file(source_file_path, "data/input")

        # Step 2: Generate a data frame using the copied file
        resultFile = generate_document(source_file_path)

        # Step 3: Save the generated document to the "results" folder
        savedResultsFile = save_file(resultFile, 'results.xlsx', destination_folder="data/results")
        
        # Display a clickable link to open the file
        if savedResultsFile:
            results_button.config(
                state="normal",  # Enable the button
                command=lambda: os.startfile(savedResultsFile)  # Open the file
            )
            results_button.grid() 

        return savedResultsFile
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in process_file: {e}"
        messagebox.showerror("Error", error_message)

def display_results_file_link(results_file):
    """
    """
    try:
        results_button.config(
            state="normal",  # Enable the button
            command=lambda: os.startfile(results_file)  # Open the file
        )
        results_button.grid() 
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in display_results_file_link: {e}"
        messagebox.showerror("Error", error_message)

def setup_gui():
    """
    Set up the main window, create and arrange the widgets using grid,
    and run the Tkinter event loop for the GUI.
    """
    try:
        global select_button, submit_button, status_label, root_window  # Needed for adjust_font function

        root_window = tk.Tk()  # The main window
        root_window.title("Gene Matcher")
        root_window.geometry("400x250")

        # Creates a grid of 9 rows and 3 columns. The weights are equal so the rows and columns take up the same amount of space within their container.
        for row in range(9):  
            root_window.grid_rowconfigure(row, weight=1)

        for column in range(3):  
            root_window.grid_columnconfigure(column, weight=1)

        # Select File button
        select_button = tk.Button(
            master=root_window, # The parent the widget will attach to 
            text="Select File",
            command=select_file,
            anchor="center"  # Keep text centered
        )
        select_button.grid(row=3, column=1, pady=10, sticky="nsew")  # pady provides padding above and below the widget. sticky="nsew" expands the widget in all directions (fills entire cell)

        # Submit button
        submit_button = tk.Button(
            master=root_window,
            text="Submit",
            command=submit,
            width=15
        )
        submit_button.grid(row=4, column=1, pady=10, sticky="nsew")  # Place button in second row, center column

        # Status label
        status_label = tk.Label(
            master=root_window,
            text="No file selected",
            fg="gray",
            anchor="center",
            justify="center",  # Ensures multi-line text is centered
            wraplength=200  # Prevent text from expanding the window (if the window expands this will cause the buttons to resize)
        )
        status_label.grid(row=5, column=1, pady=10, sticky="nsew")  # Place label in third row, center column

        # button for viewing the results file
        global results_button
        results_button = tk.Button(
            master=root_window,
            text="Open Results File",
            state="disabled",  # Initially disabled
            command=lambda: os.startfile(savedResultsFile)  # Opens file when clicked
        )
        results_button.grid(row=6, column=1, pady=10, sticky="nsew")  # Position it below the status label
        results_button.grid_remove()  # Hide the button initially

        # the adjust_font function will be called every time the configure event occurs. The configure event occurs every time the window resizes
        root_window.bind("<Configure>", adjust_font)

        root_window.mainloop()  # Start the Tkinter event loop: An infinite loop that will check for events that have been triggered and redraw the GUI / carry out any function calls in accordance with any events that have occurred
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in setup_gui: {e}"
        messagebox.showerror("Error", error_message)

if __name__ == "__main__": #When a python script is run directly, the value of __name__ is set to __main__
    setup_gui()
