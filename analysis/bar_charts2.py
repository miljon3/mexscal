import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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
capex, opex, residuals, tcos = [], [], [], []
labels = []

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

        # Extract fractions
        fin_frac = df.loc[df["Category"] == "TCO_financing_frac", "Average Value"].values[0]
        res_frac = df.loc[df["Category"] == "TCO_residual_frac", "Average Value"].values[0]

        opex_fracs = [
            "TCO_maintenance_frac", "TCO_driver_frac", "TCO_battery_frac",
            "TCO_Charging_frac", "TCO_diesel_frac", "TCO_electricity_frac"
        ]
        opex_frac = sum(df.loc[df["Category"].isin(opex_fracs), "Average Value"].values)

        # Calculate components
        capex_val = tco * fin_frac
        opex_val = tco * opex_frac
        res_val = tco * res_frac

        capex.append(capex_val)
        opex.append(opex_val)
        residuals.append(res_val)
        if i in range(5,9): 
            labels.append(f"Class {i} \n (Diesel)")
        else:
            labels.append(f"Class {i} \n (Electric)")
    except IndexError as e:
        print(f"⚠️ Missing data in {file_name}: {e}")
        capex.append(None)
        opex.append(None)
        residuals.append(None)
        tcos.append(None)
        labels.append(f"Class {i}")

# Define the new order
reorder_indices = [0, 4, 1, 5, 2, 6, 3, 7]  # 0-based index: Class 1 = index 0, Class 5 = index 4, etc.

# Reorder all the lists accordingly
labels = [labels[i] for i in reorder_indices]
capex = [capex[i] for i in reorder_indices]
opex = [opex[i] for i in reorder_indices]
residuals = [residuals[i] for i in reorder_indices]
tcos = [tcos[i] for i in reorder_indices]

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.6
x = range(len(labels))

# Plot bars
bar_opex = ax.bar(x, opex, bar_width, label="OPEX", color="#55A868")
bar_capex = ax.bar(x, capex, bar_width, bottom=opex, label="CAPEX", color="#4C72B0")

# Residual (can be negative)
bar_res = ax.bar(x, residuals, bar_width, label="Residual", color="#C44E52")

# Add percentage labels
for idx in range(len(labels)):
    if tcos[idx] is None:
        continue

    total = tcos[idx]
    opex_pct = opex[idx] / total * 100
    capex_pct = capex[idx] / total * 100
    res_pct = residuals[idx] / total * 100

    # OPEX label
    ax.text(x[idx], opex[idx] / 2, f"{opex_pct:.0f}%", ha='center', va='center', fontsize=9, color="white")

    # CAPEX label
    ax.text(x[idx], opex[idx] + capex[idx] / 2, f"{capex_pct:.0f}%", ha='center', va='center', fontsize=9, color="white")

    # Residual label (place above or below depending on sign)
    if residuals[idx] < 0:
        ax.text(x[idx], residuals[idx] - total * 0.02, f"{res_pct:.0f}%", ha='center', va='top', fontsize=9, color="black")
    else:
        ax.text(x[idx], opex[idx] + capex[idx] + residuals[idx] / 2, f"{res_pct:.0f}%", ha='center', va='center', fontsize=9, color="black")

"""
# Add TCO total labels above the bars
for idx in range(len(labels)):
    if tcos[idx] is None:
        continue

    total = opex[idx] + capex[idx] + residuals[idx]
    ax.text(
        x[idx], 
        total + max(tcos) * 0.02,  # small offset for spacing
        f"{tcos[idx]/1e6:.1f} Mkr",
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold',
        color='black'
    )
"""


# Formatting
ax.set_xlabel("Vehicle Class")
ax.set_ylabel("TCO [SEK]")
ax.set_title("TCO Breakdown by Vehicle Class")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc="upper right", frameon=False)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x/1e6:.1f} Mkr"))
ax.set_ylabel("TCO [Mkr]")

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()
