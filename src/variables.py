import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

class VariableManager:
    FILE_PATH = "variables.json"
    
    def __init__(self):
        self.variables = {
            "cost_driver_hourly": {"value": 339.9, "name": "Driver Hourly Cost", "unit": "Kr/h"},
            "lifespan": {"value": 6, "name": "Lifespan", "unit": "years"},
            "interest_rate": {"value": 0.06, "name": "Interest Rate", "unit": "%"},
            "bc": {"value": 500, "name": "Battery capacity / fuel capacity", "unit": "kWh / litres"},
            "ccph_fast": {"value": 4.0, "name": "Public fast charger cost", "unit": "Kr/kWh"},
            "r": {"value": 465, "name": "Range of the vehicle per full charge", "unit": "km"},
            "truck_cost": {"value": 1400000.0, "name": "Truck cost", "unit": "Kr"},
            "battery_cost_per_kWh": {"value": 2500.0, "name": "Battery cost per kWh", "unit": "Kr/kWh"},
            "mcpkm": {"value": 0.98, "name": "Maintenance cost per km", "unit": "Kr/km"},
            "tire_factor": {"value": 0.0, "name": "Increased tire wear for BET", "unit": "%"},
            "subsidy": {"value": 0.25, "name": "Subsidy", "unit": "%"},
            "chinco": {"value": 100000, "name": "Charger installation cost", "unit": "Kr"},
            "chutra": {"value": 0.4, "name": "Charger utilization rate", "unit": "%"},
            "eprice": {"value": 0.92, "name": "Electricity price", "unit": "Kr/kWh"},
            "yu": {"value": 250, "name": "Active days in a year", "unit": ""},
            "bcls": {"value": 5000, "name": "Battery Cycle Lifespan", "unit": "Cycles"},
            "bcd": {"value": 0.8, "name": "Battery Cycle Discharge", "unit": "%"},
            "type": {"value": 4, "name": "Type of usage", "unit": "1/2/3/4"},
            "dmile": {"value": 6.25e-8, "name": "Depreciation Mileage", "unit": ""},
            "dannum": {"value": 0.2, "name": "Depreciation Year", "unit": ""},
            "y3tax": {"value": 2161, "name": "Yearly Road Tax 3 or less Axles", "unit": "Kr"},
            "y4tax": {"value": 3609, "name": "Yearly Road Tax 4 or more Axles", "unit": "Kr"},
            "axles": {"value": 3, "name": "Number of Axles", "unit": ""},

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

def open_variable_editor_in_main_window(root, var_manager):
    for widget in root.winfo_children():
        widget.destroy()

    entries = {}
    row = 0
    col = 0
    max_columns = 3
    field_width = 15

    for var_name, info in var_manager.variables.items():
        # Add skip for type variable
        if var_name == "type":
            continue

        frame = tk.Frame(root)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")

        label_var = tk.StringVar()
        # If unit is % use a .2% format, else use integer format, or if it's a float use .3f format
        if info['unit'] == "%":
            label_var.set(f"{info['name']}: {info['value']:.2%} {info['unit']}")
        elif isinstance(info['value'], int):
            label_var.set(f"{info['name']}: {info['value']} {info['unit']}")
        else:
            label_var.set(f"{info['name']}: {info['value']:.3f} {info['unit']}")
        label = tk.Label(frame, textvariable=label_var, anchor="w", width=field_width*2)
        label.grid(row=0, column=0, columnspan=3, sticky="w")

        entry = tk.Entry(frame, width=field_width)
        entry.grid(row=1, column=0, columnspan=3, padx=5, sticky="ew")
        # Display the percentage, float or int value in the entry field
        if info['unit'] == "%":
            entry.insert(0, f"{info['value'] * 100:.2f}")
        elif isinstance(info['value'], int):
            entry.insert(0, str(info['value']))
        else:
            entry.insert(0, f"{info['value']:.3f}")

        button_frame = tk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky="ew")

        button_update = tk.Button(button_frame, text="Update", width=8,
                                  command=lambda v=var_name, e=entry, lv=label_var: handle_update(v, e, lv, var_manager))
        button_update.pack(side='left', expand=True, padx=2)

        entries[var_name] = (entry, label_var)

        col += 1
        if col >= max_columns:
            col = 0
            row += 1

    # Separate UI for 'type'
    type_info = var_manager.variables["type"]
    type_frame = tk.Frame(root)
    type_frame.grid(row=row + 1, column=0, columnspan=max_columns, padx=10, pady=10, sticky="w")

    type_label_var = tk.StringVar()
    type_label_var.set(f"{type_info['name']}: {type_info['value']} {type_info['unit']}")
    type_label = tk.Label(type_frame, textvariable=type_label_var, anchor="w", width=field_width*2)
    type_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

    selected_type = tk.StringVar()
    selected_type.set(str(type_info['value']))
    type_dropdown = tk.OptionMenu(type_frame, selected_type, "1", "2", "3", "4", "5", "6", "7", "8")
    type_dropdown.config(width=field_width - 3)
    type_dropdown.grid(row=1, column=0, padx=5, pady=2, sticky="w")

    def update_type():
        if var_manager.update_variable("type", selected_type.get()):
            type_label_var.set(f"{type_info['name']}: {var_manager.variables['type']['value']} {type_info['unit']}")
            messagebox.showinfo("Success", "Type updated successfully!")
        else:
            messagebox.showerror("Error", "Invalid type selected.")

    type_update_btn = tk.Button(type_frame, text="Update", width=8, command=update_type)
    type_update_btn.grid(row=1, column=1, padx=5, sticky="w")


def handle_update(var_name, entry_field, label_var, var_manager):
    raw_value = entry_field.get()
    try:
        value = float(raw_value)
        if var_manager.variables[var_name]['unit'] == "%":
            value /= 100  # Convert to decimal form
        if var_manager.update_variable(var_name, value):
            label_var.set(f"{var_manager.variables[var_name]['name']}: {var_manager.variables[var_name]['value']} {var_manager.variables[var_name]['unit']}")
            messagebox.showinfo("Success", f"{var_manager.variables[var_name]['name']} updated successfully!")
        else:
            messagebox.showerror("Error", "Please enter a valid number.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
