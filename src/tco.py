import tkinter as tk
from tkinter import font
from charging import calculate_cic, calculate_cic_km

def open_tco_page(parent_frame, var_manager):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    label = tk.Label(parent_frame, text="Total Cost of Ownership (TCO) Analysis")
    label.pack(pady=20)

    def calculate_and_display_cic():
        pfcr = var_manager.variables["pfcr"]["value"]
        dcr = var_manager.variables["dcr"]["value"]
        bc = var_manager.variables["bc"]["value"]
        ccph_fast = var_manager.variables["ccph_fast"]["value"]
        ccph_slow = var_manager.variables["ccph_slow"]["value"]
        r = var_manager.variables["r"]["value"]
        akm = var_manager.variables["akm"]["value"]

        cic_km = calculate_cic_km(pfcr, dcr, bc, ccph_fast, ccph_slow, r)
        cic = calculate_cic(cic_km, akm)

        label_cic_km.config(text=f"CIC_KM: {cic_km:.2f} SEK/km")
        label_cic.config(text=f"CIC: {cic:.2f} SEK")

    calculate_button = tk.Button(parent_frame, text="Calculate CIC", command=calculate_and_display_cic)
    calculate_button.pack(pady=20)

    label_cic_km = tk.Label(parent_frame, text="CIC_KM: N/A")
    label_cic_km.pack(pady=10)

    label_cic = tk.Label(parent_frame, text="CIC: N/A")
    label_cic.pack(pady=10)