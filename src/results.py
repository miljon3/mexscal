import tkinter as tk
import os
import pandas as pd

def open_stats_page(root, var_manager):
    for widget in root.winfo_children():
        widget.destroy()

    # Create a frame for the stats page
    stats_frame = tk.Frame(root)
    stats_frame.pack(pady=20)

    # Create a label for the stats page
    stats_label = tk.Label(stats_frame, text="Statistics Page", font=("Helvetica", 16))
    stats_label.pack(pady=10)

    # Create a label to display the statistics
    stats_text = tk.Text(stats_frame, width=80, height=20)
    stats_text.pack(pady=10)

    # Fetch and display statistics
    # TODO: Use read_csv_show_stats function to read the CSV files and display the statistics
    stats = read_csv_show_stats("src/results/Type1")
    """          Per km       Monthly        Yearly
        count  80.000000     80.000000  8.000000e+01
        mean    5.272748  26530.611497  3.183673e+05
        std     7.011889  35285.268632  4.234232e+05
        min     0.980000   4793.175194  5.751810e+04
        25%     1.243853   6379.886722  7.655864e+04
        50%     1.401982   6891.507995  8.269810e+04
        75%     5.350160  26826.655169  3.219199e+05
        max    17.469937  88852.906841  1.066235e+06
    """

    # Read the mean and std from the stats and display them in the text box
    stats_text.insert(tk.END, "Statistics:\n")
    stats_text.insert(tk.END, "Per km:\n")
    stats_text.insert(tk.END, f"Mean: {stats['Per km']['mean']:.2f}\n")
    stats_text.insert(tk.END, f"Std: {stats['Per km']['std']:.2f}\n")
    stats_text.insert(tk.END, "Monthly:\n")
    stats_text.insert(tk.END, f"Mean: {stats['Monthly']['mean']:.2f}\n")
    stats_text.insert(tk.END, f"Std: {stats['Monthly']['std']:.2f}\n")
    stats_text.insert(tk.END, "Yearly:\n")
    stats_text.insert(tk.END, f"Mean: {stats['Yearly']['mean']:.2f}\n")
    stats_text.insert(tk.END, f"Std: {stats['Yearly']['std']:.2f}\n")


    # Create a button to go back to the main menu
    back_button = tk.Button(stats_frame, text="Back to Main Menu", command=lambda: root.destroy())
    back_button.pack(pady=10)

def read_csv_show_stats(folder_path):
    """
    Read all the CSV files in the folder and display some key stats.
    :param folder_path: Path to the CSV files.
    """

    # List to hold DataFrames
    dataframes = []

    # Read all CSV files in the folder
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder_path, file))
            dataframes.append(df)

    # Concatenate all DataFrames into one
    all_data = pd.concat(dataframes, ignore_index=True)

    # Display some key statistics
    stats = all_data.describe()
    print(stats)

    return stats
    