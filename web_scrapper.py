import pandas as pd
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.google.com/travel/hotels/Lamu?")

def getHotels (town):
    driver.get("https://www.google.com/travel/hotels/{}?").format(town)
    headers = driver.find_elements(By.TAG_NAME, 'h2')
    hotel_names = []
    for i in headers:
        hotel_names.append(i.text)
    return hotel_names
