import pandas as pd

class ElectricPrice:
    def __init__(self):
        self.df = pd.read_excel('ASEK/8_3.xlsx')
    
    # 2019 should be set as default year in all places.
    def get_price(self, year = 2019):
        # Creates a new dataframe and key it by year, then select the relevant data and export is as variables.
        # Do this to avoid having to reference the largest dataframes several times.
        df = self.df[year]
        # Converting öre/kWh to kr/kWh
        regionalElectric = df.iloc[4]/100
        ldElectric = df.iloc[10]/100
        return regionalElectric, ldElectric
    
    # Using approximate figure for consumption, should use actual consumption in the future.
    def get_kilometer_price(self, year = 2019, consumption = 1.4):
        regionalElectric, ldElectric = self.get_price(year)
        return consumption * (regionalElectric + ldElectric)/2

electricPrice = ElectricPrice()
# Leave () empty to use 2019, specify other years.
print(electricPrice.get_kilometer_price())

