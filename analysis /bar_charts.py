import os
import pandas as pd
import matplotlib.pyplot as plt

# Use a clean style
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "font.family": "serif",  # Try "sans-serif" for a modern look
})

folder_path = "averages"
tco_per_km = []
labels = []

for i in range(1, 9):
    file_name = f"averaged_results_type_{i}.csv"
    file_path = os.path.join(folder_path, file_name)
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue
    df = pd.read_csv(file_path, skiprows=1, names=["Category", "Average Value"])
    try:
        value = df.loc[df["Category"] == "TCO per km", "Average Value"].values[0]
        tco_per_km.append(value)
        labels.append(f"Class {i}")
    except IndexError:
        print(f"⚠️ 'TCO per km' not found in {file_name}")
        tco_per_km.append(None)
        labels.append(f"Class {i}")

# Group bars
pairs = [(0, 4), (1, 5), (2, 6), (3, 7)]

bar_width = 0.35
x = range(len(pairs))
colors = ["#4C72B0", "#55A868"]  # Muted blue & green

fig, ax = plt.subplots(figsize=(10, 6))

for idx, (a, b) in enumerate(pairs):
    if a < len(tco_per_km) and b < len(tco_per_km):
        val_a = tco_per_km[a]
        val_b = tco_per_km[b]
        
        bar1 = ax.bar(idx - bar_width / 2, val_a, width=bar_width, color=colors[0])
        bar2 = ax.bar(idx + bar_width / 2, val_b, width=bar_width, color=colors[1])

        # Add value labels
        if val_a is not None:
            ax.text(idx - bar_width / 2, val_a + 0.01, f"{val_a:.2f}", ha='center', va='bottom', fontsize=9)
        if val_b is not None:
            ax.text(idx + bar_width / 2, val_b + 0.01, f"{val_b:.2f}", ha='center', va='bottom', fontsize=9)


# Labels & title
ax.set_xlabel("Class Pairs")
ax.set_ylabel("TCO per km [SEK/km]")
ax.set_title("Total Cost of Ownership (TCO) per km by Vehicle Class")

# Ticks and labels
ax.set_xticks(range(len(pairs)))
ax.set_xticklabels([f"{labels[a]} & {labels[b]}" for a, b in pairs])

# Clean up legend (only show 2 items)
ax.legend(["Electric Powertrain", "Diesel Powertrain"], loc="upper right", frameon=False)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Adjust layout
plt.tight_layout()
plt.show()
