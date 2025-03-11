import pandas as pd

class FuelPrice:
    def __init__(fuel):
        fuel.df = pd.read_excel('ASEK/A3_2.xlsx')
    
    # 2019 should be set as default year in all places.
    def get_price(fuel, year = 2019):
        # Create a new dataframe and key it by year, then select the relevant data and export is as variables.
        df = fuel.df[year]
        fuel = df.iloc[8]
        return fuel
    def get_kilometer_price(fuel, year = 2019, consumption = 0.4):
        fuel_cost = fuel.get_price(year)
        return consumption * fuel_cost

fuelprice = FuelPrice()
# Leave () empty to use 2019, specify other years.
print(fuelprice.get_kilometer_price())

