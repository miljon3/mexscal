import numpy as np

def residual_value(P0, alpha, beta, a, m):
    """
    Calculate the residual value of a truck based on age and mileage.

    Parameters:
    P0 (float): Initial purchase price [SEK]
    alpha (float): Depreciation rate per year
    beta (float): Depreciation rate per kilometre
    a (float): Age of the truck [years]
    m (float): Mileage of the truck [Km]

    Returns:
    float: Residual value [SEK]
    """
    return P0 * np.exp(-alpha * a - beta * m)
