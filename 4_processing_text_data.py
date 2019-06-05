import pprint
import json
import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.snowball import SnowballStemmer
import nltk
np.random.seed(1)
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

RAW_DATA_FILEPATH = '/users/eric/PycharmProjects/testico/api_data.json'
URL_FILEPATH = '/users/eric/PycharmProjects/testico/ico_urls.txt'
TOKEN_FILE = '/users/eric/PycharmProjects/testico/token.csv'
FULLDATA_FILE = '/users/eric/PycharmProjects/testico/fulldata.csv'
NUMERICAL_DATA_FILE = '/users/eric/PycharmProjects/testico/full_num.csv'
TEXT_DATA_FILE = '/users/eric/PycharmProjects/testico/textfeature_dataframe.csv'

data = pd.read_csv(FULLDATA_FILE)
data.dropna(subset=['ROI'], inplace=True)
data = data.drop('Unnamed: 0', axis=1)

data['description2'] = data['description'].str.replace(" ", ",")

stemmer = SnowballStemmer("english")
data['stemmed'] = data.description.map(lambda x: ' '.join([stemmer.stem(y) for y in x.split(' ')]))
vct = TfidfVectorizer(stop_words='english')
vct.fit(data.stemmed)
transformed = vct.fit_transform(data['stemmed'])
td = transformed.todense()
tdd = pd.DataFrame(td)
full_num = pd.read_csv(NUMERICAL_DATA_FILE)
tdd['ROI'] = full_num['binary_ROI']
tdd.to_csv(TEXT_DATA_FILE)