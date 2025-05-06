import math 
def calculate_daily_range(type, bc, type_dict):
    """
    Calculate the daily range based on consumption (r)
    :param type: Type of usage (1, 2, 3, or 4)
    :param weight: Weight of the vehicle (in kg)
    :return: r: daily range in km
    """
    weight = int(type_dict[type]["weight"]) * 1000
    # ICT 5-8
    if type in range(5, 9):
        consumption = 0.0903*math.log(weight) -0.6404
        r = bc / consumption
    # BET 1-4
    elif type in range(1, 5):
        consumption = 0.3814*math.log(weight) -2.6735
        r = bc / consumption
    return r