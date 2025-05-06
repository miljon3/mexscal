import math 
def calculate_daily_range(type, bc):
    """
    Calculate the daily range based on consumption (r)
    :param type: Type of usage (1, 2, 3, or 4)
    :param weight: Weight of the vehicle (in kg)
    :return: r: daily range in km
    """
    print(type)
    weight = 1
    if type == 1 or type == 2:
        consumption = 0.3814*math.log(weight)*(-2.6735)
        range = bc / consumption
    elif type == 3 or type == 4:
        consumption = 0.0903*math.log(weight)*(-0.0604)
        range = bc / consumption
    return range