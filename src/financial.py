def calculate_financing_cost(truck_cost, battery_cost, interest_rate, loan_term_years, subsidy):
    """
    Calculate the annual loan repayment cost (cash outflow) for a truck purchase after subsidy.
    
    :param truck_cost: Cost of the truck [SEK]
    :param battery_cost: Cost of the battery [SEK]
    :param interest_rate: Annual interest rate (as a decimal)
    :param loan_term_years: Loan term in years
    :param subsidy: Subsidy percentage (as a decimal)
    :return: Annual loan payment [SEK]
    """
    # Apply subsidy
    total_cost = (truck_cost + battery_cost) * (1 - subsidy)

    # Convert to monthly terms
    monthly_interest_rate = interest_rate / 12
    number_of_payments = loan_term_years * 12

    monthly_payment = (total_cost * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -number_of_payments)

    annual_payment = monthly_payment * 12
    return annual_payment
