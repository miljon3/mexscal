import numpy as np
import matplotlib.pyplot as plt

""" Uncomment to test the function """
#simulated_data = monte_carlo_sampling(num_days=250, type=4, max_range=372)
#animate(simulated_data)
#summary_statistics(simulated_data)

def monte_carlo_sampling(num_days, type, max_range):
    """
    Simulate the Monte Carlo sampling for a given number of days and type of sampling.

    Parameters:
    num_days (int): Number of days of driving to simulate.
    type (int): Type of truck to sample: 1 (Distribution),2(Regional Distribution),3(Long range trafic),4(Nomadic).
    max_range (int): Maximum range of the truck on one discharge.

    Returns:
    np.ndarray: Array of sampled daily distances, their respective required charging stops and the hours driven.
    """

    # Create a dedicated generator instance
    rng = np.random.default_rng()

    # TODO: Check these numbers and add input for them
    params = {
        1: (160, 40),    # Distribution
        2: (160, 40),    # Distribution
        3: (320, 80),    # Regional Distribution
        4: (320, 80),    # Regional Distribution
        5: (500, 125),   # Long-range traffic
        6: (500, 125),   # Long-range traffic
        7: (720, 180),   # Nomadic
        8: (720, 180),   # Nomadic
    }

    if type not in params:
        raise ValueError("Invalid type. Must be 1, 2, 3, or 4.")

    mean, std = params[type]
    daily_distances = rng.normal(mean, std, num_days)
    daily_distances = np.clip(daily_distances, 0, 800)

    # TODO: Add a condition to add stops for edge cases

    daily_stops = np.ceil(daily_distances / max_range) - 1
    daily_stops = np.clip(daily_stops, 0, None).astype(int)

    # TODO: Check hour calculation logic
    """ Maximum possible hours is 9 per day, except in type 3 and 4 where it is 10 (Technically its 10 hours maximum two times per week, but we use 10 hours for simplicity) """
    """ However the average speed will vary depending on type of driving"""
    """ For example, for type 1, the average speed is 25 km/h, so 9 hours = 225 km"""
    """ For type 2, the average speed is 40 km/h, so 9 hours = 360 km"""
    """ For type 3, the average speed is 60 km/h, so 10 hours = 600 km"""
    """ For type 4, the average speed is 70 km/h, so 10 hours = 700 km"""
    """ As long as the distance is equal or more than the average speed, we assume that the truck was driven for 9 or 10 hours"""
    """ If it is less, we check if the truck was driven for 8 hours, then 7 hours, etc."""
    # Define max hours and speed per type
    type_info = {
        1: (9, 25),
        2: (9, 25),
        3: (9, 40),
        4: (9, 40),
        5: (10, 60),
        6: (10, 60),
        7: (10, 70),
        8: (10, 70)
    }

    max_hours, avg_speed = type_info[type]
    daily_hours = np.zeros_like(daily_distances, dtype=int)

    for h in range(max_hours, 0, -1):
        mask = (daily_hours == 0) & (daily_distances >= h * avg_speed)
        daily_hours[mask] = h

    # Clamp minimum to 1 hour, since we assume the truck is always driven at least 1 hour per active day
    daily_hours[daily_hours == 0] = 1
    return np.column_stack((daily_distances, daily_stops, daily_hours))


def animate(simulated_data):
    distances = simulated_data[:, 0]
    stops = simulated_data[:, 1].astype(int)
    num_unique_stops = stops.max() + 1
    colors = plt.cm.viridis(np.linspace(0, 1, num_unique_stops))

    plt.figure(figsize=(10, 6))
    for stop_count in range(num_unique_stops):
        mask = stops == stop_count
        plt.hist(distances[mask], bins=30, alpha=0.7, label=f"{stop_count} stop(s)", color=colors[stop_count])

    plt.xlabel('Daily Distance Driven (km)')
    plt.ylabel('Frequency')
    plt.title('Daily Driving Distance Colored by Charging Stops')
    plt.legend(title='Charging Stops')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def summary_statistics(simulated_data):
    """
    Calculate and print summary statistics for the simulated data.

    Parameters:
    simulated_data (np.ndarray): Array of sampled daily distances and their respective required charging stops.
    """
    # Calculate summary statistics
    total_days = simulated_data.shape[0]
    avg_distance = np.mean(simulated_data[:, 0])
    max_distance = np.max(simulated_data[:, 0])
    min_distance = np.min(simulated_data[:, 0])
    avg_stops = np.mean(simulated_data[:, 1])
    max_stops = int(np.max(simulated_data[:, 1]))
    stop_distribution = np.bincount(simulated_data[:, 1].astype(int))

    print(f"Total simulated days: {total_days}")
    print(f"Average daily distance: {avg_distance:.1f} km")
    print(f"Min/Max daily distance: {min_distance:.1f} km / {max_distance:.1f} km")
    print(f"Average charging stops per day: {avg_stops:.2f}")
    print(f"Maximum charging stops in a day: {max_stops}")
    print("\nCharging stop distribution:")
    for i, count in enumerate(stop_distribution):
        print(f"  {i} stop(s): {count} days")


def return_totals(simulated_data):
    """
    Calculate and return the total distance driven and total charging stops.

    Parameters:
    simulated_data (np.ndarray): Array of sampled daily distances and their respective required charging stops.

    Returns:
    tuple: Total distance, stops, and hours driven.
    """

    total_distance = np.sum(simulated_data[:, 0])
    total_stops = np.sum(simulated_data[:, 1])
    total_hours = np.sum(simulated_data[:, 2])
    return total_distance, total_stops, total_hours



