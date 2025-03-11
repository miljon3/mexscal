import pandas as pd

# Class to represent a truck
class Truck:
    def __init__(self, name, battery_size = 0, empty_weight=0, max_payload=0, price=0, diesel_consumption = 0.1, battery_consumption = 0):
        self.name = name
        self.battery_size = battery_size
        self.empty_weight = empty_weight
        self.max_payload = max_payload
        self.price = price
        self.diesel_consumption = diesel_consumption
        self.battery_consumption = battery_consumption
        
    
    # Method to calculate payload at different gross weights, check that it is not above max_payload
    def payload_at_gross_weight(self, gross_weight):
        if gross_weight > self.max_payload + self.empty_weight:
            return self.max_payload
        else:
            return gross_weight - self.empty_weight
    
    def consumption_at_gross_weight(self, gross_weight):
        pass
    
    def payload_adjusted_consumption(self, gross_weight):
        pass

# Create a truck object
truck = Truck('Volvo FH42T E', 'BET', 330, 9935, 50000, 1000000)
    