import os
import pandas as pd
import matplotlib.pyplot as plt

# Use clean style
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
tco_per_km = []
labels = []

for i in range(1, 9):
    file_name = f"averaged_results_type_{i}.csv"
    file_path = os.path.join(folder_path, file_name)
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue
    with open(file_path, 'r') as f:
        f.readline()
        type_line = f.readline().strip()
        vehicle_type = type_line.split(",", 1)[1]
    df = pd.read_csv(file_path, skiprows=1, names=["Category", "Average Value"])

    try:
        value_str = df.loc[df["Category"] == "TCO per km", "Average Value"].values[0]
        try:
            value = float(value_str.replace(",", "").strip())
        except ValueError:
            print(f"⚠️ Could not convert value '{value_str}' to float in {file_name}")
            value = None
        tco_per_km.append(value)
        if i == 5:
            class_number = 1
        elif i == 6:
            class_number = 2
        elif i == 7:
            class_number = 3
        elif i == 8:
            class_number = 4
        else:
            class_number = i
        labels.append(f"Class {class_number}")
    except IndexError:
        print(f"⚠️ 'TCO per km' not found in {file_name}")
        tco_per_km.append(None)
        labels.append(f"Class {i}")

# Group bars as pairs (Class 1 & 5, etc.)
pairs = [(0, 4), (1, 5), (2, 6), (3, 7)]
bar_width = 0.35
x = range(len(pairs))
colors = ["#4C72B0", "#55A868"]  # Blue & green

# Create two subplots with shared x-axis
fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True, figsize=(10, 7), gridspec_kw={'height_ratios': [1, 2]})

# Define break range
y_break_low = 1.5   # Bottom y-limit of top plot
y_break_high = 3.5  # Top y-limit of bottom plot

for idx, (a, b) in enumerate(pairs):
    val_a = tco_per_km[a]
    val_b = tco_per_km[b]

    # Draw bars in both axes
    ax_top.bar(idx - bar_width/2, val_a, width=bar_width, color=colors[0])
    ax_top.bar(idx + bar_width/2, val_b, width=bar_width, color=colors[1])

    ax_bottom.bar(idx - bar_width/2, val_a, width=bar_width, color=colors[0])
    ax_bottom.bar(idx + bar_width/2, val_b, width=bar_width, color=colors[1])

    # Add value labels (on bottom only for smaller values)
    if val_a < y_break_low:
        ax_bottom.text(idx - bar_width/2, val_a + 0.05, f"{val_a:.2f}", ha='center', va='bottom', fontsize=9)
    else:
        ax_top.text(idx - bar_width/2, val_a + 0.05, f"{val_a:.2f}", ha='center', va='bottom', fontsize=9)

    if val_b < y_break_low:
        ax_bottom.text(idx + bar_width/2, val_b + 0.05, f"{val_b:.2f}", ha='center', va='bottom', fontsize=9)
    else:
        ax_top.text(idx + bar_width/2, val_b + 0.05, f"{val_b:.2f}", ha='center', va='bottom', fontsize=9)

# Hide overlapping spines
ax_top.spines['bottom'].set_visible(False)
ax_bottom.spines['top'].set_visible(False)
ax_top.tick_params(labeltop=False)
ax_bottom.xaxis.tick_bottom()

# Y-axis limits
ax_top.set_ylim(y_break_high, max(tco_per_km) + 0.5)
ax_bottom.set_ylim(0, y_break_low)

# Diagonal break marks
kwargs = dict(marker=[(-1, -1), (1, 1)], markersize=12, linestyle='none', color='k', mec='k', mew=1, label="_nolegend_")
ax_top.plot([0, 1], [0, 0], transform=ax_top.transAxes, **kwargs)
ax_bottom.plot([0, 1], [1, 1], transform=ax_bottom.transAxes, **kwargs)

# Labels & title
ax_bottom.set_xlabel("Class Pairs")
fig.supylabel("TCO per km [SEK/km]", fontsize=12)
ax_top.set_title("Total Cost of Ownership (TCO) per km by Vehicle Class")

# X-ticks and class pair labels
ax_bottom.set_xticks(range(len(pairs)))
ax_bottom.set_xticklabels([f"{labels[a]}" for a, b in pairs])

# Legend
ax_top.legend(["Electric Powertrain", "Diesel Powertrain"], loc="upper right", frameon=False)

ax_top.set_ylim(y_break_high, max(tco_per_km) * 1.15)

# Layout
plt.tight_layout()
plt.subplots_adjust(hspace=0.05)
plt.show()
