import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# Function to send email
def send_email(subject, body, to_email):
    from_email = "censored"
    password = "censored"  
    
    initial_message_id = "<censored>"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.add_header('In-Reply-To', initial_message_id)
    msg.add_header('References', initial_message_id)

    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Reply sent successfully!")
    except Exception as e:
        print(f"Failed to send reply: {e}")

# Function to initialize the WebDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver_path = "censored"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to open Google Flights
def open_google_flights(driver):
    driver.get('https://www.google.com/flights')
    time.sleep(2)

# Function to set departure airport
def set_departure(driver, departure_city):
    departure_input = driver.find_element(By.XPATH, '//input[@aria-label="Where from?"]')
    departure_input.clear()
    departure_input.send_keys(departure_city)
    time.sleep(3)
    departure_input = driver.find_element(By.XPATH, f'//*[@aria-label="{departure_city}, United Kingdom"]')
    departure_input.click()
    time.sleep(3)

# Function to set destination airports
def select_destination(driver, destination_city, destination_country):
    destination_input = driver.find_element(By.XPATH, "//input[contains(@aria-label, 'Where to')]")
    destination_input.clear()
    destination_input.send_keys(destination_city)
    time.sleep(3)
    destination_input = driver.find_element(By.XPATH, f'//*[@aria-label="{destination_city}, {destination_country}"]')
    destination_input.click()
    time.sleep(3)

# Function to adjust trip length to 4 days
def set_days(driver, example_city):
    destination_input = driver.find_element(By.XPATH, "//input[contains(@aria-label, 'Where to')]")
    destination_input.clear()
    destination_input.send_keys(example_city)
    time.sleep(3)
    destination_input = driver.find_element(By.XPATH, f'//*[@aria-label="{example_city}, France"]')
    destination_input.click()
    time.sleep(3)

    departure_input = driver.find_element(By.XPATH, '//input[@aria-label="Departure"]')
    departure_input.click()
    time.sleep(3)

    for _ in range(3):
        try:
            length_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc LjDxcd XhPA0b LQeN7 MWXAnd"]'))
            )
            length_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking length button: {e}")
    
    time.sleep(3)

# Function to open the departure calendar and navigate to January 2025
def navigate_to_january(driver):
    departure_input = driver.find_element(By.XPATH, '//input[@aria-label="Departure"]')
    departure_input.click()
    time.sleep(3)

    for _ in range(4):
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"]'))
            )
            next_button.click()
            time.sleep(2)  
        except Exception as e:
            print(f"Error navigating to January: {e}")

# Function to scrape the prices and dates
def scrape_flights(driver):
    flights = []
    seen_dates = set()

    for _ in range(4):  
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label]'))
            )
        except Exception as e:
            print(f"Error while waiting for the page to load: {e}")
        

        dates = driver.find_elements(By.XPATH, '//div[@class="eoY5cb CylAxb sLG56c yCya5"]')
        prices = driver.find_elements(By.XPATH, '//div[contains(@class, "UNMzKf")]')

        for date, price in zip(dates, prices):
            try:
                
                full_date = date.get_attribute("aria-label")  
                price_text = price.text.replace('$', '')  
                if price_text.isdigit():  
                    date_obj = datetime.strptime(full_date, '%A, %B %d, %Y')
                    if date_obj.year == 2025 and date_obj.month >= 1:
                        if (full_date, price_text) not in seen_dates:  
                            seen_dates.add((full_date, price_text))  
                            flights.append((full_date, int(price_text)))   
            except Exception as e:
                print(f"Error processing date or price: {e}")

        next_button = driver.find_element(By.XPATH, '//button[@aria-label="Next"]')
        next_button.click()
        time.sleep(2)

    return flights

# Main function
def main():
    destinations = ["Berlin", "Paris", "Oslo", "Stockholm", "Rome", "Madrid", "Barcelona", "Amsterdam", "İstanbul", "Reykjavík", 
                    "Zürich", "Florence", "Lisbon", "Skopje", "Warsaw", "Prague", "Munich", "Copenhagen", "Helsinki", "Tromsø Municipality",
                    "Budapest", "Athens", "Vienna", "Milan", "Cannes", "Valencia", "Gothenburg"] 
    countries = ["Germany", "France", "Norway", "Sweden", "Italy", "Spain", "Spain", "Netherlands", "Türkiye", "Iceland", 
                 "Switzerland", "Italy", "Portugal", "North Macedonia", "Poland", "Czechia", "Germany", "Denmark", "Finland", "Norway",
                 "Hungary", "Greece", "Austria", "Italy", "France", "Spain", "Sweden"]

    driver = init_driver()
    open_google_flights(driver)
    set_departure(driver, "London")
    
    email_body = ""
    
    set_days(driver, "Paris")

    
    for (destination, country) in zip(destinations, countries):
        select_destination(driver, destination, country)
        navigate_to_january(driver)
        flights = scrape_flights(driver)
        sorted_flights = sorted(flights, key=lambda x: x[1])
        cheapest_flights = sorted_flights[:5]

        email_body += f"Destination: {destination}, {country}\n"
        for date, price in cheapest_flights:
            email_body += f"Date: {date}, Price: ${price}\n"
        email_body += "\n"
    
    send_email("Flight Update", email_body, "censored")
    
    driver.quit()

# Entry point of the script
if __name__ == "__main__":
    main()
