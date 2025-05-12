import tkinter as tk
import pandas as pd
from exporter import save_results_to_csv
from charging import calculate_cic_km, calculate_charger_costs, calculate_ccph_depot, calculate_cycles
from maintenance import calculate_maintenance_cost
from financial import calculate_financing_cost
from montecarlo import monte_carlo_sampling, return_totals, animate
from purchase_price import calculate_purchase_price
from routes import calculate_driver_cost, calculate_driver_cost_km
from depreciation import residual_value
from range import calculate_daily_range
from discount import discount

typedict = {
            1: {
                "name": "Distribution",
                "weight": "18",
                "fuel": "Electric",
                "power": "200",
                "capacity": "180"
            },
            2: {
                "name": "Regional Distribution",
                "weight": "18",
                "fuel": "Electric",
                "power": "200",
                "capacity": "250",
            },
            3: {
                "name": "Long Range Traffic",
                "weight": "42",
                "fuel": "Electric",
                "power": "350",
                "capacity": "550",
            },
            4: {
                "name": "Nomadic",
                "weight": "72",
                "fuel": "Electric",
                "power": "550",
                "capacity": "550",
            },
            5: {
                "name": "Distribution (diesel)",
                "weight": "18",
                "fuel": "Diesel",
                "power": "200",
                "capacity": "180",
            },
            6: {
                "name": "Regional Distribution (diesel)",
                "weight": "18",
                "fuel": "Diesel",
                "power": "200",
                "capacity": "250",
            },
            7: {
                "name": "Long Range Traffic (diesel)",
                "weight": "42",
                "fuel": "Diesel",
                "power": "350",
                "capacity": "550",
            },
            8: {
                "name": "Nomadic (diesel)",
                "weight": "72",
                "fuel": "Diesel",
                "power": "550",
                "capacity": "550",
            }
        }

