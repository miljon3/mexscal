import pandas as pd

# Module for calculating operational costs for TCO analysis in combination with financial costs

# Using fuelprice.py to import fuel prices.
import fuelPrice

fuelprice = fuelPrice.FuelPrice()
print(fuelprice.fuel_price())