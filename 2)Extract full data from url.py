import json
import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


RAW_DATA_FILEPATH = '/users/eric/PycharmProjects/testico/api_data.json'
URL_FILEPATH = '/users/eric/PycharmProjects/testico/ico_urls.txt'
TOKEN_FILE = '/users/eric/PycharmProjects/testico/token.csv'
FULLDATA_FILE = '/users/eric/PycharmProjects/testico/fulldata.csv'
NUMERICAL_DATA_FILE = '/users/eric/PycharmProjects/testico/full_num.csv'
TEXT_DATA_FILE = '/users/eric/PycharmProjects/testico/textfeature_dataframe.csv'

with open(URL_FILEPATH, 'r') as f:
    urls = f.readlines()

urls = [url.strip('\n') for url in urls]
results = []
for url in urls:
    html = requests.get(url)
    htmltxt = bs(html.text, 'html.parser')
    htmlbody = htmltxt.body
    heads = htmlbody.find_all("div", class_="col-xs-6 col-md-3")[2:]
    heads = [head.text.strip().split('\n')[0] for head in heads]
    datas = htmlbody.find_all("div", class_="col-xs-6 col-md-9")[2:]
    datas = [data.text.strip().split('\n')[0] for data in datas]
    rr = list(zip(heads, datas))
    results.append(rr)

final_results = []
for result in results:
    dict_result = {key: value for (key, value) in result}
    final_results.append(dict_result)

for idx, url in enumerate(urls):
    name = url.split('/')[-1]
    final_results[idx]['name'] = name
    final_results[idx]['url'] = url

df = pd.DataFrame(final_results)
# df.to_csv('token.csv', index=False)
df.to_csv(TOKEN_FILE, index=False)

scraped_data = pd.read_csv(TOKEN_FILE)
with open(RAW_DATA_FILEPATH, 'r') as f:
    api_data = json.load(f)
api_data = api_data['ico']['finished']
api_df = pd.DataFrame(api_data)

api_df.rename(columns={'all_time_roi': 'ROI', 'coin_symbol': 'Coin Symbol', 'icowatchlist_url': 'url'},
              inplace=True)
cols_to_use = api_df.columns.difference(scraped_data.columns)

fulldata = pd.merge(scraped_data, api_df[cols_to_use], left_index=True, right_index=True, how='outer')
fulldata.to_csv(FULLDATA_FILE)

