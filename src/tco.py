import tkinter as tk
from charging import calculate_cic, calculate_cic_km, calculate_charger_costs, calculate_ccph_depot
from maintenance import calculate_maintenance_cost
from financial import calculate_financing_cost

def open_tco_page(parent_frame, var_manager):
    # Clear existing widgets in the parent frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Add TCO page title
    title_label = tk.Label(parent_frame, text="Total Cost of Ownership (TCO) Analysis")
    title_label.pack(pady=10)

    # Create a frame for the grid layout
    grid_frame = tk.Frame(parent_frame)
    grid_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Add headers for the columns
    tk.Label(grid_frame, text="Category").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="Per km").grid(row=0, column=1, padx=10, pady=5)
    tk.Label(grid_frame, text="Monthly").grid(row=0, column=2, padx=10, pady=5)
    tk.Label(grid_frame, text="Yearly").grid(row=0, column=3, padx=10, pady=5)

    # Add category labels
    tk.Label(grid_frame, text="Charging Infrastructure Cost").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="Maintenance").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="Financing").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="Total").grid(row=4, column=0, padx=10, pady=5, sticky="w")

    # Add data labels for costs
    label_cic_km = tk.Label(grid_frame, text="N/A")
    label_cic_km.grid(row=1, column=1, padx=10, pady=5)

    label_cic_monthly = tk.Label(grid_frame, text="N/A")
    label_cic_monthly.grid(row=1, column=2, padx=10, pady=5)

    label_cic_yearly = tk.Label(grid_frame, text="N/A")
    label_cic_yearly.grid(row=1, column=3, padx=10, pady=5)

    label_maintenance_km = tk.Label(grid_frame, text="N/A")
    label_maintenance_km.grid(row=2, column=1, padx=10, pady=5)

    label_maintenance_monthly = tk.Label(grid_frame, text="N/A")
    label_maintenance_monthly.grid(row=2, column=2, padx=10, pady=5)

    label_maintenance_yearly = tk.Label(grid_frame, text="N/A")
    label_maintenance_yearly.grid(row=2, column=3, padx=10, pady=5)

    label_financial_km = tk.Label(grid_frame, text="N/A")
    label_financial_km.grid(row=4, column=1, padx=10, pady=5)

    label_financial_monthly = tk.Label(grid_frame, text="N/A")
    label_financial_monthly.grid(row=4, column=2, padx=10, pady=5)

    label_financial_yearly = tk.Label(grid_frame, text="N/A")
    label_financial_yearly.grid(row=4, column=3, padx=10, pady=5)

    label_total_per_km = tk.Label(grid_frame, text="N/A")
    label_total_per_km.grid(row=3, column=1, padx=10, pady=5)

    label_total_monthly = tk.Label(grid_frame, text="N/A")
    label_total_monthly.grid(row=3, column=2, padx=10, pady=5)

    label_total_yearly = tk.Label(grid_frame, text="N/A")
    label_total_yearly.grid(row=3, column=3, padx=10, pady=5)

    # Function to calculate and display costs
    def calculate_and_display_cic():
        # Retrieve variables from var_manager
        pfcr = var_manager.variables["pfcr"]["value"]
        dcr = var_manager.variables["dcr"]["value"]
        bc = var_manager.variables["bc"]["value"]
        ccph_fast = var_manager.variables["ccph_fast"]["value"]
        ccph_slow = var_manager.variables["ccph_slow"]["value"]
        r = var_manager.variables["r"]["value"]
        akm = var_manager.variables["akm"]["value"]
        mckpm = var_manager.variables["mcpkm"]["value"]
        truck_cost = var_manager.variables["truck_cost"]["value"]
        battery_cost_per_kWh = var_manager.variables["battery_cost_per_kWh"]["value"]
        lifespan = var_manager.variables["lifespan"]["value"]
        interest_rate = var_manager.variables["interest_rate"]["value"]
        subsidy = var_manager.variables["subsidy"]["value"]
        remaining_value = var_manager.variables["remaining_value"]["value"]
        chinco = var_manager.variables["chinco"]["value"]
        chutra = var_manager.variables["chutra"]["value"]
        eprice = var_manager.variables["eprice"]["value"]

        # Perform calculations
        cic_two = calculate_charger_costs(chinco, chutra, lifespan, bc)
        print(f"Charger cost per kWh: {cic_two:.2f} SEK/kWh")
        ccph_depot = calculate_ccph_depot(cic_two, eprice)
        print(f"Depot charger cost per kWh: {ccph_depot:.2f} SEK/kWh")
        # Replaced ccph_slow with ccph_depot in the calculation
        cic_km = calculate_cic_km(pfcr, dcr, bc, ccph_fast, ccph_depot, eprice, r)
        cic = calculate_cic(cic_km, akm)
        maintenance_cost = calculate_maintenance_cost(mckpm, akm)
        battery_cost = bc * battery_cost_per_kWh
        financing_cost = calculate_financing_cost(truck_cost, battery_cost, interest_rate, lifespan, subsidy, remaining_value)

        # Calculate total costs
        total_cost_yearly = cic + maintenance_cost + financing_cost
        total_cost_monthly = total_cost_yearly / 12
        total_cost_per_km = total_cost_yearly / akm

        # Update CIC labels
        label_cic_km.config(text=f"{cic_km:.2f} SEK/km")
        label_cic_monthly.config(text=f"{cic / 12:.2f} SEK")
        label_cic_yearly.config(text=f"{cic:.2f} SEK")

        # Update maintenance labels
        label_maintenance_km.config(text=f"{maintenance_cost / akm:.2f} SEK/km")
        label_maintenance_monthly.config(text=f"{maintenance_cost / 12:.2f} SEK")
        label_maintenance_yearly.config(text=f"{maintenance_cost:.2f} SEK")

        # Update financing labels
        label_financial_km.config(text=f"{financing_cost / akm:.2f} SEK/km")
        label_financial_monthly.config(text=f"{financing_cost / 12:.2f} SEK")
        label_financial_yearly.config(text=f"{financing_cost:.2f} SEK")

        # Update total cost labels
        label_total_per_km.config(text=f"{total_cost_per_km:.2f} SEK/km")
        label_total_monthly.config(text=f"{total_cost_monthly:.2f} SEK")
        label_total_yearly.config(text=f"{total_cost_yearly:.2f} SEK")

    # Button to trigger the calculation
    calculate_button = tk.Button(parent_frame, text="Calculate Costs", command=calculate_and_display_cic)
    calculate_button.pack(pady=10)