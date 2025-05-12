# Placeholder for calculating maintenance costs

def calculate_maintenance_cost(mcpkm, tire_factor, akm, type):
    """
    Calculate the maintenance cost per kilometre (MCPKM)
    :param mcpkm: Maintenance cost per kilometre
    :param akm: Annual kilometers driven
    :return: amc: Annual maintenance costs
    """
    if type in range(1,5):
        return mcpkm *(1+tire_factor*0.2)* akm * 0.7
    else:
        return mcpkm *(1+tire_factor*0.2)* akm * 0.7

def maintenance_per_km(mcpkm, type):
    """
    Calculate the maintenance cost per kilometre (MCPKM)
    :param mcpkm: Maintenance cost per kilometre
    :return: amc: Annual maintenance costs
    """
    return mcpkm

