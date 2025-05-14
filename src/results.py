import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
import tkinter as tk
from tkinter import ttk


def merge_csvs_per_type(base_folder):
    merged_data = []
    for subdir in os.listdir(base_folder):
        subdir_path = os.path.join(base_folder, subdir)
        if os.path.isdir(subdir_path) and subdir.startswith("Type"):
            dfs = []
            for file in os.listdir(subdir_path):
                if file.endswith(".csv"):
                    df = pd.read_csv(os.path.join(subdir_path, file))
                    df = df.set_index("Category").T
                    df.columns = df.columns.str.strip()
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


def rank_types(df, metrics):
    ranking = {}
    for metric in metrics:
        best_type = df.loc[df[metric].idxmin(), "Type"]
        ranking[metric] = best_type
    ranking_df = pd.DataFrame(list(ranking.items()), columns=["Metric", "Best Type"])
    print("=== Best Type per Metric ===")
    print(ranking_df)
    return ranking_df


def plot_tradeoff(df, x_metric, y_metric):
    x_metric = x_metric.strip()
    y_metric = y_metric.strip()
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x=x_metric, y=y_metric, hue="Type", s=100)
    plt.title(f'Tradeoff: {x_metric} vs. {y_metric}')
    plt.tight_layout()
    plt.show()


def open_stats_page(root, var_manager):
    """
    Open the statistics page in the main window.
    :param root: The main window
    :param var_manager: VariableManager instance
    """

    # Load and analyze
    base_folder = "/Users/carllavo/Desktop/MEX/mexscal/src/results"
    df_raw = merge_csvs_per_type(base_folder)
    df = preprocess(df_raw)

    # Show the tradeoff plot
    plot_tradeoff(df, "Lifespan", "TCO per km")

def plot_tradeoff(df, x_metric, y_metric):
    x_metric = x_metric.strip()
    y_metric = y_metric.strip()

    # Define color by drivetrain
    color_mapping = {
        "Type1": "green", "Type2": "green", "Type3": "green", "Type4": "green",
        "Type5": "grey",  "Type6": "grey",  "Type7": "grey",  "Type8": "grey"
    }

    # Define class labels
    type_to_class = {
        "Type1": "Class1", "Type5": "Class1",
        "Type2": "Class2", "Type6": "Class2",
        "Type3": "Class3", "Type7": "Class3",
        "Type4": "Class4", "Type8": "Class4",
    }

    df["Class"] = df["Type"].map(type_to_class)

    plt.figure(figsize=(10, 7))
    sns.set(style="whitegrid")

    # Scatter plot
    ax = sns.scatterplot(
        data=df,
        x=x_metric,
        y=y_metric,
        hue="Type",
        palette=color_mapping,
        s=120,
        edgecolor="black",
        linewidth=0.5,
        legend=False
    )

    # Find cluster centers and add labels
    centers = df.groupby("Class")[[x_metric, y_metric]].mean().reset_index()

    for _, row in centers.iterrows():
        plt.text(
            row[x_metric] + 1,
            row[y_metric] + 1,
            row["Class"],
            fontsize=11,
            weight="bold",
            ha="center",
            va="bottom",
            color="black",
        )

    plt.title(f"Tradeoff: {x_metric} vs. {y_metric}", fontsize=16, weight='bold', pad=15)
    plt.xlabel(x_metric, fontsize=14)
    plt.ylabel(y_metric, fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

