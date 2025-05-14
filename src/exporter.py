import os
import pandas as pd
import json


def save_results_to_csv(df, type):
    """ Saves the results to a csv file in the given types directory"""
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

def export_json(foldername, jsonfile):
    """Exports all CSV results in the folder (including subfolders) to a single JSON file with flat key:value rows."""
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    data = []
    for root, _, filenames in os.walk(foldername):
        for filename in filenames:
            if filename.endswith(".csv"):
                filepath = os.path.join(root, filename)
                df = pd.read_csv(filepath)
                records = df.to_dict(orient='records')

                # Flatten if format is [{'Category': ..., 'Value': ...}]
                if set(df.columns) == {"Category", "Value"}:
                    flat_record = {row["Category"]: row["Value"] for row in records}
                    data.append(flat_record)
                else:
                    data.extend(records)  # Normal flat rows

    with open(jsonfile, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data exported to {jsonfile}")


def import_json(foldername, jsonfile):
    """Imports data from a JSON file and saves each record group as CSVs in subfolders based on their Type."""
    if not os.path.exists(jsonfile):
        print(f"{jsonfile} does not exist.")
        return

    # Load the JSON file
    try:
        with open(jsonfile, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from {jsonfile}.")
        return

    if not data:
        print(f"No data found in {jsonfile}.")
        return

    for i, records in enumerate(data):
        if not records:
            continue
        df = pd.DataFrame([records]) if isinstance(records, dict) else pd.DataFrame(records)

        if 'Type' not in df.columns:
            print(f"Skipping entry {i}: missing 'Type' column.")
            continue

        type_value = df['Type'].iloc[0]
        type_dir = os.path.join(foldername, f"Type{type_value}")
        os.makedirs(type_dir, exist_ok=True)

        file_count = len([
            f for f in os.listdir(type_dir)
            if f.startswith("tco_results_Type") and f.endswith(".csv")
        ])
        file_name = f"tco_results_Type{type_value}_{file_count + 1}.csv"
        df.to_csv(os.path.join(type_dir, file_name), index=False)
        print(f"Results saved to {file_name}")

    print(f"Data imported from {jsonfile}")
