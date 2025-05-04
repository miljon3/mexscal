def calculate_driver_cost(total_hours, driver_cost_per_hour):
    """
    Calculate the driver cost per year based on total hours driven.
    
    :param total_hours: Total hours driven
    :param driver_cost_per_hour: Driver cost per hour [SEK]
    :return: Driver cost per kilometer [SEK/km]
    """
    return (total_hours * driver_cost_per_hour)

def calculate_driver_cost_km(total_hours, driver_cost_per_hour, akm):
    """
    Calculate the driver cost per kilometer based on total hours driven.
    
    :param total_hours: Total hours driven
    :param driver_cost_per_hour: Driver cost per hour [SEK]
    :param akm: Annual kilometers driven
    :return: Driver cost per kilometer [SEK/km]
    """
    return (total_hours * driver_cost_per_hour) / akm

    