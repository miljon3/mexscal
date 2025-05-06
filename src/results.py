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
    stats = read_csv_show_stats("src/results/Type4")

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
    print(all_data.head())  # Display the first few rows of the concatenated DataFrame

    # Display some key statistics
    stats = all_data.describe()
    print(stats)

    return stats
    