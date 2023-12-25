import requests
import json
import pandas as pd
import numpy as np
import glob
import os

data_set = pd.read_csv('HS Codes used.csv')
codes = list(data_set['HS Code'])

def createData(codes):
    # print(tickers.index(i) ,"Symbol, {} found".format(i))
    final_list = []
    empty_hs_codes = []
    for i in codes:
        url = 'https://comtrade.un.org/api/get?max=502&type=C&freq=A&px=HS&ps=2016%2C2017%2C2018&r=all&p=0&rg=1&cc={}'.format(i)
        
        response = requests.get(url)
        if response.ok:
            code_data_contents = response.content
            json_object = json.loads(code_data_contents)
            
            if json_object['dataset'] == []:
                print(codes.index(i), 'Code {}, This dataset is empty'.format(i))
                empty_hs_codes.append(i)
            else:
                print(codes.index(i), 'HS Code, {} found'.format(i))
                df = pd.DataFrame.from_dict(json_object['dataset'])
                final_list.append(df)
        else:
            print(codes.index(i), "HS Code, {} caused an error".format(i))
            print(response.content.decode('utf-16-be'))
            break
    print(empty_hs_codes)
    return pd.concat(final_list)
