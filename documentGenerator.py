import os
import pandas as pd
import traceback

def generate_document(input_file, output_folder="results"):
    try:

        
        df = pd.read_excel(input_file)
        strings_to_remove = ['BLANK', '']

        first_column = extract_column(df, 0)
        first_column_unique_cells = remove_repeating_strings(first_column)
        first_column_with_reduntant_cells_removed = remove_matching_strings(first_column_unique_cells, strings_to_remove)

        second = extract_column(df, 0)
        second_unique_cells = remove_repeating_strings(second)
        second_with_reduntant_cells_removed = remove_matching_strings(second_unique_cells, strings_to_remove)
        matching_genes = find_common_strings(first_column_with_reduntant_cells_removed, second_with_reduntant_cells_removed)
        print("=========================")
        print('matching_genes', matching_genes)
        return df

    except Exception as e:
        # Print the full error message and stack trace to the console
        print("An error occurred:")
        print(str(e))
        traceback.print_exc()  # This will print the stack trace to the console
        return None

def extract_column(df, column_number):
    return df.iloc[:, column_number].astype(str).tolist()

def remove_repeating_strings(arr):
    return list(dict.fromkeys(arr))

def remove_matching_strings(arr, strings_to_remove):
    return [string for string in arr if string not in strings_to_remove]



def find_common_strings(array1, array2):
    """
    Finds the strings that appear in both input arrays and returns them as a new array.
    
    :param array1: List of strings (first array)
    :param array2: List of strings (second array)
    :return: List of strings found in both arrays
    """
    # Use set intersection to find common elements
    common = list(set(array1) & set(array2))
    return common