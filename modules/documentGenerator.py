""" 
This file is part of Gene Matcher.
Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See LICENSE file for details: https://creativecommons.org/licenses/by-nc/4.0/
"""
import config
import os
import pandas as pd
import traceback
from tkinter import messagebox
import copy
from .fileHandler import get_file_extension

"""
FUNCTIONS

def rename_columns
def clean_dataframe_to_integers
def format_cell
def read_and_clean_column
def find_matching_strings
def initialize_matching_strings_positions
def find_positions
def populate_positions
def convert_to_dataframe
def generate_document
"""

def rename_columns(dataframe):
    """
    Renames the first two columns of the dataframe to 'Set 1' and 'Set 2'.
    """
    try:
        column_names = dataframe.columns
        column_list = list(column_names)  # Convert to a list
        column_count = len(column_list)  # Get the number of columns

        if column_count < 2:
            messagebox.showwarning("Insufficient Columns", "The spreadsheet must contain at least two columns of data.")
            raise ValueError("The dataframe must contain at least two columns.") #Will trigger the exception block. Value error is used when the argument is the right data type, but has the wrong value

        first_column = column_list[0]
        second_column = column_list[1]

        rename_dict = {first_column: "Set 1", second_column: "Set 2"}
        dataframe = dataframe.rename(columns=rename_dict)

        return dataframe
    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in rename_columns: {e}"
        messagebox.showerror("Error", error_message)



def clean_dataframe_to_integers(dataframe):
    
    """
    Cleans the dataframe so all numeric values are converted to integers.
    """
    try:
        for column in dataframe.columns:
            if pd.api.types.is_numeric_dtype(dataframe[column]): # pd.api.types is refering to a submodule within a sub-module is_numeric_dtype checks if the column data is numeric
                dataframe[column] = dataframe[column].fillna(0) #empty data is filled in with a 0
                dataframe[column] = dataframe[column].astype(int) # column data is converted into an integer
        return dataframe
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred in clean_dataframe_to_integers: {e}"
        messagebox.showerror("Error", error_message)

def format_cell(value):
    """
    Cleans the value of a cell so it is formatted correctly:

        - Converts any numerical value to a string
    """
    try:
        if isinstance(value, (int, float)):  # Ensure value is numeric
            if value == int(value):  #int() will convert decimal to an integer. the check on this line will return true if the value is an integer or a decimal with no numbers after the decimal place (e.g. 10 or 10.0)
                return str(int(value))  # Convert to int and then string
            else:
                return str(value)  # Keep decimals if needed
        else:
            return str(value)  # Convert non-numeric values directly to strings
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occured in format_cell: {e}"
        messagebox.showerror("Error", error_message)

def read_and_clean_column(df, column_name):
    """
    Extracts and cleans column data from an excel file:
        - Removes empty cells
        - Converts numeric values to string
        - Remove duplicate cells
    """
    try:
        column_series = df[column_name] # returns a panda series, which is an array like data structure
        cleaned_series = column_series.dropna() # removes empty cells from the series
        string_series = cleaned_series.apply(format_cell) # Converts numeric values to string
        unique_values = string_series.unique() #removes duplicates
        column_list = list(unique_values) # puts the values into a list: an array like structure that is easier to manipulate than a normal array

        return column_list
    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in read_and_clean_column: {e}"
        messagebox.showerror("Error", error_message)

def find_matching_strings(column_1_strings, column_2_strings):
    """
    Identifies matching strings between two columns.
    """
    try:
        matching_strings = []
        
        # Iterate through each string in column_1_strings
        for string in column_1_strings:
            # Check if the string is present in column_2_strings
            if string in column_2_strings:
                matching_strings.append(string)  # Append matching string to the result list
        
        return matching_strings
    
    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in find_matching_strings: {e}"
        messagebox.showerror("Error", error_message)


