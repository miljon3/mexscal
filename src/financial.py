def calculate_financing_cost(truck_cost, battery_cost, interest_rate, loan_term_years, subsidy, remaining_value):
    """
    Calculate the financing cost of a truck after applying subsidy and accounting for remaining value.
    
    :param truck_cost: Cost of the truck [SEK]
    :param battery_cost: Cost of the battery [SEK]
    :param interest_rate: Annual interest rate (as a decimal)
    :param loan_term_years: Loan term in years
    :param subsidy: Subsidy percentage (as a decimal, e.g. 0.2 for 20%)
    :param remaining_value: Remaining value percentage at end of loan (as a decimal)
    :return: Total financing cost over the loan term [SEK]
    """
    # Apply subsidy to the cost
    total_cost = (truck_cost + battery_cost) * (1 - subsidy)
    print(f"Total cost after subsidy: {total_cost:.2f} SEK")
    
    # Calculate monthly payment
    monthly_interest_rate = interest_rate / 12

    number_of_payments = loan_term_years * 12

    monthly_payment = (total_cost * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -number_of_payments)
    print(f"Monthly payment: {monthly_payment:.2f} SEK")
    
    # Total cost subtracting remaining value
    yearly_financing_cost = ((monthly_payment * number_of_payments) - (total_cost * remaining_value))/loan_term_years
    print(f"Total financing cost: {yearly_financing_cost:.2f} SEK")
    return yearly_financing_cost
