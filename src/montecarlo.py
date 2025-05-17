import numpy as np
import matplotlib.pyplot as plt


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

    params = {
        1: (52, 6),    # Distribution
        2: (110, 8),    # Regional Distribution
        3: (238, 10),   # Long-range traffic
        4: (507, 11),   # Nomadic
        5: (52, 6),    # Distribution(diesel)
        6: (110, 9),    # Regional Distribution(diesel)
        7: (238, 10),   # Long-range traffic(diesel)
        8: (507, 11),   # Nomadic (diesel)
    }
    if type not in params:
        raise ValueError("Invalid type. Must be 1, 2, 3, or 4.")

    mean, std = params[type]
    daily_distances = rng.normal(mean, std, num_days)
    daily_distances = np.clip(daily_distances, 0, 800)

    # TODO: Add a condition to add stops for edge cases

    daily_stops = np.ceil(daily_distances / max_range) - 1
    daily_stops = np.clip(daily_stops, 0, None).astype(int)

    # Estimate the number of hours driven based on recorded average speeds of a day
    type_info = {
        1: (9, 6.5),
        2: (9, 14),
        3: (9, 30),
        4: (9, 64),
        5: (9, 6.5),
        6: (9, 14),
        7: (9, 30),
        8: (9, 64)
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



#simulated_data = monte_carlo_sampling(num_days=250, type=4, max_range=372)
#animate(simulated_data)
#summary_statistics(simulated_data)