def initialize_matching_strings_positions(matching_strings):
    """
    Creates an array of objects to store matching strings and their positions in both columns.
    """
    try:
        result = []

        for string in matching_strings:
            matching_string_info = {
                "Gene": string,
                "Column 1": [],
                "Column 2": []
            }
            
            result.append(matching_string_info)
        
        return result

    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in initialize_matching_strings_positions: {e}"
        messagebox.showerror("Error", error_message)


def find_positions(dataframe, column_name, matching_string):
    """
    Finds the row indices where a matching string appears in a given column.
    """
    try:
        column_data = dataframe[column_name]
        matching_indices = []

        matching_string = str(matching_string)

        for index, value in enumerate(column_data): #enumerate allows you to loop through each item in a list and at each iteration have access to the value of the item and its index within the list
            value_as_string = str(value)
            if value_as_string == matching_string:
                adjusted_index = index + 2 # this needs to be the value of the row number in excel. Given that rows in excel are not zero indexed and the first row contains the column headinds, you need increase the list index by two
                matching_indices.append(adjusted_index)

        return matching_indices
    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in find_positions: {e}"
        messagebox.showerror("Error", error_message)

def populate_positions(dataframe, matching_strings_positions_empty):
    """
    Populates the positions of matching strings in both columns.
    """
    try:
        matching_strings_positions_copy = copy.deepcopy(matching_strings_positions_empty) #Stops matching_strings_positions_empty from being altered
        for obj in matching_strings_positions_copy:
            obj["Column 1"] = find_positions(dataframe, "Set 1", obj["Gene"])
            obj["Column 2"] = find_positions(dataframe, "Set 2", obj["Gene"])

        return matching_strings_positions_copy
    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in populate_positions: {e}"
        messagebox.showerror("Error", error_message)

def convert_to_dataframe(matching_strings_positions):
    """
    Converts matching_strings_positions into a DataFrame.
    """
    try:
        dataframe = pd.DataFrame(matching_strings_positions)
        return dataframe
    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in convert_to_dataframe: {e}"
        messagebox.showerror("Error", error_message)

def generate_document(source_file_path):
    """
    Processes the input file to identify matching strings and returns a DataFrame
    containing matching strings and their positions.
    """
    try:
        print('=================================================')
        debug = False
        file_extension = get_file_extension(source_file_path)

        if file_extension in [".xls", ".xlsx"]:
            df_to_analyse = pd.read_excel(source_file_path)
        elif file_extension == ".ods":
            df_to_analyse = pd.read_excel(source_file_path, engine="odf")
        else:
            raise ValueError("Unsupported file format")

        df_to_analyse = rename_columns(df_to_analyse)
        df_to_analyse = clean_dataframe_to_integers(df_to_analyse)
        column1_strings = read_and_clean_column(df_to_analyse, "Set 1")
        column2_strings = read_and_clean_column(df_to_analyse, "Set 2")
        matching_strings = find_matching_strings(column1_strings, column2_strings)
        matching_strings_positions_empty = initialize_matching_strings_positions(matching_strings)
        matching_strings_positions_populated = populate_positions(df_to_analyse, matching_strings_positions_empty)
        matching_strings_df = convert_to_dataframe(matching_strings_positions_populated)

        if debug:
            print('df_to_analyse\n', df_to_analyse, '\n')
            print('COLUMN 1\n', column1_strings, '\n')
            print('COLUMN 2\n', column2_strings, '\n')
            print('Matching Strings\n', matching_strings, '\n')
            print('matching_strings_positions_empty\n', matching_strings_positions_empty, '\n')
            print('matching_strings_positions_populated\n', matching_strings_positions_populated, '\n')
            print('matching_strings_df\n', matching_strings_df)
        else:
            pass
            print('\n Matching Genes:')
            print('\n', matching_strings_df)
        return matching_strings_df
    except Exception as e:
        traceback.print_exc()
        error_message = f"Error in generate_document: {e}"
        messagebox.showerror("Error", error_message)
