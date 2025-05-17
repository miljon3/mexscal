import os
import threading
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
import tkinter as tk
from tkinter import ttk
from matplotlib.ticker import PercentFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog



def merge_csvs_per_type(base_folder, progress_callback=None):
    merged_data = []
    subdirs = [d for d in os.listdir(base_folder) if d.startswith("Type")]
    total_subdirs = len(subdirs)

    for i, subdir in enumerate(subdirs):
        subdir_path = os.path.join(base_folder, subdir)
        if os.path.isdir(subdir_path):
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

        if progress_callback:
            progress_callback(int((i + 1) / total_subdirs * 40))  # Progress 0–40%

    return pd.concat(merged_data, ignore_index=True)


def preprocess(df, progress_callback=None, base_progress=40):
    total_cols = len(df.columns) - 1  # excluding 'Type'

    for i, col in enumerate(df.columns):
        if col != "Type":
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if progress_callback:
                progress_callback(base_progress + int((i + 1) / total_cols * 30))  # Progress 40–70%

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


def open_stats_page(root, var_manager, x_metric, progress_callback=None):
    base_folder = "src/results"

    df_raw = merge_csvs_per_type(base_folder, progress_callback=progress_callback)
    df = preprocess(df_raw, progress_callback=progress_callback)

    if progress_callback:
        progress_callback(90)

    return df


def run_analysis(content_frame, var_manager, x_metric):
    for widget in content_frame.winfo_children():
        widget.destroy()

    label = tk.Label(content_frame, text=f"Running {x_metric.capitalize()} Analysis...")
    label.pack(pady=10)

    progress = ttk.Progressbar(content_frame, mode='determinate', maximum=100)
    progress.pack(pady=10, fill='x', padx=20)

    def update_progress(value):
        progress['value'] = value
        content_frame.update_idletasks()

    def analysis_task():
        df = open_stats_page(content_frame, var_manager, x_metric, progress_callback=update_progress)
        
        # Schedule plotting and progress update in the main thread
        def finish_plotting():
            plot_tradeoff(content_frame, df, x_metric, "TCO per km")
            update_progress(100)  # Ensure progress is set to 100%
        
        content_frame.after(0, finish_plotting)

    threading.Thread(target=analysis_task, daemon=True).start()


def plot_tradeoff(parent_frame, df, x_metric, y_metric):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import tkinter as tk
    

    x_metric = x_metric.strip()
    y_metric = y_metric.strip()

    # Custom labels for legend
    type_labels = {
        "Type1": "(1) Electric 18t 180kwh",
        "Type2": "(2) Electric 18t 250kwh",
        "Type3": "(3) Electric 42t 550kwh",
        "Type4": "(4) Electric 72t 550kwh",
        "Type5": "(1) Diesel 18t",
        "Type6": "(2) Diesel 18t",
        "Type7": "(3) Diesel 42t",
        "Type8": "(4) Diesel 72t"
    }

    # Type to class mapping
    type_to_class = {
        "Type1": "Class1", "Type5": "Class1",
        "Type2": "Class2", "Type6": "Class2",
        "Type3": "Class3", "Type7": "Class3",
        "Type4": "Class4", "Type8": "Class4",
    }

    # Map labels and class
    df["Class"] = df["Type"].map(type_to_class)
    df["Label"] = df["Type"].map(type_labels)

    LFC = int(df["LFC"].values[0])
    # Define consistent palette for all subplots
    label_palette = {
        "(1) Electric 18t 180kwh": "#1f77b4",
        "(2) Electric 18t 250kwh": "#1f77b4",
        "(3) Electric 42t 550kwh": "#1f77b4",
        "(4) Electric 72t 550kwh": "#1f77b4",
        "(1) Diesel 18t": "#ff7f0e",
        "(2) Diesel 18t": "#ff7f0e",
        "(3) Diesel 42t": "#ff7f0e",
        "(4) Diesel 72t": "#ff7f0e"
    }

    classes = sorted(df["Class"].unique())
    n_classes = len(classes)


    
    # Grid setup
    n_rows = 2
    n_cols = 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 5 * n_rows), sharey=False)
    axes = axes.flatten()  # flatten to 1D for easy indexing

    sns.set(style="whitegrid")

    for i, cls in enumerate(classes):
        class_df = df[df["Class"] == cls].sort_values(by=x_metric)

        ax = axes[i]
        sns.lineplot(
            data=class_df,
            x=x_metric,
            y=y_metric,
            hue="Label",
            marker="o",
            linewidth=2,
            ax=ax,
            palette=label_palette  # consistent color mapping
        )

        ax.legend(title=None) 

        if (x_metric == "Lifespan"):
            ax.set_title(f"{LFC} LFC: Analysis Period vs. {y_metric}", fontsize=14, weight='bold')
            ax.set_xlabel("Analysis Period" + "[years]")
        else:
            ax.set_title(f"Subsidy vs. {y_metric}", fontsize=14, weight='bold')
            ax.set_xlabel("Subsidy" + "[%]")
            ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.set_ylabel(y_metric + " [SEK]")
        ax.tick_params(labelsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)

        # Optional: remove individual legends
        # ax.legend_.remove()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    if file_path:
        fig.savefig(file_path, dpi=300)
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
