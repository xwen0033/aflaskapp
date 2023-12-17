import os
import pandas as pd
import json


def read_csv_from_path(file_path: str):
    if os.path.isfile(file_path):
        if not file_path.endswith('.csv'):
            raise ValueError("Invalid file format. Please provide a CSV file.")
        data = pd.read_csv(file_path, index_col=0)
        return data
    raise ValueError("Please enter a valid file path and make sure the file exists")


def save_output(output, path):
    with open(path, 'w') as json_file:
        json.dump(output, json_file)
