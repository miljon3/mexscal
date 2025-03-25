import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

class VariableManager:
    FILE_PATH = "variables.json"
    
    def __init__(self):
        self.variables = {
            "cost_tires": {"value": 6300, "name": "Tire Cost", "unit": "Kr"},
            "cost_depot_electricity": {"value": 1.81, "name": "Depot Electricity Cost", "unit": "Kr/kWh"},
            "cost_public_electricity": {"value": 6.00, "name": "Public Electricity Cost", "unit": "Kr/kWh"},
            "cost_driver_hourly": {"value": 339.9, "name": "Driver Hourly Cost", "unit": "Kr/h"},
            "lifespan": {"value": 6, "name": "Lifespan", "unit": "years"},
            "interest_rate": {"value": 0.06, "name": "Interest Rate", "unit": "%"},
            "remaining_value": {"value": 0.3, "name": "Remaining Value", "unit": "%"},
            "yearly_depreciation": {"value": 0.3, "name": "Yearly Depreciation", "unit": "%"},
            "distance_deprecation": {"value": 0.0, "name": "Distance related depreciation", "unit": "%/km"},
            "pfcr": {"value": 0.6, "name": "Fraction of energy charged at public fast chargers", "unit": "%"},
            "dcr": {"value": 0.4, "name": "Fraction of energy charged at depot chargers", "unit": "%"},
            "bc": {"value": 500, "name": "Battery capacity", "unit": "kWh"},
            "ccph_fast": {"value": 0.5, "name": "Charging infrastructure cost per kWh for public fast chargers", "unit": "Kr/kWh"},
            "ccph_slow": {"value": 0.2, "name": "Charging infrastructure cost per kWh for depot chargers", "unit": "Kr/kWh"},
            "r": {"value": 300, "name": "Range of the vehicle per full charge", "unit": "km"},
            "akm": {"value": 50000, "name": "Annual kilometers driven over", "unit": "km"}
        }
        self.load_variables()
    
    def load_variables(self):
        if os.path.exists(self.FILE_PATH):
            df = pd.read_json(self.FILE_PATH, typ='series')
            for key, val in df.items():
                if key in self.variables and isinstance(val, dict):
                    self.variables[key]["value"] = val.get("value", self.variables[key]["value"])
    
    def save_variables(self):
        df = pd.Series(self.variables)
        df.to_json(self.FILE_PATH, indent=4)
    
    def update_variable(self, var_name, new_value):
        try:
            self.variables[var_name]["value"] = round(float(new_value), 3)
            self.save_variables()
            return True
        except ValueError:
            return False
    
    def adjust_variable(self, var_name, adjustment):
        self.variables[var_name]["value"] = round(self.variables[var_name]["value"] * adjustment, 3)
        self.save_variables()
        return self.variables[var_name]["value"]

def open_variable_editor_in_main_window(root, var_manager):
    for widget in root.winfo_children():
        widget.destroy()

    entries = {}
    row = 0
    col = 0
    max_columns = 3

    field_width = 15

    for var_name, info in var_manager.variables.items():
        frame = tk.Frame(root)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")

        label_var = tk.StringVar()
        label_var.set(f"{info['name']}: {info['value']} {info['unit']}")
        label = tk.Label(frame, textvariable=label_var, anchor="w", width=field_width*2)  # Fixed width
        label.grid(row=0, column=0, columnspan=3, sticky="w")

        entry = tk.Entry(frame, width=field_width)
        entry.grid(row=1, column=0, columnspan=3, padx=5, sticky="ew")
        entry.insert(0, str(info['value']))

        button_frame = tk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky="ew")

        button_minus_25 = tk.Button(button_frame, text="-25%", width=5, command=lambda v=var_name, e=entry, lv=label_var: handle_adjust(v, e, lv, var_manager, 0.75))
        button_minus_25.pack(side='left', expand=True, padx=2)

        button_update = tk.Button(button_frame, text="Update", width=8, command=lambda v=var_name, e=entry, lv=label_var: handle_update(v, e, lv, var_manager))
        button_update.pack(side='left', expand=True, padx=2)

        button_plus_25 = tk.Button(button_frame, text="+25%", width=5, command=lambda v=var_name, e=entry, lv=label_var: handle_adjust(v, e, lv, var_manager, 1.25))
        button_plus_25.pack(side='left', expand=True, padx=2)

        entries[var_name] = (entry, label_var)

        col += 1
        if col >= max_columns:
            col = 0
            row += 1


def handle_update(var_name, entry_field, label_var, var_manager):
    if var_manager.update_variable(var_name, entry_field.get()):
        label_var.set(f"{var_manager.variables[var_name]['name']}: {var_manager.variables[var_name]['value']} {var_manager.variables[var_name]['unit']}")
        messagebox.showinfo("Success", f"{var_manager.variables[var_name]['name']} updated successfully!")
    else:
        messagebox.showerror("Error", "Please enter a valid number.")

def handle_adjust(var_name, entry_field, label_var, var_manager, adjustment):
    new_value = var_manager.adjust_variable(var_name, adjustment)
    label_var.set(f"{var_manager.variables[var_name]['name']}: {new_value} {var_manager.variables[var_name]['unit']}")
    entry_field.delete(0, tk.END)
    entry_field.insert(0, str(new_value))
