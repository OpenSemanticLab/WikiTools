import os
import pandas as pd
from pathlib import Path
import json

# problem with escaping of uri's, reimplementation of dict_to_json below
def dictdf_to_json(dictionary={}, name_of_json="sample", optional_orient=None, optional_path=None):
    if optional_orient is None:
        df_json = pd.DataFrame.from_dict(dictionary)
    else:
        df_json = pd.DataFrame.from_dict(dictionary, orient=optional_orient)
    if optional_path is None: 
        filepath_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", f"{name_of_json}.json")
        print(filepath_json)
    else: 
        Path(optional_path)    
    # filepath_json.parent.mkdir(parents=True, exist_ok=True)  
    df_json.to_json(filepath_json)  

# export dictionary as json file
def dict_to_json(dictionary={}, name_of_json="sample", optional_path=None):
    if optional_path is None: 
        filepath_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", f"{name_of_json}.json")
        with open(filepath_json, "w") as outfile:
            json.dump(dictionary, outfile)
            print(name_of_json, "created as json using filepath: \n", filepath_json, "\n")
    else: 
        optional_filepath = Path(optional_path)    
        with open(optional_filepath, "w") as outfile:
            json.dump(dictionary, outfile)
            print(name_of_json, "created as json using optional filepath: \n", optional_filepath, "\n")
 
# import data from json file as dictonary
def json_to_dict(name_of_json="sample", optional_path=None):
    if optional_path is None: 
        filepath_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", f"{name_of_json}.json")
        with open(filepath_json) as json_file:
            print(name_of_json, "loaded using filepath:\n", filepath_json, "\n")
            return json.load(json_file)
    else:
        optional_filepath = Path(optional_path)
        with open(optional_path) as json_file:
            print(name_of_json, "loaded using optional filepath:\n", optional_filepath)
            return json.load(json_file)