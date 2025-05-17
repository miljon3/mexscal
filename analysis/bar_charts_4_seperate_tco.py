import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

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


all_data = []
for i in range(1, 9):
    file_name = f"averaged_results_type_{i}.csv"
    file_path = os.path.join(folder_path, file_name)
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        all_data.append(None)
        continue

    # Read metadata
    with open(file_path, 'r') as f:
        f.readline()
        type_line = f.readline().strip()
        vehicle_type = type_line.split(",", 1)[1]

    # Read and clean data
    df = pd.read_csv(file_path, skiprows=1, names=["Category", "Average Value"])
    df["Average Value"] = pd.to_numeric(df["Average Value"], errors="coerce")

    try:
        tco = df.loc[df["Category"] == "TCO", "Average Value"].values[0]
        fin_frac = df.loc[df["Category"] == "TCO_financing_frac", "Average Value"].values[0]
        res_frac = df.loc[df["Category"] == "TCO_residual_frac", "Average Value"].values[0]
        opex_fracs = [
            "TCO_maintenance_frac", "TCO_driver_frac", "TCO_battery_frac",
            "TCO_Charging_frac", "TCO_diesel_frac", "TCO_electricity_frac"
        ]
        opex_frac = df.loc[df["Category"].isin(opex_fracs), "Average Value"].sum()

        capex_val = tco * fin_frac
        opex_val = tco * opex_frac
        res_val = tco * res_frac
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
        label = f"Class {class_number} \n ({vehicle_type})"


        all_data.append({
            "label": label,
            "capex": capex_val,
            "opex": opex_val,
            "residual": res_val,
            "tco": tco
        })
    except IndexError as e:
        print(f"⚠️ Missing data in {file_name}: {e}")
        all_data.append(None)

# Generate 4 separate plots
for pair_idx in range(4):
    idx_electric = pair_idx
    idx_diesel = pair_idx + 4

    if all_data[idx_electric] is None or all_data[idx_diesel] is None:
        print(f"⚠️ Skipping Class {pair_idx+1} vs {pair_idx+5} due to missing data")
        continue

    pair_data = [all_data[idx_electric], all_data[idx_diesel]]

    labels = [d["label"] for d in pair_data]
    capex = [d["capex"] for d in pair_data]
    opex = [d["opex"] for d in pair_data]
    residuals = [d["residual"] for d in pair_data]
    tcos = [d["tco"] for d in pair_data]

    fig, ax = plt.subplots(figsize=(8, 5))
    bar_width = 0.2
    x = np.arange(len(labels)) * 0.5



    # Plot bars
    ax.bar(x, opex, bar_width, label="OPEX", color="#55A868")
    ax.bar(x, capex, bar_width, bottom=opex, label="CAPEX", color="#4C72B0")
    ax.bar(x, residuals, bar_width, label="Residual", color="#C44E52")

    # Add percentage labels
    for idx in range(2):
        if tcos[idx] is None:
            continue
        total = tcos[idx]
        opex_pct = opex[idx] / total * 100
        capex_pct = capex[idx] / total * 100
        res_pct = residuals[idx] / total * 100

        ax.text(x[idx], opex[idx] / 2, f"{opex_pct:.0f}%", ha='center', va='center', fontsize=9, color="white")
        ax.text(x[idx], opex[idx] + capex[idx] / 2, f"{capex_pct:.0f}%", ha='center', va='center', fontsize=9, color="white")

        if residuals[idx] < 0:
            ax.text(x[idx], residuals[idx] - total * 0.02, f"{res_pct:.0f}%", ha='center', va='top', fontsize=9, color="black")
        else:
            ax.text(x[idx], opex[idx] + capex[idx] + residuals[idx] / 2, f"{res_pct:.0f}%", ha='center', va='center', fontsize=9, color="black")
    
    for idx in range(2):
        top = opex[idx] + capex[idx]
        ax.text(
            x[idx], 
            top + 0.02*top,
            f"{tcos[idx]/1e6:.2f} Mkr", 
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )
    # Formatting
    ax.set_xlabel("Vehicle Class")
    ax.set_ylabel("TCO [SEK]")
    ax.set_title(f"TCO Breakdown: Class {pair_idx+1} (Electric) vs Class {pair_idx+1} (Diesel)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False)
    #plt.tight_layout() 
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x/1e6:.1f} Mkr"))
    ax.set_ylabel("TCO [Mkr]")

    max_height = max([opex[i] + capex[i] + residuals[i] for i in range(2)])
    ax.set_ylim(top=max_height * 1.2)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()
