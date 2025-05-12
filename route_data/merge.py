import pandas as pd

# Load both CSV files
df1 = pd.read_csv('route_data/Comb_plate_data.csv')
df2 = pd.read_csv('vehicle_weights.csv')

# Rename columns to have the same name if needed
df1 = df1.rename(columns={"License Plate": "Plate"})  # or vice versa

# Merge on the common column (now both are "Plate")
merged = pd.merge(df1, df2, on="Plate", how="left")  # use 'left', 'right', or 'outer' if needed

# Save the result to a new CSV
merged.to_csv('merged.csv', index=False)
