import pandas as pd
from pathlib import Path
from collections import defaultdict

input_folder = Path("results")  # Replace with your actual path
output_folder = Path("averages")
output_folder.mkdir(exist_ok=True)

data_by_type = defaultdict(list)

# Find all relevant CSVs
for file in input_folder.rglob("tco_results_Type*.csv"):
    folder_name = file.parent.name.lower()
    if folder_name.startswith("type") and folder_name[4:].isdigit():
        type_number = int(folder_name[4:])
        df = pd.read_csv(file)

        # Clean and ensure correct format
        df = df.set_index("Category")
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")  # Convert to numeric
        data_by_type[type_number].append(df["Value"])

# Compute means
for type_num, series_list in data_by_type.items():
    combined_df = pd.concat(series_list, axis=1)
    mean_series = combined_df.mean(axis=1, skipna=True)  # Mean across columns
    mean_series.to_csv(output_folder / f"averaged_results_type_{type_num}.csv", header=["Average Value"])
