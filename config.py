""" 
This file is part of Gene Matcher.
Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See LICENSE file for details: https://creativecommons.org/licenses/by-nc/4.0/
"""
import os

APP_DATA_FOLDER = os.path.join(os.environ["APPDATA"], "GeneMatcher")

DATA_FOLDER = os.path.join(APP_DATA_FOLDER, "data")
INPUT_FOLDER = os.path.join(DATA_FOLDER, "input")
RESULTS_FOLDER = os.path.join(DATA_FOLDER, "results")
USER_FOLDER = os.path.join(DATA_FOLDER, "user")

NUMBER_OF_USES_FILE = os.path.join(USER_FOLDER, "number_of_uses.txt")

ALL_FOLDERS = [APP_DATA_FOLDER, DATA_FOLDER, INPUT_FOLDER, RESULTS_FOLDER, USER_FOLDER]
