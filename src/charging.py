# Module for calculating costs related to charging.

def calculate_charger_costs(chinco, chutra, lifespan, bc, yu):
    """
    Calculate the charger costs per kWh, yearly over lifespan.
    :param lifespan: Lifespan of the charger [years]
    :param range: Range of the vehicle per full charge [km]
    :param bc: Battery capacity [kWh]
    :param chinco: Charger Installation Cost [SEK]
    :param chutra: Charger Utilization Rate (0 < chutra <= 1)
    :param yu: Yearly uses of the charger
    :return: Charger cost per kWh [kr/kWh]
    """
    if chutra == 0:
        raise ValueError("Charger utilization rate must be greater than 0.")
    
    yearly_cost = chinco / lifespan
    cost_per_use = yearly_cost / chutra / yu
    cost_per_kwh = cost_per_use / bc
    return cost_per_kwh

def calculate_ccph_depot(cpkwh, eprice):
    """
    Calculate the cost per kWh for depot chargers
    :param cpkwh: Cost per kWh for depot chargers [SEK/kWh] from calculate_charger_costs
    :param eprice: Electricity price [SEK/kWh]
    :return: CIC per kWh for depot chargers [SEK/kWh] to replace ccph_slow
    """
    if cpkwh == 0:
        raise ValueError("Cost per kWh for depot chargers must be greater than 0.")
    
    ccph_depot = cpkwh + eprice
    return ccph_depot


def calculate_cic_km(pfcr, dcr, bc, ccph_fast, ccph_depot, r):
    """
    Calculate the charging infrastructure cost per kilometre (CIC_KM)
    :param pfcr: Fraction of energy charged at public fast chargers
    :param dcr: Fraction of energy charged at depot chargers
    :param bc: Battery capacity [kWh]
    :param ccph_fast: Charging infrastructure cost per kWh for public fast chargers [SEK/kWh]
    :param ccph_slow: Charging infrastructure cost per kWh for depot chargers [SEK/kWh]
    :param r: Range of the vehicle per full charge [km]
    :param eprice: Electricity price [SEK/kWh]
    :return: CIC_KM (Charging infrastructure cost per km)
    """
    print(f"Public Fast Charging Ratio: {pfcr:.2f}")
    print(f"Depot Charging Ratio: {dcr:.2f}")
    # TODO: Evaluate if bcd should be used
    cic_fast_km = (bc * ccph_fast) / r
    cic_slow_km = (bc * ccph_depot) / r
    print(f"Charging Infrastructure Cost per km (Fast): {cic_fast_km:.2f} SEK/km")
    print(f"Charging Infrastructure Cost per km (Depot): {cic_slow_km:.2f} SEK/km")
    
    cic_km = pfcr * cic_fast_km + dcr * cic_slow_km
    return cic_km

def calculate_cycles(r, km, cd):
    """
    Calculate the number of cycles based on battery capacity, range, and kilometers driven.
    :param bc: Battery capacity [kWh]
    :param r: Range of the vehicle per full charge [km]
    :param km: Kilometers driven [km]
    :param cd: Cycle Discharge [%] e.g 0.8 for 80% discharge from 90% to 10% etc.
    :return: Number of cycles
    """
    print(f"Range: {r} km")
    print(f"Kilometers driven: {km} km")
    # print(f"Cycle discharge: {cd} %")
    # cycles = (km / r) * cd
    cycles = (km / r)

    

    print(f"Total cycles: {cycles} cycles")

    return cycles
