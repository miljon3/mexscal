# Placeholder for calculating maintenance costs

def calculate_maintenance_cost(mcpkm, tire_factor, akm):
    """
    Calculate the maintenance cost per kilometre (MCPKM)
    :param mcpkm: Maintenance cost per kilometre
    :param akm: Annual kilometers driven
    :return: amc: Annual maintenance costs
    """
    return mcpkm *(1+tire_factor*0.2)* akm

def maintenance_per_km(mcpkm):
    """
    Calculate the maintenance cost per kilometre (MCPKM)
    :param mcpkm: Maintenance cost per kilometre
    :return: amc: Annual maintenance costs
    """
    return mcpkm