def open_tco_page(scrollable_frame, var_manager):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

     # Scrollable frame setup
    canvas = tk.Canvas(scrollable_frame)
    scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    def _on_mousewheel(event):
    # For MacOS, delta values are small so multiply by 1 (or higher if needed)
        canvas.yview_scroll(int(-1 * (event.delta*3)), "units")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)  

    title_label = tk.Label(scrollable_frame, text="Total Cost of Ownership (TCO) Analysis")
    title_label.pack(pady=10)

    grid_frame = tk.Frame(scrollable_frame)
    grid_frame.pack(pady=10, padx=10, fill="both", expand=True)

    stat_frame = tk.Frame(scrollable_frame)
    stat_frame.pack(pady=10, padx=10, fill="both", expand=True)

    """ Grid frame for displaying the results """

    # Headers
    tk.Label(grid_frame, text="Category").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="Per km").grid(row=0, column=1, padx=10, pady=5)
    tk.Label(grid_frame, text="Monthly").grid(row=0, column=2, padx=10, pady=5)
    tk.Label(grid_frame, text="Yearly").grid(row=0, column=3, padx=10, pady=5)

    # Main categories & subcategories
    tk.Label(grid_frame, text="Charging Costs").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="   - Charger Cost").grid(row=2, column=0, padx=10, pady=2, sticky="w")
    tk.Label(grid_frame, text="   - Energy Price").grid(row=3, column=0, padx=10, pady=2, sticky="w")

    tk.Label(grid_frame, text="Operational Costs").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="   - Maintenance").grid(row=5, column=0, padx=10, pady=2, sticky="w")
    tk.Label(grid_frame, text="   - Driver").grid(row=6, column=0, padx=10, pady=2, sticky="w")
    tk.Label(grid_frame, text="   - Road Tax").grid(row=7, column=0, padx=10, pady=2, sticky="w")

    tk.Label(grid_frame, text="Financing Costs").grid(row=8, column=0, padx=10, pady=5, sticky="w")
    tk.Label(grid_frame, text="   - Truck").grid(row=9, column=0, padx=10, pady=2, sticky="w")
    tk.Label(grid_frame, text="   - Battery").grid(row=10, column=0, padx=10, pady=2, sticky="w")

    tk.Label(grid_frame, text="Total").grid(row=11, column=0, padx=10, pady=5, sticky="w")

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

    label_driver_km = tk.Label(grid_frame, text="N/A")
    label_driver_km.grid(row=6, column=1, padx=10, pady=2)

    label_driver_monthly = tk.Label(grid_frame, text="N/A")
    label_driver_monthly.grid(row=6, column=2, padx=10, pady=2)

    label_driver_yearly = tk.Label(grid_frame, text="N/A")
    label_driver_yearly.grid(row=6, column=3, padx=10, pady=2)

    label_road_tax_km = tk.Label(grid_frame, text="N/A")
    label_road_tax_km.grid(row=7, column=1, padx=10, pady=2)

    label_road_tax_monthly = tk.Label(grid_frame, text="N/A")
    label_road_tax_monthly.grid(row=7, column=2, padx=10, pady=2)

    label_road_tax_yearly = tk.Label(grid_frame, text="N/A")
    label_road_tax_yearly.grid(row=7, column=3, padx=10, pady=2)

    label_financial_truck_km = tk.Label(grid_frame, text="N/A")
    label_financial_truck_km.grid(row=9, column=1, padx=10, pady=2)

    label_financial_battery_km = tk.Label(grid_frame, text="N/A")
    label_financial_battery_km.grid(row=10, column=1, padx=10, pady=2)

    label_total_per_km = tk.Label(grid_frame, text="N/A")
    label_total_per_km.grid(row=11, column=1, padx=10, pady=5)

    label_total_monthly = tk.Label(grid_frame, text="N/A")
    label_total_monthly.grid(row=11, column=2, padx=10, pady=5)

    label_total_yearly = tk.Label(grid_frame, text="N/A")
    label_total_yearly.grid(row=11, column=3, padx=10, pady=5)

    # DISPLAY TCO VALUES

    label_TCO_per_km_title = tk.Label(grid_frame, text="TCO per km:", font=('Arial', 15, 'bold'))
    label_TCO_per_km_title.grid(row=12, column=1, padx=10, pady=(10, 2))

    label_TCO_total_title = tk.Label(grid_frame, text="Total TCO:", font=('Arial', 15, 'bold'))
    label_TCO_total_title.grid(row=12, column=3, padx=10, pady=(10, 2))

    label_total_TCO_per_km = tk.Label(grid_frame, text="N/A")
    label_total_TCO_per_km.grid(row=13, column=1, padx=10, pady=5)

    label_total_TCO = tk.Label(grid_frame, text="N/A")
    label_total_TCO.grid(row=13, column=3, padx=10, pady=5)

    # Main categories & subcategories
    tk.Label(stat_frame, text="Truck").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(stat_frame, text="   - Truck Cost").grid(row=2, column=0, padx=10, pady=2, sticky="w")
    tk.Label(stat_frame, text="   - Battery Cost").grid(row=3, column=0, padx=10, pady=2, sticky="w")
    tk.Label(stat_frame, text="   - Battery Capacity").grid(row=4, column=0, padx=10, pady=2, sticky="w")
    tk.Label(stat_frame, text="   - Daily Range").grid(row=5, column=0, padx=10, pady=2, sticky="w")
    tk.Label(stat_frame, text="   - Daily Driving Distance").grid(row=6, column=0, padx=10, pady=2, sticky="w")
    tk.Label(stat_frame, text="   - Daily Driving Time").grid(row=7, column=0, padx=10, pady=2, sticky="w")
    tk.Label(stat_frame, text="   - Days driven per year").grid(row=8, column=0, padx=10, pady=2, sticky="w")
    tk.Label(stat_frame, text="   - Annual Kilometers Driven").grid(row=9, column=0, padx=10, pady=2, sticky="w")
    tk.Label(stat_frame, text="   - Number of battery replacements").grid(row=10, column=0, padx=10, pady=2, sticky="w")

    # For every Label in the grid, create a label to display the value

    label_truck_cost = tk.Label(stat_frame, text="N/A")
    label_truck_cost.grid(row=2, column=1, padx=10, pady=2)

    label_battery_cost = tk.Label(stat_frame, text="N/A")
    label_battery_cost.grid(row=3, column=1, padx=10, pady=2)

    label_battery_capacity = tk.Label(stat_frame, text="N/A")
    label_battery_capacity.grid(row=4, column=1, padx=10, pady=2)

    label_daily_range = tk.Label(stat_frame, text="N/A")
    label_daily_range.grid(row=5, column=1, padx=10, pady=2)

    label_daily_driving_distance = tk.Label(stat_frame, text="N/A")
    label_daily_driving_distance.grid(row=6, column=1, padx=10, pady=2)

    label_daily_driving_time = tk.Label(stat_frame, text="N/A")
    label_daily_driving_time.grid(row=7, column=1, padx=10, pady=2)

    label_days_driven_per_year = tk.Label(stat_frame, text="N/A")
    label_days_driven_per_year.grid(row=8, column=1, padx=10, pady=2)

    label_annual_kilometers_driven = tk.Label(stat_frame, text="N/A")
    label_annual_kilometers_driven.grid(row=9, column=1, padx=10, pady=2)

    label_battery_replacements = tk.Label(stat_frame, text="N/A")
    label_battery_replacements.grid(row=10, column=1, padx=10, pady=2)


    def calculate_and_display_cic():
        """ Variables """
        type = var_manager.variables["type"]["value"]
        type = int(type)
        #pfcr = var_manager.variables["pfcr"]["value"]
        #dcr = var_manager.variables["dcr"]["value"]
        cost_driver_hourly = var_manager.variables["cost_driver_hourly"]["value"]
        # bc = var_manager.variables["bc"]["value"]
        d = var_manager.variables["d"]["value"]
        ccph_fast = var_manager.variables["ccph_fast"]["value"]
        # r = var_manager.variables["r"]["value"]
        """ akm should be done by mc, uncomment otherwise"""
        #akm = var_manager.variables["akm"]["value"]
        mckpm = var_manager.variables["mcpkm"]["value"]
        tire_factor = var_manager.variables["tire_factor"]["value"]
        battery_cost_per_kWh = var_manager.variables["battery_cost_per_kWh"]["value"]
        lifespan = var_manager.variables["lifespan"]["value"]
        interest_rate = var_manager.variables["interest_rate"]["value"]
        subsidy = var_manager.variables["subsidy"]["value"]
        chinco = var_manager.variables["chinco"]["value"]
        chutra = var_manager.variables["chutra"]["value"]
        eprice = var_manager.variables["eprice"]["value"]
        yu = int(var_manager.variables["yu"]["value"])
        bc = int(typedict[type]["capacity"])
        battery_cost = bc * battery_cost_per_kWh
        bcls = var_manager.variables["bcls"]["value"]
        bcd = var_manager.variables["bcd"]["value"]
       
        # Dictionary containing variables for the different types
        
        y3tax = var_manager.variables["y3tax"]["value"]
        y4tax = var_manager.variables["y4tax"]["value"]
        dy3tax = var_manager.variables["dy3tax"]["value"]
        dy4tax = var_manager.variables["dy4tax"]["value"]
        axles = var_manager.variables["axles"]["value"]
        dieselprice = var_manager.variables["dieselprice"]["value"]
        dieseltank = var_manager.variables["dieseltank"]["value"]
        dieselrange = var_manager.variables["dieselrange"]["value"]
        # Run the Monte Carlo simulation
        # If type is 5,6,7,8 change r to dieselrange and set bcd to 0.95
        if type in [5, 6, 7, 8]:
            print("Disesel Detected")
            r = dieselrange
            bcd = 1
            bc = dieseltank
            battery_cost = 0
            battery_cost_per_kWh = 0
        daily_range = calculate_daily_range(type, bc, typedict)
        daily_battery_capacity = bc * bcd
        simulated_data = monte_carlo_sampling(yu, type, daily_range)
        """ Animation """
        #animate(simulated_data)
        # Calculate the total distance driven and the number of charging stops
        akm, total_stops, total_hours = return_totals(simulated_data)
        total_stops = int(total_stops)
        total_hours = int(total_hours)
        print(f"Total distance driven: {akm} km")
        daily_drive = akm / yu
        daily_time = total_hours / yu
        print(f"Daily driving time: {daily_time:,.2f} hours")
        print(f"Daily driving distance: {daily_drive:,.2f} km")

        # Use total stops to calculate the ratio dcr and pfcr. (Public fast charging stops / total stops + depot stops (one a day))
        # If nomadic driving, we never charge at depot, so dcr = 0 and pfcr = 1
        if type == 4:
            pfcr = 1
            dcr = 0
        # If we have depot charging, we need to calculate the ratio of public fast charging stops to total stops
        else:
            pfcr = total_stops / (yu + total_stops)
            dcr = 1-pfcr
        print(f"Daily Charging Ratio: {pfcr:,.2f}")

        """ Charging costs """

        # Charging
        # TODO: Add separate presentation of tax costs involved in the charging costs
        cic_installation = calculate_charger_costs(chinco, chutra, lifespan, daily_battery_capacity, yu)
        ccph_depot = calculate_ccph_depot(cic_installation, eprice)
        # Added check for nomadic driving.
        if type == 4:
            ccph_depot = 0
            eprice = 0
        # Or if type is 5,6,7,8. Change to the diesel variables
        elif type in [5, 6, 7, 8]:
            ccph_depot = 0
            ccph_fast = dieselprice
            pfcr = 1
            dcr = 0
            y3tax = dy3tax
            y4tax = dy4tax

        cic_km = calculate_cic_km(pfcr, dcr, daily_battery_capacity, ccph_fast, ccph_depot, daily_range)
        cic = cic_km * akm
        print(f"Total Charging Infrastructure Cost: {cic:,.2f}".replace(",", " ").replace(".", ",") + " SEK")

        """ Operational costs """

        # Maintenance
        maintenance_cost = calculate_maintenance_cost(mckpm, tire_factor, akm, type)

        # Driver
        driver_cost_yearly = calculate_driver_cost(total_hours, cost_driver_hourly)
        driver_cost_km = calculate_driver_cost_km(total_hours, cost_driver_hourly, akm)

       

        """ Financial Costs"""
        # TODO: Road tax
        if axles <= 3:
            road_tax = y3tax
        else:
            road_tax = y4tax

        # TODO: Depreciation by distance and time for the truck, battery already done
        mileage = akm * lifespan
        # Manually override the depreciation values for testing
        # https://publications.anl.gov/anlpubs/2021/05/167399.pdf suggests a value of 6.25e-8 per km
        dmile = 6.25e-8
        dannum = 0.2
        truck_cost = calculate_purchase_price(type, typedict)
        remaining_value = residual_value(truck_cost, dannum, dmile, lifespan, mileage)
        # dconstant = (remaining_value) / truck_cost
        print(f"Remaining Value: {remaining_value:,.2f}".replace(",", " ").replace(".", ",") + " SEK")


        # Financing
        # TODO: Tax and subsidy presentation logic for financing costs
        battery_cost = bc * battery_cost_per_kWh
        tcls = calculate_cycles(daily_range, akm, bcd) * lifespan
        # TODO: Check yearly logic of cycles, possibly adding ability to change type of usage
        print(f"Total cycles: {tcls}")
        financing_cost = calculate_financing_cost(truck_cost, battery_cost, interest_rate, lifespan, subsidy)


        print(f"Financing Cost: {financing_cost:,.2f}".replace(",", " ").replace(".", ",") + " SEK")

        # Share of total cost from battery
        bshare = battery_cost / (battery_cost + truck_cost)
        tshare = truck_cost / (battery_cost + truck_cost)
        battery_financing = financing_cost * bshare
        print(f"Battery Financing Cost: {battery_financing:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        truck_financing = financing_cost * tshare


        # Residual values
        battery_value_remaining = max(0,battery_cost * (1 - tcls / bcls))
        
        total_residual_value = remaining_value + battery_value_remaining
        print(remaining_value)
        print(f"Total Residual Value: {total_residual_value:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        """ Total costs are done below"""

        # BATTERY REPLACEMENT
        battery_replacements = tcls // bcls

        print(f"Battery replacements: {battery_replacements}")

        battery_replacement_cost = battery_cost_per_kWh * bc
        discounted_battery_cost = 0
        total_battery_replacement_cost = battery_replacement_cost * (battery_replacements)
        
        if battery_replacements > 0:
            for i in range(1, int(battery_replacements) + 1):
                replacement_year = i * lifespan / (battery_replacements + 1)
                discounted_battery_cost += battery_replacement_cost / ((1 + d) ** replacement_year)


        # Totals
        total_cost_yearly = cic + maintenance_cost + financing_cost + driver_cost_yearly + (total_battery_replacement_cost / lifespan)
        ### TCO ###
        TCO = discount(total_cost_yearly, d, lifespan) + discounted_battery_cost - total_residual_value / ((1 + d) ** lifespan)
        ### TCO ###
        print(f"Total Cost of Ownership: {TCO:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        TCO_KM = TCO / (akm * lifespan)
        print(f"Total Cost of Ownership per km: {TCO_KM:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")
        total_cost_monthly = total_cost_yearly / 12
        total_cost_per_km = total_cost_yearly / akm
        print(f"Total Cost of Ownership per km (not discounted): {total_cost_per_km:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")

        r = daily_range

        # Fixed charging cost per km
        charger_cost_per_km = cic_km
        label_charger_cost_km.config(text=f"{charger_cost_per_km:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")
        label_energy_price_km.config(text=f"{(bc * eprice) / r:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")

        label_maintenance_km.config(text=f"{maintenance_cost / akm:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")
        label_maintenance_monthly.config(text=f"{maintenance_cost / 12:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        label_maintenance_yearly.config(text=f"{maintenance_cost:,.2f}".replace(",", " ").replace(".", ",") + " SEK")

        label_driver_km.config(text=f"{driver_cost_km:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")
        label_driver_monthly.config(text=f"{driver_cost_yearly / 12:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        label_driver_yearly.config(text=f"{driver_cost_yearly:,.2f}".replace(",", " ").replace(".", ",") + " SEK")

        label_road_tax_km.config(text=f"{road_tax / akm:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")
        label_road_tax_monthly.config(text=f"{road_tax / 12:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        label_road_tax_yearly.config(text=f"{road_tax:,.2f}".replace(",", " ").replace(".", ",") + " SEK")

        label_financial_truck_km.config(text=f"{truck_financing / akm:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")
        label_financial_battery_km.config(text=f"{battery_financing / akm:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")

        label_total_per_km.config(text=f"{total_cost_per_km:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")
        label_total_monthly.config(text=f"{total_cost_monthly:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        label_total_yearly.config(text=f"{total_cost_yearly:,.2f}".replace(",", " ").replace(".", ",") + " SEK")

        label_total_TCO.config(text=f"{TCO:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        label_total_TCO_per_km.config(text=f"{TCO_KM:,.2f}".replace(",", " ").replace(".", ",") + " SEK/KM")


        """ Display the key assumptions """
        label_battery_cost.config(text=f"{battery_cost:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        label_battery_capacity.config(text=f"{bc:,.2f} kWh")
        label_daily_range.config(text=f"{daily_range:,.2f} km")
        label_truck_cost.config(text=f"{truck_cost:,.2f}".replace(",", " ").replace(".", ",") + " SEK")
        label_daily_driving_distance.config(text=f"{daily_drive:,.2f} km")
        label_daily_driving_time.config(text=f"{daily_time:,.2f} hours")
        label_days_driven_per_year.config(text=f"{yu:,.2f} days")
        label_annual_kilometers_driven.config(text=f"{akm:,.2f}".replace(",", " ").replace(".", ",") + " KM")
        label_battery_replacements.config(text=f"{battery_replacements:,.2f}")
        
        # Export Type, Daily Driving Distance, Annual Kilometers Driven, pfcr, daily_range, daily_battery_capacity, daily_time, charger_cost_per_km, maintenance_cost, driver_cost_km, road_tax_km, truck_financing, battery_financing, total_cost_per_km, total_cost_monthly, total_cost_yearly
        df = pd.DataFrame({
            "Category": ["Type", "Daily Driving Distance", "Annual Kilometers Driven", "Public Fast Charging Ratio", "Daily Range", "Daily Battery Capacity", "Daily Time", "Charger Cost per km", "Maintenance Cost per km", "Driver Cost per km", "Road Tax per km", "Truck Financing Cost per km", "Battery Financing Cost per km", "Total Cost per km", "Total Cost per month", "Total Cost per year", "TCO", "TCO per km", "Battery Replacements", "Battery Replacement Cost"],
            "Value": [typedict[type]["name"], daily_drive, akm, pfcr, daily_range, daily_battery_capacity, daily_time, charger_cost_per_km, maintenance_cost / akm, driver_cost_km, road_tax / akm, truck_financing / akm, battery_financing / akm, total_cost_per_km, total_cost_monthly, total_cost_yearly, TCO, TCO_KM, battery_replacements, battery_replacement_cost]
        })

        # Save the results to a CSV file
        type = int(type)
        save_results_to_csv(df, type)



    calculate_button = tk.Button(scrollable_frame, text="Calculate Costs", command=calculate_and_display_cic)
    calculate_button.pack(pady=10, anchor="n")

    def calculate_50_times():
        for _ in range(50):
            calculate_and_display_cic()

    calculate_button_50 = tk.Button(scrollable_frame, text="Calculate Costs 50 simulations", command=calculate_50_times)
    calculate_button_50.pack(pady=10, anchor="n") 

    