import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Styling
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "font.family": "serif",
})

folder_path = "averages"
labels = []
tcos = []

# OPEX components and colors
opex_keys = [
    ("TCO_maintenance_frac", "#C1C1C1"),
    ("TCO_driver_frac", "#55A868"),
    ("TCO_battery_frac", "#937860"),
    ("TCO_Charging_frac", "#64B5CD"),
    ("TCO_diesel_frac", "#DA8BC3"),
    ("TCO_electricity_frac", "#B2912F")
]

opex_components = {key: [] for key, _ in opex_keys}

for i in range(1, 9):
    file_name = f"averaged_results_type_{i}.csv"
    file_path = os.path.join(folder_path, file_name)
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue

    df = pd.read_csv(file_path, skiprows=1, names=["Category", "Average Value"])

    try:
        tco = df.loc[df["Category"] == "TCO", "Average Value"].values[0]
        tcos.append(tco)

        # Compute only the relevant opex components
        for key, _ in opex_keys:
            frac = df.loc[df["Category"] == key, "Average Value"].values[0]
            opex_components[key].append(tco * frac)

        # Label
        if i in range(5, 9):
            labels.append(f"Class {i}\n(Diesel)")
        else:
            labels.append(f"Class {i}\n(Electric)")

    except IndexError as e:
        print(f"⚠️ Missing data in {file_name}: {e}")
        tcos.append(None)
        for key, _ in opex_keys:
            opex_components[key].append(None)
        labels.append(f"Class {i}")

# Reorder all lists
reorder_indices = [0, 4, 1, 5, 2, 6, 3, 7]
labels = [labels[i] for i in reorder_indices]
tcos = [tcos[i] for i in reorder_indices]
for key in opex_components:
    opex_components[key] = [opex_components[key][i] for i in reorder_indices]

# Calculate total cost for percentage calculation (check if tcos is not empty)
total_cost = []
for i in range(len(labels)):
    # Calculate the total cost for each class
    total = sum([opex_components[key][i] if opex_components[key][i] is not None else 0 for key in opex_components])
    total_cost.append(total)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
bar_height = 0.6
y = range(len(labels))

# Stack bars
bottom = [0] * len(labels)
for key, color in opex_keys:
    values = opex_components[key]
    label = key.replace("TCO_", "").replace("_frac", "").capitalize()

    if label == "Battery":
        label = "Battery Replacement"
    if label == "Charging":
        label = "Charging Infrastructure"
    ax.barh(y, values, bar_height, left=bottom, label=label, color=color)
    bottom = [b + (v if v is not None else 0) for b, v in zip(bottom, values)]


# Axis & Legend
ax.set_ylabel("Vehicle Class")
ax.set_xlabel("OPEX [Mkr]")
ax.set_title("OPEX Breakdown by Vehicle Class")
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.legend(loc="lower right", frameon=False)  # Legend at the bottom-right corner

# Format the x-axis labels
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x/1e6:.1f} Mkr"))

# Clean up
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.show()
