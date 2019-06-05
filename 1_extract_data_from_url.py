import json
import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def get_webpage_link(html_body):

    html = html_body.find_all("div", class_="col-xs-6 col-md-6")
    if len(html) == 0:
        return None
    html2 = html[1]
    html3 = html2.contents
    website = [ii for ii in html3 if not ii == '\n'][0]
    weblink = website.get('href')
    return weblink


def get_github_link(html_body):

    html2 = html_body.find_all("div", class_="col-xs-6 col-md-9")
    if len(html2) == 0:
        return None
    icon = html2[0]
    icon1 = icon.contents
    link = [item for item in icon1 if not item == '\n']
    linktxt = []
    for xx in link:
        bb = xx.get('href')
        linktxt.append(bb)

    for xx in linktxt:
        if 'github' in xx:
            return xx

    return None


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
    ico_results = list(zip(heads, datas))


    github_link = get_github_link(htmlbody)
    website_link = get_webpage_link(htmlbody)
    ico_results.append(('Github URL', github_link))
    ico_results.append(('Official Website', website_link))
    results.append(ico_results)
     


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
#df.to_csv('token_new.csv', index=False)
df.to_csv(TOKEN_FILE, index=False)
df.count()


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

