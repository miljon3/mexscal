import math

typedict = {
            1: {
                "name": "Distribution",
                "weight": "18",
                "fuel": "Electric"
            },
            2: {
                "name": "Regional Distribution",
                "weight": "18",
                "fuel": "Electric"
            },
            3: {
                "name": "Long Range Traffic",
                "weight": "42",
                "fuel": "Electric"
            },
            4: {
                "name": "Nomadic",
                "weight": "72",
                "fuel": "Electric"
            },
            5: {
                "name": "Distribution (diesel)",
                "weight": "18",
                "fuel": "Diesel"
            },
            6: {
                "name": "Regional Distribution (diesel)",
                "weight": "18",
                "fuel": "Diesel"
            },
            7: {
                "name": "Long Range Traffic (diesel)",
                "weight": "42",
                "fuel": "Diesel"
            },
            8: {
                "name": "Nomadic (diesel)",
                "weight": "72",
                "fuel": "Diesel"
            }
        }

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


def calc_battery_size():
    ### BATTERY SIZING CALCULATIONS
    for i in range(100,2000):
        r = calculate_daily_range(4, i, type_dict=typedict)
        if r*0.8 > 507.46:
            print(i)
            break

#calc_battery_size()

# type 1, average distance is 51.7 km, result = 69 kWh
# type 2, average distance is 110.35 km, result = 147 kWh
# type 3, average distance is 238.24 km, result = 413 kWh
# type 4, average distance is 507.46 km, result = 1010 kWh