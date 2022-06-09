import pandas as pd
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.capitalcube.com/login")

#Capital Cube web scrapper
form = driver.find_element(By.XPATH, "//button[@type='submit']")
username = driver.find_element(By.CSS_SELECTOR, "input#loginEmail")
password = driver.find_element(By.CSS_SELECTOR, "input#loginPassword")
username.send_keys(' hebotot356@tsclip.com')
password.send_keys('12345678')
form.click()

search_btn = driver.find_element(By.XPATH, "//form/div[@class='input-group w-100']/div[@class='input-group-append']")
search_input = driver.find_element(By.NAME, "search")
search_input.clear()
search_input.send_keys('unilever')

list_opt = driver.find_element(By.XPATH, "//button[@role='option']")
list_opt.click()

stock_info = driver.find_elements(By.XPATH, "//div[@class='card shadow-none border-0']")
results = driver.find_elements(By.XPATH, "//div[@class='row']/div[@class = 'col-md-8 text-justify mb-4']")

desc = results[0].text
tick = stock_info[0].text
tick = tick.split('\n')
company_name = tick[1]
stock_symbol = tick[0]

data = pd.DataFrame([[company_name, stock_symbol, desc]], columns=['Company Name', 'Stock Symbol', 'Description'])
gen_data = data.to_csv('data.csv')

## Yahoo Finance web scrapper
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://finance.yahoo.com/")

element = driver.find_element(By.CSS_SELECTOR, "input#yfin-usr-qry")
element.send_keys('tesla')
form = driver.find_elements(By.CSS_SELECTOR, "form#header-search-form")
form[0].submit()
#ticker_elem = driver.find_element(By.CSS_SELECTOR, "h1").text
profile = driver.find_element(By.XPATH, "//div[@id ='quote-nav']/ul/li[@data-test='COMPANY_PROFILE']/a")
profile.click()
ticker_elem = driver.find_element(By.CSS_SELECTOR, "h1").text
description = driver.find_element(By.XPATH, "//section[@class='quote-sub-section Mt(30px)']/p").text

split_ticker = ticker_elem.split(' ')
symbol = split_ticker[-1]
name = split_ticker[:-1]
name = ' '.join(name)
df = pd.DataFrame([[name, symbol, description.text]], columns= ['Stock name','Stock symbol', 'Description'])

