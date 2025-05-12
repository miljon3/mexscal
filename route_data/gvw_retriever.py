from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import time
import pandas as pd

df = pd.read_csv("vehicle_weights.csv")

df_cleaned = df.drop_duplicates()

df_cleaned.to_csv("cleaned_file.csv", index=False)

exit()

plates = []
# List of license plates
with open("route_data/plates.txt", "r") as file:
    for line in file:
        plates.append(line.strip())

# Set up headless Chrome with webdriver-manager
options = webdriver.ChromeOptions()


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("length of plates", len(plates))
with open("vehicle_weights.csv", "r") as file:
    next(file)
    for line in file:
        split_line = line.split(",")
        if int(split_line[1]) != 0:
            plates.remove(split_line[0])
print("length of plates after clean", len(plates))

# Create CSV output
with open("vehicle_weights_2.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Plate", "Totalvikt", "Släpvikt"])
    for plate in plates:
        try:
            url = "https://fordon-fu-regnr.transportstyrelsen.se/"
            driver.get(url)
            time.sleep(3)
            wait = WebDriverWait(driver, 30)

            reg_field = wait.until(EC.visibility_of_element_located((By.NAME, 'Registreringsnummer')))
            reg_field.send_keys(plate.strip())
            reg_field.send_keys(Keys.RETURN)

            time.sleep(1)

            driver.find_element(By.XPATH, '//a[@href="#ts-teknik-heading"]').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//a[@href="#ts-MattVikt-heading"]').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//a[@href="#koppling"]').click()
            time.sleep(2)

            # Extract values
            totalvikt_elem = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div[1]/div[1]/div/form/div[1]/div[7]/div[2]/div/div/div[2]/div[2]/div/div/div[6]/p')
            totalvikt = totalvikt_elem.text.strip().split(" ")[0]
            totalvikt = totalvikt.split("\n")
            totalvikt = totalvikt[1]

            try:
                slapvikt_elem = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div[1]/div[1]/div/form/div[1]/div[7]/div[2]/div/div/div[4]/div[2]/div/div[2]/div[2]/p')
                slapvikt = slapvikt_elem.text.strip().split(" ")[1]
                slapvikt = slapvikt.split("\n")
                slapvikt = slapvikt[1]
            except Exception as e:
                print("Inget släp :)")
                slapvikt = 0

            # Write only if both values were fetched
            writer.writerow([plate.strip(), totalvikt, slapvikt])
            print(f"Saved {plate}: {totalvikt} / {slapvikt}")

        except Exception as e:
            print(f"❌ Failed for {plate}: {e}")
            writer.writerow([plate.strip(), 0, 0])
        time.sleep(40)


driver.quit()
