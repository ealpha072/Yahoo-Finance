import http.client
import json
import pandas as pd
import numpy as np
import sys

def get_summ(path, api_key):
    data = pd.read_csv(path)
    tickers = [i for i in list(data['Symbol'])]
    conn = http.client.HTTPSConnection("yh-finance.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Host': "yh-finance.p.rapidapi.com",
        'X-RapidAPI-Key': api_key
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