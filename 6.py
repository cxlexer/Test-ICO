
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

tdd = pd.read_csv(TEXT_DATA_FILE)
train, test = train_test_split(tdd, test_size=0.33)
array_train = train.values
array_test = test.values
x_train = array_train[:, 0:-1]
y_train = array_train[:, -1]
x_test = array_test[:, 0:-1]
y_test = array_test[:, -1]
model = XGBClassifier()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(accuracy)

fullvalue = tdd.values
traindata = fullvalue[:, 0:-1]
testdata = fullvalue[:, -1]
xgbc = model.fit(x_train, y_train)
scores = cross_val_score(xgbc, traindata, testdata, cv=10)
print(scores)
print(np.mean(scores))