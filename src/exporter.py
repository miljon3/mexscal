import os
import pandas as pd
import json


def save_results_to_csv(df, type):
    results_dir = "src/results"
    # Check if the directory exists, if not create it
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    # Check the type and create a subdirectory for each type
    type_dir = os.path.join(results_dir, f"Type{type}")
    if not os.path.exists(type_dir):
        os.makedirs(type_dir)
    # Save the file with a unique name based on the type and number of files already in the directory
    # Count the number of files in the directory that start with tco_results_Type and end with .csv
    # and add 1 to the count to create a unique name
    file_count = len([f for f in os.listdir(type_dir) if f.startswith("tco_results_Type") and f.endswith(".csv")])
    file_name = f"tco_results_Type{type}_{file_count + 1}.csv"
    df.to_csv(os.path.join(type_dir, file_name), index=False)
    print(f"Results saved to {file_name}")
     