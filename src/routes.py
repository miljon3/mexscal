import pandas as pd

# This file takes a route and displays the amount of breaks required and if it's possible to do the route
# in the given time. 270 minutes is the maximum time before a 45-minute break is required.
def calculate_breaks(route):
    """
    Calculate the number of breaks required for a given route.
    
    :param route: List of tuples with (location, time) where time is in minutes
    :return: Number of breaks required
    """
    total_time = sum([time for _, time in route])
    
    # Calculate number of breaks needed based on 270 minutes of driving
    breaks = total_time // 270
    return breaks

def calculate_charging(route, vehicle_range, avg_speed=60):
    """
    Calculate the number of charging stops needed for a given route.
    
    :param route: Distance of the route in km
    :param vehicle_range: Range of the vehicle in km
    :param avg_speed: Average speed in km/h
    :return: Number of charging stops needed
    """
    
    # Calculate number of charging stops needed based on vehicle range
    charging_stops = route // vehicle_range
    return charging_stops


def display_route(route, time_limit, vehicle_range, avg_speed):
    """
    Displays the route and checks if it can be done with or without breaks.
    Also checks with the range of the vehicle.
    """
    
    # Check the time needed for the route with the average speed and distance.
    total_time = route / avg_speed
    if total_time > time_limit:
        print("The route cannot be done in the given time limit.")
        breaks = calculate_breaks(total_time)
        print(f"You will need {breaks} breaks.")
    else:
        print("The route can be done in the given time limit, checking for charging breaks.")
        charging_stops = calculate_charging(route, vehicle_range, avg_speed)
        if charging_stops > 0:
            print(f"You will need {charging_stops} charging stops.")
        else:
            print("No charging stops needed.")
        


# Test
display_route(500, 270, 465, 60)

    