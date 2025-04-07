import tkinter as tk
from tkinter import font
from charging import calculate_cic, calculate_cic_km
from maintenance import calculate_maintenance_cost
from financial import calculate_financing_cost

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
        mckpm = var_manager.variables["mcpkm"]["value"]
        truck_cost = var_manager.variables["truck_cost"]["value"]
        battery_cost_per_kWh = var_manager.variables["battery_cost_per_kWh"]["value"]
        lifespan = var_manager.variables["lifespan"]["value"]
        interes_rate = var_manager.variables["interest_rate"]["value"]
        battery_cost = bc * battery_cost_per_kWh
        subsidy = var_manager.variables["subsidy"]["value"]
        remaining_value = var_manager.variables["remaining_value"]["value"]

        cic_km = calculate_cic_km(pfcr, dcr, bc, ccph_fast, ccph_slow, r)
        cic = calculate_cic(cic_km, akm)

        label_cic_km.config(text=f"CIC_KM: {cic_km:.2f} SEK/km")
        label_cic.config(text=f"CIC: {cic:.2f} SEK")

        maintenance_cost = calculate_maintenance_cost(mckpm, akm)
        label_maintenance.config(text=f"Maintenance Cost: {maintenance_cost:.2f} SEK")

        financing_cost = calculate_financing_cost(truck_cost, battery_cost, interes_rate, lifespan, subsidy, remaining_value)
        label_financing.config(text=f"Financing Cost: {financing_cost:.2f} SEK")

        # Load the interest rate and lifespan from the variable manager
        interest_rate = var_manager.variables["interest_rate"]["value"]
        lifespan = var_manager.variables["lifespan"]["value"]

        # Add the lifespan and interest rate to their labels
        label_lifespan.config(text=f"Lifespan (years): {lifespan}")
        label_interest_rate.config(text=f"Interest Rate (%): {interest_rate * 100:.2f}")
        label_remaining_value.config(text=f"Remaining Value (%): {remaining_value * 100:.2f}")
        label_subsidy.config(text=f"Subsidy (%): {subsidy * 100:.2f}")


        # Add everything up to get the total cost of ownership (TCO)
        total_cost = cic*lifespan + maintenance_cost*lifespan + financing_cost
        label_tco.config(text=f"Total Cost of Ownership (TCO): {total_cost:.2f} SEK")



    calculate_button = tk.Button(parent_frame, text="Calculate CIC", command=calculate_and_display_cic)
    calculate_button.pack(pady=20)

    label_cic_km = tk.Label(parent_frame, text="CIC_KM: N/A")
    label_cic_km.pack(pady=10)

    label_cic = tk.Label(parent_frame, text="CIC: N/A")
    label_cic.pack(pady=10)

    label_maintenance = tk.Label(parent_frame, text="Maintenance Cost: N/A")
    label_maintenance.pack(pady=10)

    label_financing = tk.Label(parent_frame, text="Financing Cost: N/A")
    label_financing.pack(pady=10)

    # Label the lifespan and interest rate for clarity
    label_lifespan = tk.Label(parent_frame, text="Lifespan (years):")
    label_lifespan.pack(pady=5)

    label_interest_rate = tk.Label(parent_frame, text="Interest Rate (%):")
    label_interest_rate.pack(pady=5)

    label_remaining_value = tk.Label(parent_frame, text="Remaining Value (%):")
    label_remaining_value.pack(pady=5)

    label_subsidy = tk.Label(parent_frame, text="Subsidy (%):")
    label_subsidy.pack(pady=5)


    # Create a label for the total cost of ownership (TCO)
    label_tco = tk.Label(parent_frame, text="Total Cost of Ownership (TCO): N/A")
    label_tco.pack(pady=10)