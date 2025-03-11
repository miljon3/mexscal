import pandas as pd

# Module for calculating operational costs for TCO analysis in combination with financial costs

# Using fuelprice.py to import fuel prices.
import fuelPrice, electricPrice

fp = fuelPrice.FuelPrice()
ep = electricPrice.ElectricPrice()

print(fp.get_kilometer_price(), ep.get_kilometer_price())

# Put the kilometer price from fuel and electricity into a dictionary.
kilometer_prices = {
    'ICE': fp.get_kilometer_price(),
    'BET': ep.get_kilometer_price()
}

# Create a dataframe with the kilometer prices.
df = pd.DataFrame(kilometer_prices, index = ["Kr/km"])

print(df)