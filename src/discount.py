def discount(yearly_cost, discount_rate, years):
    """
    Calculate the present value of a series of future cash flows (yearly costs) using a discount rate.
    
    :param yearly_cost: The cost incurred each year
    :param discount_rate: The discount rate (as a decimal, e.g. 0.05 for 5%)
    :param years: The number of years over which the costs are incurred
    :return: The present value of the future cash flows
    """
    return yearly_cost * ((1 - (1 + discount_rate) ** -years) / discount_rate)