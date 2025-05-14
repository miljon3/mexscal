import pandas as pd
from pathlib import Path
from collections import defaultdict, Counter

input_folder = Path("src/results")  # Replace with your actual path
output_folder = Path("averages")
output_folder.mkdir(exist_ok=True)

data_by_type = defaultdict(list)
type_labels = defaultdict(list)

# Find all relevant CSVs
for file in input_folder.rglob("tco_results_Type*.csv"):
    folder_name = file.parent.name.lower()
    if folder_name.startswith("type") and folder_name[4:].isdigit():
        type_number = int(folder_name[4:])
        df = pd.read_csv(file)

        # Extract Type label
        type_row = df.loc[df["Category"] == "Type", "Value"].values
        if len(type_row) > 0:
            type_labels[type_number].append(type_row[0])

        # Clean and ensure correct format
        df = df.set_index("Category")
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")  # Convert to numeric
        data_by_type[type_number].append(df["Value"])

# Compute means and write CSVs with Type label at top
for type_num, series_list in data_by_type.items():
    combined_df = pd.concat(series_list, axis=1)
    mean_series = combined_df.mean(axis=1, skipna=True)  # Mean across columns

    # Create output DataFrame with Type at the top
    output_df = pd.DataFrame(columns=["Category", "Average Value"])
    
    # Determine the most common Type string
    type_counts = Counter(type_labels[type_num])
    most_common_type = type_counts.most_common(1)[0][0] if type_counts else "Unknown"

    # Add Type as the first row
    output_df.loc[0] = ["Type", most_common_type]

    # Add the rest of the averaged values
    for i, (category, value) in enumerate(mean_series.items(), start=1):
        output_df.loc[i] = [category, value]

    # Write to CSV
    output_df.to_csv(output_folder / f"averaged_results_type_{type_num}.csv", index=False)
