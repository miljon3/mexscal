# Module for calculating costs related to charging.

def calculate_charger_costs(chinco, chutra, lifespan, bc):
    """
    Calculate the charger costs per kWh, yearly over lifespan.
    :param lifespan: Lifespan of the charger [years]
    :param range: Range of the vehicle per full charge [km]
    :param bc: Battery capacity [kWh]
    :param chinco: Charger Installation Cost [SEK]
    :param chutra: Charger Utilization Rate (0 < chutra <= 1)
    :return: Charger cost per kWh [kr/kWh]
    """
    if chutra == 0:
        raise ValueError("Charger utilization rate must be greater than 0.")
    
    yearly_cost = chinco / lifespan
    cost_per_use = yearly_cost / chutra
    cost_per_kwh = cost_per_use / bc
    return cost_per_kwh


def calculate_cic_km(pfcr, dcr, bc, ccph_fast, ccph_slow, eprice, r):
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
    cic_fast_km = (bc * ccph_fast) / r
    cic_slow_km = (bc * ccph_slow) / r
    
    cic_km = pfcr * cic_fast_km + dcr * cic_slow_km
    return cic_km

def calculate_cic(cic_km, akm):
    """
    Calculate the total charging infrastructure cost (CIC)
    :param cic_km: Charging infrastructure cost per km
    :param akm: Annual kilometers driven
    :return: CIC (Total charging infrastructure cost)
    """
    return cic_km * akm
