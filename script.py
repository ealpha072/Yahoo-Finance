import http.client
import pprint 
import json
import pandas as pd
import sys
import os
import glob
import numpy as np

data = pd.read_csv("quotes (2).csv")
symbols = list(data['Symbol'])

##fix dataframe reading
#deal with errors
#api key 
def get_summ(tickers):
    conn = http.client.HTTPSConnection("yh-finance.p.rapidapi.com")
    headers = {
         'X-RapidAPI-Host': "yh-finance.p.rapidapi.com",
        'X-RapidAPI-Key': "873bfa8fe6mshf78eca5dfb72fe2p16e11fjsnf3c21ea59a6e"
        }
    desc = []
    
    for i in tickers:
        try:
            conn.request("GET", "/stock/v2/get-summary?symbol={}".format(i), headers=headers)
            res = conn.getresponse()
            data = res.read()
            df = json.loads(data)
            summ = df["summaryProfile"]
            key_to_find = 'longBusinessSummary'
            if key_to_find in summ:
                prof = summ[key_to_find]
            else:
                prof = 'Not Found'
            print(tickers.index(i) ,"Symbol, {} found".format(i))
            desc.append({'Symbol':i, 'Description':prof})
        except:
            print(tickers.index(i),'Error', sys.exc_info()[0], 'occured')
            print()
    return pd.DataFrame(desc)