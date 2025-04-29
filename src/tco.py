import tkinter as tk
from charging import calculate_cic, calculate_cic_km, calculate_charger_costs, calculate_ccph_depot, calculate_cycles
from maintenance import calculate_maintenance_cost
from financial import calculate_financing_cost

def open_tco_page(parent_frame, var_manager):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(parent_frame, text="Total Cost of Ownership (TCO) Analysis")
    title_label.pack(pady=10)

    grid_frame = tk.Frame(parent_frame)
    grid_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Headers
    tk.Label(grid_frame, text="Category").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="Per km").grid(row=0, column=1, padx=10, pady=5)
    tk.Label(grid_frame, text="Monthly").grid(row=0, column=2, padx=10, pady=5)
    tk.Label(grid_frame, text="Yearly").grid(row=0, column=3, padx=10, pady=5)

    # Main categories & subcategories
    tk.Label(grid_frame, text="Charging Infrastructure Cost").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="   - Charger Cost").grid(row=2, column=0, padx=10, pady=2, sticky="w")
    tk.Label(grid_frame, text="   - Energy Price").grid(row=3, column=0, padx=10, pady=2, sticky="w")

    tk.Label(grid_frame, text="Maintenance").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="   - Maintenance per km").grid(row=5, column=0, padx=10, pady=2, sticky="w")

    tk.Label(grid_frame, text="Financing").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="   - Truck").grid(row=7, column=0, padx=10, pady=2, sticky="w")
    tk.Label(grid_frame, text="   - Battery").grid(row=8, column=0, padx=10, pady=2, sticky="w")

    tk.Label(grid_frame, text="Total").grid(row=9, column=0, padx=10, pady=5, sticky="w")

    # Subcategory labels
    label_charger_cost_km = tk.Label(grid_frame, text="N/A")
    label_charger_cost_km.grid(row=2, column=1, padx=10, pady=2)

    label_energy_price_km = tk.Label(grid_frame, text="N/A")
    label_energy_price_km.grid(row=3, column=1, padx=10, pady=2)

    label_maintenance_km = tk.Label(grid_frame, text="N/A")
    label_maintenance_km.grid(row=5, column=1, padx=10, pady=2)

    label_maintenance_monthly = tk.Label(grid_frame, text="N/A")
    label_maintenance_monthly.grid(row=5, column=2, padx=10, pady=2)

    label_maintenance_yearly = tk.Label(grid_frame, text="N/A")
    label_maintenance_yearly.grid(row=5, column=3, padx=10, pady=2)

    label_financial_truck_km = tk.Label(grid_frame, text="N/A")
    label_financial_truck_km.grid(row=7, column=1, padx=10, pady=2)

    label_financial_battery_km = tk.Label(grid_frame, text="N/A")
    label_financial_battery_km.grid(row=8, column=1, padx=10, pady=2)

    label_total_per_km = tk.Label(grid_frame, text="N/A")
    label_total_per_km.grid(row=9, column=1, padx=10, pady=5)

    label_total_monthly = tk.Label(grid_frame, text="N/A")
    label_total_monthly.grid(row=9, column=2, padx=10, pady=5)

    label_total_yearly = tk.Label(grid_frame, text="N/A")
    label_total_yearly.grid(row=9, column=3, padx=10, pady=5)

    def calculate_and_display_cic():
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
        yu = var_manager.variables["yu"]["value"]
        battery_cost = bc * battery_cost_per_kWh
        subsidy = var_manager.variables["subsidy"]["value"]
        remaining_value = var_manager.variables["remaining_value"]["value"]
        bcls = var_manager.variables["bcls"]["value"]
        bcd = var_manager.variables["bcd"]["value"]

        # Charging
        cic_two = calculate_charger_costs(chinco, chutra, lifespan, bc, yu)
        ccph_depot = calculate_ccph_depot(cic_two, eprice)
        cic_km = calculate_cic_km(pfcr, dcr, bc, ccph_fast, ccph_depot, eprice, r)
        cic = calculate_cic(cic_km, akm)

        # Maintenance
        maintenance_cost = calculate_maintenance_cost(mckpm, akm)

        # Financing
        battery_cost = bc * battery_cost_per_kWh
        tcls = calculate_cycles(bc, r, akm, bcd)
        financing_cost = calculate_financing_cost(truck_cost, battery_cost, interest_rate, lifespan, subsidy, remaining_value, bcls, tcls)

        # Share of total cost from battery
        bshare = battery_cost / (battery_cost + truck_cost)
        print(f"Battery Share: {bshare}")
        tshare = truck_cost / (battery_cost + truck_cost)
        print(f"Truck Share: {tshare}")
        battery_financing = financing_cost * bshare
        truck_financing = financing_cost * tshare
        print(f"Battery Financing: {battery_financing}")
        print(f"Truck Financing: {truck_financing}")

        # Totals
        total_cost_yearly = cic + maintenance_cost + financing_cost
        total_cost_monthly = total_cost_yearly / 12
        total_cost_per_km = total_cost_yearly / akm

        # Update labels
        charger_cost_per_km = ((bc * ccph_fast) + (bc * ccph_depot)) / (2 * r)
        label_charger_cost_km.config(text=f"{charger_cost_per_km:.2f} SEK/km")
        label_energy_price_km.config(text=f"{(bc * eprice) / r:.2f} SEK/km")

        label_maintenance_km.config(text=f"{maintenance_cost / akm:.2f} SEK/km")
        label_maintenance_monthly.config(text=f"{maintenance_cost / 12:.2f} SEK")
        label_maintenance_yearly.config(text=f"{maintenance_cost:.2f} SEK")

        label_financial_truck_km.config(text=f"{truck_financing / akm:.2f} SEK/km")
        label_financial_battery_km.config(text=f"{battery_financing / akm:.2f} SEK/km")

        label_total_per_km.config(text=f"{total_cost_per_km:.2f} SEK/km")
        label_total_monthly.config(text=f"{total_cost_monthly:.2f} SEK")
        label_total_yearly.config(text=f"{total_cost_yearly:.2f} SEK")

    calculate_button = tk.Button(parent_frame, text="Calculate Costs", command=calculate_and_display_cic)
    calculate_button.pack(pady=10)
