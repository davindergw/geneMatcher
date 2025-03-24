""" 
This file is part of Gene Matcher.
Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See LICENSE file for details: https://creativecommons.org/licenses/by-nc/4.0/
"""
import config
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import traceback
import webbrowser
from .documentGenerator import generate_document
from .fileHandler import clear_files, save_file, truncate_filename, get_file_extension
from .userDataHandler import track_use
import pandas as pd

"""
FUNCTIONS

def adjust_font
def select_file
def submit
def process_file
def display_donation_reminder
def display_results_file_link
def display_donation_options
def setup_gui
"""

# Global variables
source_file_path = None
status_label = None
paypal_url = 'https://paypal.me/Davinder321?country.x=GB&locale.x=en_GB'


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
            new_size_initial = window_width // width_factor
            new_size = max(min_font_size, min(new_size_initial, max_font_size))
            new_font = ("Arial", new_size)

            select_button.config(font=new_font)
            submit_button.config(font=new_font)
            status_label.config(font=new_font)
            contact_details.config(font=new_font)
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
        global source_file_path # the global keyword makes sure the variable refers to the global variable already created, rather than having a new local variable created
        global status_label

        filetypes = [
            ("Spreadsheet files", "*.xls *.xlsx *.ods") #first element is a description of the file type. The next element is a list of permitted file types
        ]
        
        source_file_path = filedialog.askopenfilename(filetypes=filetypes) # Opens the file dialog for the user to select a file and blocks the program execution. Once the user has selected a file, the file path is returned

        if source_file_path:
            file_name = os.path.basename(source_file_path) #gets the filename on the end of the file path
            file_name_truncated = truncate_filename(file_name)
            status_label.config(text=f"Selected: {file_name_truncated}") #f strings allow you to insert variables into strings
            results_button.config(state=tk.DISABLED)
        else:
            status_label.config(text="No file selected")

        # refresh layout after file dialog closes (needed to fix a bug)
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
        numberOfUses = track_use()
        results_file = process_file()

        if numberOfUses % 50 == 0:
            display_donation_reminder(numberOfUses)

        display_results_file_link(results_file)
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in submit: {e}"
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
        clear_files() #Clear old files from the folders
        resultFile = generate_document(source_file_path) # Generate a data frame using the copied file
        
        # Saving the file
        file_extension = get_file_extension(source_file_path)
        savedResultsFile = save_file(resultFile, f'results{file_extension}', config.RESULTS_FOLDER)

        # Configure the results button to open the file
        if savedResultsFile:
            results_button.config(
                command=lambda: os.startfile(savedResultsFile)  # Open the file
            )

        return savedResultsFile
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in process_file: {e}"
        messagebox.showerror("Error", error_message)

