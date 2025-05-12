import os
import pandas as pd
import matplotlib.pyplot as plt

folder_path = "averages"  # adjust this if needed

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
        value = df.loc[df["Category"] == "TCO", "Average Value"].values[0]
        tco_per_km.append(value)
        labels.append(f"Type {i}")
    except IndexError:
        print(f"⚠️ 'TCO per km' not found in {file_name}")
        tco_per_km.append(None)
        labels.append(f"Type {i}")

# Group bars: (1,5), (2,6), ...
pairs = [(0, 4), (1, 5), (2, 6), (3, 7)]

bar_width = 0.35
x = range(len(pairs))

fig, ax = plt.subplots(figsize=(10, 6))

for idx, (a, b) in enumerate(pairs):
    if a < len(tco_per_km) and b < len(tco_per_km):
        ax.bar(idx - bar_width/2, tco_per_km[a], width=bar_width, label=labels[a])
        ax.bar(idx + bar_width/2, tco_per_km[b], width=bar_width, label=labels[b])

ax.set_xlabel("Type Pairs")
ax.set_ylabel("TCO per km")
ax.set_title("TCO per km Comparison")
ax.set_xticks(range(len(pairs)))
ax.set_xticklabels([f"{labels[a]} & {labels[b]}" for a, b in pairs])
ax.legend()
plt.tight_layout()
plt.show()
