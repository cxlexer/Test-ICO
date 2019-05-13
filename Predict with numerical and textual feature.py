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
full_num = pd.read_csv(NUMERICAL_DATA_FILE)
model = XGBClassifier()

full_num = full_num.drop('binary_ROI', axis=1)
fulldata = pd.concat([full_num, tdd], axis=1)
fulldata.to_csv('completedata_text_num.csv')
train2, test2 = train_test_split(fulldata, test_size=0.33)
array_train2 = train2.values
array_test2 = test2.values
x_train2 = array_train2[:, 0:-1]
y_train2 = array_train2[:, -1]
x_test2 = array_test2[:, 0:-1]
y_test2 = array_test2[:, -1]
model.fit(x_train2, y_train2)
y_pred2 = model.predict(x_test2)
accuracy2 = accuracy_score(y_test2, y_pred2)
print(accuracy2)

fullvalue = fulldata.values
traindata = fullvalue[:, 0:-1]
testdata = fullvalue[:, -1]
xgbc = model.fit(x_train2, y_train2)
scores = cross_val_score(xgbc, traindata, testdata, cv=10)
print(scores)
print(np.mean(scores))