def display_donation_options():
    """
    Displays a pop up containing links to Buy Me a Coffe and Paypal donate
    """
    try:
        popup = tk.Toplevel(root_window)
        popup.title("Donation Options")

        # Get the dimensions of the main window
        root_x = root_window.winfo_x()
        root_y = root_window.winfo_y()
        root_width = root_window.winfo_width()
        root_height = root_window.winfo_height()

        popup_width = 300
        popup_height = 130

        # Calculate the position at centre of main window
        pos_x = root_x + (root_width // 2) - (popup_width // 2)
        pos_y = root_y + (root_height // 2) - (popup_height // 2)

        # Apply calculated position
        popup.geometry(f"{popup_width}x{popup_height}+{pos_x}+{pos_y}")

        label = tk.Label(
            popup,
            text="Support the developer via Buy Me a Coffee or PayPal Donate:",
            font=("Arial", 12),
            fg="black",
            wraplength=280,
            justify="center"
        )
        label.pack(pady=5)

        # Button to open donation link
        coffee_button = tk.Button(
            popup,
            text="☕ Buy Me a Coffee",
            bg="#ffd966",
            cursor="hand2",
            command=lambda: [webbrowser.open("https://buymeacoffee.com/davinder"), popup.destroy()] #lambada lets you define anonymous funcitons
        )
        coffee_button.pack(pady=5)

        # "Maybe Later" button
        paypal_button = tk.Button(
            popup,
            text="💳 Paypal Donate",
            bg="#ffd966",
            cursor="hand2",
            command=lambda: [webbrowser.open(paypal_url), popup.destroy()] #lambada lets you define anonymous funcitons
        )
        paypal_button.pack(pady=5)
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in display_donation_options: {e}"
        messagebox.showerror("Error", error_message)

def display_donation_reminder(numberOfUses):
    """
    Displays a pop up telling the user how many times they have used the app
    and reminding them to consider donating
    """
    try:
        popup = tk.Toplevel(root_window)
        popup.title("Please Consider Donating")

        # Get the dimensions of the main window
        root_x = root_window.winfo_x()
        root_y = root_window.winfo_y()
        root_width = root_window.winfo_width()
        root_height = root_window.winfo_height()

        popup_width = 400
        popup_height = 280

        # Calculate the position at centre of main window
        pos_x = root_x + (root_width // 2) - (popup_width // 2)
        pos_y = root_y + (root_height // 2) - (popup_height // 2)

        # Apply calculated position
        popup.geometry(f"{popup_width}x{popup_height}+{pos_x}+{pos_y}")

        label1 = tk.Label(
            popup,
            text=f"You have used Gene Matcher {numberOfUses} times!",
            font=("Arial", 15, "bold"),
            fg="black",
            wraplength=380,
            justify="center"
        )
        label1.pack(pady=5)

        label2 = tk.Label(
            popup,
            text="This app is free and open-source, but took time to build. If you find it useful, please consider supporting the developer.\n\n"
                  "Support via Buy Me a Coffee or PayPal Donate:",
            font=("Arial", 12),
            fg="black",
            wraplength=380,
            justify="center"
        )
        label2.pack(pady=5)

        # Button to open donation link
        coffee_button = tk.Button(
            popup,
            text="☕ Buy Me a Coffee",
            bg="#ffd966", #gets the background colour for the popup window
            cursor="hand2",
            command=lambda: [webbrowser.open("https://buymeacoffee.com/davinder"), popup.destroy()] #lambada lets you define anonymous funcitons
        )
        coffee_button.pack(pady=5)

         # Button to open donation link
        paypal_button = tk.Button(
            popup,
            text="💳 Paypal Donate",
            bg="#ffd966", #gets the background colour for the popup window
            cursor="hand2",
            command=lambda: [webbrowser.open(paypal_url), popup.destroy()] #lambada lets you define anonymous funcitons
        )
        paypal_button.pack(pady=5)

        # "Maybe Later" button
        maybe_later_button = tk.Button(
            popup, text="Maybe Later", 
            bg=popup.cget("bg"),
            cursor="hand2",
            command=popup.destroy)
        maybe_later_button.pack(pady=5)
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in display_donation_reminder: {e}"
        messagebox.showerror("Error", error_message)

def display_results_file_link(results_file):
    """
    Dispays the button to see the results file
    """
    try:
        results_button.config(
            state="normal",  # Enable the button
            command=lambda: os.startfile(results_file)  # Open the file
        )
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in display_results_file_link: {e}"
        messagebox.showerror("Error", error_message)

def setup_gui():
    """
    - Sets up the main window
    - Creates and arrange the widgets
    - Runs the event loop
    """
    try:
        global select_button, submit_button, status_label, results_button, contact_details, root_window  # Needed for adjust_font function

        root_window = tk.Tk()  # The main window
        root_window.title("Gene Matcher")
        root_window.geometry("500x500")

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
        submit_button.grid(row=4, column=1, pady=10, sticky="nsew") 

        # Status label
        status_label = tk.Label(
            master=root_window,
            text="No file selected",
            fg="gray",
            anchor="center",
            justify="center",  # Ensures text is centered
            wraplength=200  # Prevent text from expanding the window (if the window expands this will cause the buttons to resize)
        )
        status_label.grid(row=5, column=1, pady=10, sticky="nsew") 

        # button for viewing the results file
        results_button = tk.Button(
            master=root_window,
            text="Open Results File",
            state="disabled", 
            command=lambda: os.startfile(savedResultsFile)  # Opens file when clicked
        )
        results_button.grid(row=6, column=1, pady=10, sticky="nsew")  

        #Donations button
        donate_button = tk.Button(
            master=root_window,
            text="Support the Developer 💖", 
            font=("Arial", 12, "bold"),   
            bg="#ffd966",  
            fg="black",   
            cursor="hand2",
            command=display_donation_options
        )
        donate_button.grid(row=7, column=1, pady=10, sticky="nsew")

        #Contact Details
        contact_details = tk.Label(
            master=root_window,
            text="Contact the developer at: pythongenematcher@gmail.com" +
            "\n\n Find instructions for downloading the latest version of Gene Matcher at:",
            fg="black",
            font=("Arial", 10),   
            anchor="center",
            justify="center",   
            wraplength=400  
        )
        contact_details.grid(row=8, column=1, pady=10, sticky="nsew") 

        # Create a Text widget with Arial font
        contact_text = tk.Text(
            root_window,
            height=3,
            width=50,
            wrap="word",
            borderwidth=0,
            bg=root_window.cget("bg"),
            font=("Arial", 10)
        )
        contact_text.insert("1.0", "Contact the developer at:\npythongenematcher@gmail.com\n\n")
        contact_text.insert("end", "Instructions for downloading the latest version of Gene Matcher can be found at: ")

        # Insert the clickable link
        contact_text.insert("end", "https://github.com/davindergw/geneMatcher/blob/main/README.md", "link")

        # Apply center alignment using a tag
        contact_text.tag_configure("center", justify="center")
        contact_text.tag_add("center", "1.0", "end")

        # Make the text uneditable
        contact_text.config(state="disabled")

        # Configure the hyperlink tag
        contact_text.tag_configure("link", foreground="blue", underline=True)
        contact_text.tag_bind("link", "<Button-1>", lambda e: webbrowser.open("https://github.com/davindergw/geneMatcher"))

        # Place the widget using grid instead of pack
        contact_text.grid(row=8, column=1, pady=10, sticky="nsew")

        root_window.bind("<Configure>", adjust_font) # the adjust_font function will be called every time the configure event occurs. The configure event occurs every time the window resizes
        root_window.mainloop()  # Start the Tkinter event loop: An infinite loop that will check for events that have been triggered and redraw the GUI / carry out any function calls in accordance with any events that have occurred
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in setup_gui: {e}"
        messagebox.showerror("Error", error_message)


