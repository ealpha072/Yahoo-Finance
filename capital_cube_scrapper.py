import selenium
import time
import sys
import os
import glob
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.capitalcube.com/")

#Sign in 
form = driver.find_element(By.XPATH, "//button[@type='submit']")
username = driver.find_element(By.CSS_SELECTOR, "input#loginEmail")
password = driver.find_element(By.CSS_SELECTOR, "input#loginPassword")
username.send_keys(' hebotot356@tsclip.com')
password.send_keys('12345678')
form.click()

def get_values(path_to_file):
    data = pd.read(path_to_file)
    tickers = list(data['Symbols'])
    comps = []
    search = driver.find_element(By.XPATH, '/html/body/cc-root/div[2]/cc-header/header/div/div/div/div[4]/form/div/input')
    for i in tickers:
        try:
            search.clear()
            search.send_keys(i)
            time.sleep(4)
            button = driver.find_element(By.XPATH, "/html/body/cc-root/div[2]/cc-header/header/div/div/div/div[4]/form/div/ngb-typeahead-window/button[1]")

            if(button):
                btn_text = button.text[5:len(i)+5]
                if btn_text == i:
                    button.click()
                    time.sleep(5)
                    desc = driver.find_element(By.XPATH, '/html/body/cc-root/div[2]/div/cc-stock/div/div/div[2]/cc-summary/div/div/div[8]/div/div/div[2]/div/div[1]').text
                    sector = driver.find_element(By.XPATH, '/html/body/cc-root/div[2]/div/cc-stock/div/div/div[2]/cc-summary/div/div/div[8]/div/div/div[2]/div/div[2]/table/tbody/tr[1]/td[2]').text
                    industry = driver.find_element(By.XPATH, '/html/body/cc-root/div[2]/div/cc-stock/div/div/div[2]/cc-summary/div/div/div[8]/div/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]').text
                    comps.append({'Symbol':i, 'Description':desc, 'Sect':sector, 'Industry':industry})
                    print(tickers.index(i),'Ticker: {} found'.format(i))
                    time.sleep(2)
                else:
                    print(tickers.index(i),'Ticker: {} has no correct suggestion'.format(i))
                    comps.append({'Symbol':i, 'Description':'NA', 'Sect':'NA', 'Industry':'NA'})
                    continue
            else:
                print(tickers.index(i), 'Ticker: {} not found'.format(i))
                comps.append({'Symbol':i, 'Description':'NA', 'Sect':'NA', 'Industry':'NA'})
                continue
        except:
            print(tickers.index(i),'Error', sys.exc_info()[0], 'occured')
            print(comps)
            comps.append({'Symbol':i, 'Description':'NA', 'Sect':'NA', 'Industry':'NA'})
            continue
    return comps

def combine_datasets(path):
    files = os.path.join("my_data", "*.csv")
    files = glob.glob(files)
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    data = pd.DataFrame(df)
    final_file = data.to_csv('cleaned_data.csv')
    return final_file
    
descs = get_values(symbols)