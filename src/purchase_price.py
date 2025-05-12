def calculate_purchase_price(type, type_dict):

    # 2010 EUR to 2025 EUR 39.84% - https://www.in2013dollars.com/europe/inflation/2010?amount=1
    # 1 EUR TO SEK = 10.89, 2025/05/12 - https://www.xe.com/sv/currencyconverter/convert/?Amount=1&From=EUR&To=SEK
    # Glider numbers from https://elib.dlr.de/111576/1/2017_EEVC_Kleiner%20and%20Friedrich.pdf
    EUR_FACTOR_10_25 = 1.40
    EUR_FACTOR_19_25 = 1.40  
    EUR_SEK = 10.89

    LARGE_DIESEL_ENGINE = 56.5 # EUR /kW
    ELECTRIC_MOTOR = 32.5 # EUR / kw, this value from https://www.sciencedirect.com/science/article/pii/S0306261921013659#b0385

    if type == 1 or type == 2 or type == 5 or type == 6:
        rest_of_truck = 51000*EUR_FACTOR_10_25*EUR_SEK
    elif type == 3 or type == 7:
        rest_of_truck = 56.250*EUR_FACTOR_10_25*EUR_SEK
    elif type == 4 or type == 8:
        rest_of_truck = (56.2500 +20.585)*EUR_FACTOR_10_25*EUR_SEK

    if type in range(5,9):
        powertrain = int(type_dict[type]["power"])* EUR_FACTOR_10_25*EUR_SEK * LARGE_DIESEL_ENGINE
    elif type in range(1,5):
        powertrain = int(type_dict[type]["power"])* EUR_FACTOR_19_25*EUR_SEK * ELECTRIC_MOTOR
   
    return rest_of_truck + powertrain