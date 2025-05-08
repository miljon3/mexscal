import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi

def merge_csvs_per_type(base_folder):
    merged_data = []
    for subdir in os.listdir(base_folder):
        subdir_path = os.path.join(base_folder, subdir)
        if os.path.isdir(subdir_path) and subdir.startswith("Type"):
            dfs = []
            for file in os.listdir(subdir_path):
                if file.endswith(".csv"):
                    df = pd.read_csv(os.path.join(subdir_path, file))
                    df.columns = df.columns.str.strip()
                    df = df.set_index("Category").T
                    dfs.append(df)
            if dfs:
                merged_df = pd.concat(dfs, ignore_index=True)
                merged_df["Type"] = subdir
                merged_data.append(merged_df)
    return pd.concat(merged_data, ignore_index=True)

def preprocess(df):
    for col in df.columns:
        if col != "Type":
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def compare_key_metrics(df, key_metrics):
    melted = df.melt(id_vars=["Type"], value_vars=key_metrics, var_name="Metric", value_name="Value")
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Metric", y="Value", hue="Type", data=melted)
    plt.title("Comparison of Key Metrics Across Types")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def radar_chart(df, metrics):
    categories = metrics
    N = len(categories)

    for i in range(len(df)):
        values = df.loc[i, categories].values.flatten().tolist()
        values += values[:1]
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        plt.figure(figsize=(6, 6))
        ax = plt.subplot(111, polar=True)
        plt.xticks(angles[:-1], categories, color='grey', size=8)
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=df.loc[i, "Type"])
        ax.fill(angles, values, alpha=0.1)
        plt.title(f'Radar Chart - {df.loc[i, "Type"]}', size=10, y=1.1)
        plt.tight_layout()
        plt.show()

def rank_types(df, metrics):
    ranking = {}
    for metric in metrics:
        best_type = df.loc[df[metric].idxmin(), "Type"]
        ranking[metric] = best_type
    ranking_df = pd.DataFrame(list(ranking.items()), columns=["Metric", "Best Type"])
    print("=== Best Type per Metric ===")
    print(ranking_df)

def plot_tradeoff(df, x_metric, y_metric):
    x_metric = x_metric.strip()
    y_metric = y_metric.strip()
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x=x_metric, y=y_metric, hue="Type", s=100)
    plt.title(f'Tradeoff: {x_metric} vs. {y_metric}')
    plt.tight_layout()
    plt.show()

# Load and analyze
base_folder = "/Users/carllavo/Desktop/MEX/mexscal/src/results"  # Update if needed
df_raw = merge_csvs_per_type(base_folder)
df = preprocess(df_raw)

# Select key metrics for analysis
key_metrics = [
    "Total Cost of Ownership", "Annual Kilometers Driven"
]
key_metrics = [m for m in key_metrics if m in df.columns]

# Run analyses
compare_key_metrics(df, key_metrics)
radar_chart(df, key_metrics)
rank_types(df, key_metrics)
plot_tradeoff(df, "Total Cost of Ownership", "Annual Kilometers Driven")
