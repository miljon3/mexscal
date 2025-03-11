import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
from datetime import date

# Class for loan represenation to use with financial costs
class Loan:
    def __init__(self, principal, interest_rate, years, payments_per_year=12, addl_principal=0, start_date=date.today()):
        self.principal = principal
        self.interest_rate = interest_rate
        self.years = years
        self.payments_per_year = payments_per_year
        self.addl_principal = -abs(addl_principal)  # Ensure it's negative
        self.start_date = start_date
        self.schedule = self._generate_amortization_schedule()

    def _generate_amortization_schedule(self):
        # Amortization schedule, adjustable for more aggressive or less aggressive payment plans.
        periods = self.years * self.payments_per_year
        dates = pd.date_range(self.start_date, periods=periods, freq='MS')

        df = pd.DataFrame(index=dates, columns=['Payment', 'Principal', 'Interest', 'Addl_Principal', 'Balance'], dtype='float')
        df.index.name = "Date"

        per_payment = npf.pmt(self.interest_rate / self.payments_per_year, periods, self.principal)
        df["Payment"] = per_payment
        df["Principal"] = npf.ppmt(self.interest_rate / self.payments_per_year, np.arange(1, periods + 1), periods, self.principal)
        df["Interest"] = npf.ipmt(self.interest_rate / self.payments_per_year, np.arange(1, periods + 1), periods, self.principal)
        df["Addl_Principal"] = self.addl_principal

        df["Cumulative_Principal"] = (df["Principal"] + df["Addl_Principal"]).cumsum().clip(lower=-self.principal)
        df["Balance"] = self.principal + df["Cumulative_Principal"]

        return df

    def plot_amortization(self):
        # Plot example for future visualization needs. Unused as of now.
        plt.figure(figsize=(10, 5))
        plt.plot(self.schedule.index, self.schedule["Balance"], label="Remaining Balance", color='blue')
        plt.fill_between(self.schedule.index, self.schedule["Balance"], color='blue', alpha=0.1)
        plt.xlabel("Date")
        plt.ylabel("Loan Balance")
        plt.title("Loan Amortization Over Time")
        plt.legend()
        plt.grid()
        plt.show()

    def get_schedule(self):
        # Returns a dataframe of the amortization schedule.
        return self.schedule.copy()
    
# Example usage, loan of 1 millionm with 5% interest over 5 years
loan = Loan(principal=1000000, interest_rate=0.05, years=5)

# Get the amortization schedule
df = loan.get_schedule()
print(df.head())

