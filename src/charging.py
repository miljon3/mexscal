# Module for calculating costs related to charging.

def calculate_cic_km(pfcr, dcr, bc, ccph_fast, ccph_slow, r):
    """
    Calculate the charging infrastructure cost per kilometre (CIC_KM)
    :param pfcr: Fraction of energy charged at public fast chargers
    :param dcr: Fraction of energy charged at depot chargers
    :param bc: Battery capacity [kWh]
    :param ccph_fast: Charging infrastructure cost per kWh for public fast chargers [SEK/kWh]
    :param ccph_slow: Charging infrastructure cost per kWh for depot chargers [SEK/kWh]
    :param r: Range of the vehicle per full charge [km]
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
