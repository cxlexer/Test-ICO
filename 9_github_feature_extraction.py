import json
import numpy as np
import requests, ConnectionError,
import pandas as pd
from bs4 import BeautifulSoup as bs
from operator import itemgetter
import time

RAW_DATA_FILEPATH = '/users/eric/PycharmProjects/testico/api_data.json'
URL_FILEPATH = '/users/eric/PycharmProjects/testico/ico_urls.txt'
TOKEN_FILE = '/users/eric/PycharmProjects/testico/token.csv'
FULLDATA_FILE = '/users/eric/PycharmProjects/testico/fulldata.csv'
NUMERICAL_DATA_FILE = '/users/eric/PycharmProjects/testico/full_num.csv'
TEXT_DATA_FILE = '/users/eric/PycharmProjects/testico/textfeature_dataframe.csv'
URL_COPY_FILEPATH = '/users/eric/PycharmProjects/testico/ico_urls copy.txt'


def repolink_extract(url):
    try:
        html = requests.get(url)
    except Exception as e:
        print(e)
        print(url)
        return None
    htmltxt = bs(html.text, 'html.parser')

    repohtml = htmltxt.find_all('a', class_="d-inline-block",
                                itemprop="name codeRepository")

    partial_repolink_list = []
    for item in repohtml:
        link = item.attrs['href']
        partial_repolink_list.append(link)
    return partial_repolink_list


def nextpage_extract(url):
    try:
        html = requests.get(url)
    except Exception as e:
        print(e)
        print(url)
        return None
    htmltxt = bs(html.text, 'html.parser')

    nextpage = htmltxt.find_all('a',
                                class_="next_page",
                                rel="next")
    if len(nextpage) != 0:
        a = 'https://github.com'
        next_ = nextpage[0].attrs['href']
        nextlink = '{}{}'.format(a, next_)
        return nextlink
    else:
        return None


def repolink_extract_paginator(current_url):
    output = repolink_extract(current_url)
    next_url = nextpage_extract(current_url)
    while next_url is not None:
        current_url = next_url
        output_temp = repolink_extract(current_url)
        output.append(output_temp)
        next_url = nextpage_extract(current_url)
        time.sleep(1)
    repolink_list = []

    def reemoveNestings(l):
        for i in l:
            if type(i) == list:
                reemoveNestings(i)
            else:
                repolink_list.append(i)

    reemoveNestings(output)

    return repolink_list


def gitfeature_extract(partial_repolink):
    a = 'https://github.com'
    full_repolink = '{}{}'.format(a, partial_repolink)
    try:
        githtml = requests.get(full_repolink)
    except Exception as e:
        print(e)
        print(partial_repolink)
        gitfeature = {
            'watchers': 0,
            'stars': 0,
            'forks': 0,
            'commits': 0,
            'branches': 0}
        return gitfeature
    githtmltxt = bs(githtml.text, 'html.parser')
    otherfeature_html = githtmltxt.find_all(
        'span', class_="num text-emphasized")
    if len(otherfeature_html) == 0:
        gitfeature = {
            'watchers': 0,
            'stars': 0,
            'forks': 0,
            'commits': 0,
            'branches': 0}
        return gitfeature
    else:
        watch_html = githtmltxt.find_all(
            'a',
            class_="social-count",
            href='{}{}'.format(partial_repolink, '/watchers')
        )
        watch = watch_html[0].text.strip().replace(',', '')
        stars_html = githtmltxt.find_all(
            'a',
            class_="social-count",
            href='{}{}'.format(partial_repolink, '/stargazers')
        )
        stars = stars_html[0].text.strip().replace(',', '')
        forks_html = githtmltxt.find_all(
            'a',
            href='{}{}'.format(partial_repolink, '/network/members'),
            class_="social-count"
        )

        forks = forks_html[0].text.strip().replace(',', '')

        otherfeature_html = githtmltxt.find_all(
            'span', class_="num text-emphasized")
        commits = otherfeature_html[0].text.strip().replace(',', '')
        branches = otherfeature_html[1].text.strip().replace(',', '')
        releases = otherfeature_html[2].text.strip().replace(',', '')
        gitfeature = {
            'watchers': watch,
            'stars': stars,
            'forks': forks,
            'commits': commits,
            'branches': branches}
        return gitfeature


def repofeature_extract_paginator(current_url):
    output = repolink_extract(current_url)
    next_url = nextpage_extract(current_url)
    while next_url is not None:
        current_url = next_url
        output_temp = repolink_extract(current_url)
        output.append(output_temp)
        next_url = nextpage_extract(current_url)
        time.sleep(1)
    repolink_list = []

    def reemoveNestings(l):
        for i in l:
            if type(i) == list:
                reemoveNestings(i)
            else:
                repolink_list.append(i)

    reemoveNestings(output)
    d_list = []
    feature_sum = {}
    for partial_repolink in repolink_list:
        feature_dic = gitfeature_extract(partial_repolink)
        d_list.append(feature_dic)
    for d in d_list:
        for k in d.keys():
            feature_sum[k] = feature_sum.get(k, 0) + int((d[k]))
    return feature_sum


def gitfeature_html(github_account_html):
    if github_account_html is None:
        gitfeature = {
            'watchers': 0,
            'stars': 0,
            'forks': 0,
            'commits': 0,
            'branches': 0}
        return gitfeature
    else:
        try:
            html = requests.get(github_account_html)
        except Exception as e:
            print(e)
            print(url)
            gitfeature = {
                'watchers': 0,
                'stars': 0,
                'forks': 0,
                'commits': 0,
                'branches': 0}
            return gitfeature
        htmltxt = bs(html.text, 'html.parser')
        repohtml = htmltxt.find_all('a', class_="d-inline-block",
                                    itemprop="name codeRepository")
        if len(repohtml) == 0:
            output = gitfeature_extract(github_account_html.replace('https://github.com', ''))
            return output


        else:
            output = repofeature_extract_paginator(github_account_html)
            return output


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

    git_feature = gitfeature_html(github_link)
    git_feature_list = []
    for key, value in git_feature.items():
        temp = (key, value)
        git_feature_list.append(temp)

    joinedlist = ico_results + git_feature_list
    results.append(joinedlist)

final_results = []
for result in results:
    dict_result = {key: value for (key, value) in result}
    final_results.append(dict_result)

for idx, url in enumerate(urls):
    name = url.split('/')[-1]
    final_results[idx]['name'] = name
    final_results[idx]['url'] = url

df = pd.DataFrame(final_results)
df.to_csv('token_with_github_feature.csv')