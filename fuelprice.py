import pandas

class FuelPrice:
    def __init__(fuel):
        fuel.df = pandas.read_excel('ASEK/A3_2.xlsx')
    
    def fuel_price(fuel, year):
        # Create a new dataframe and key it by year, then select just the relevant price data.
        df = fuel.df[year]
        eDf = df.iloc[[7,8]]
        return eDf

fuelprice = FuelPrice()
print(fuelprice.fuel_price(2019))

