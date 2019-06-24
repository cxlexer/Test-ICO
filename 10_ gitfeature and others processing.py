import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

np.random.seed(1)

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import eli5
from eli5.sklearn import PermutationImportance
from sklearn.linear_model import LogisticRegression

RAW_DATA_FILEPATH = '/users/eric/PycharmProjects/testico/api_data.json'
URL_FILEPATH = '/users/eric/PycharmProjects/testico/ico_urls.txt'
TOKEN_FILE = '/users/eric/PycharmProjects/testico/token.csv'
FULLDATA_FILE = '/users/eric/PycharmProjects/testico/fulldata.csv'
NUMERICAL_DATA_FILE = '/users/eric/PycharmProjects/testico/full_num.csv'
TEXT_DATA_FILE = '/users/eric/PycharmProjects/testico/textfeature_dataframe.csv'
TOKEN_GIT_FEATURE_FILE = '/users/eric/PycharmProjects/testico/token_with_github_feature.csv'
FULLDATA_PLUS_GIT = '/users/eric/PycharmProjects/testico/fulldata_plus_git.csv'

full = pd.read_csv(FULLDATA_PLUS_GIT)
full.dropna(subset=['ROI'], inplace=True)

full_num = full.drop(['Coin Symbol', 'Accepted Currencies', 'Have Prototype?', 'Pre-ICO Dates',
                      'name', 'url', 'image', 'timezone', 'description', 'website_link',
                      'Funding Goal', 'Total Tokens', 'Price Now', 'Funds in Escrow?',
                      'Restricted Countries', 'Total Raised'],
                     axis=1)
full_num['Initial Token Price'] = full_num['Initial Token Price'].replace(['\$'], '', regex=True)
full_num['Initial Token Price'] = full_num['Initial Token Price'].str.strip()
full_num['Initial Token Price'] = pd.to_numeric(full_num['Initial Token Price'].str.replace(',', ''), errors='coerce')
full_num['price_usd'] = pd.to_numeric(full_num['price_usd'].str.replace(',', ''), errors='coerce')
#

full_num['ROI'] = full_num['ROI'].str.replace(',', '')
full_num['ROI'] = full_num['ROI'].str.rstrip('%').astype('float')/100
#
full_num['end_time'] = pd.to_datetime(full_num['end_time'])
full_num['start_time'] = pd.to_datetime(full_num['start_time'])
full_num['Total days'] = (full_num['end_time'] - full_num['start_time']).dt.days
full_num = full_num.drop(['end_time', 'start_time'], axis=1)
full_num = full_num[['ROI', 'Country', 'Initial Token Price', 'Platform',
                     'price_usd', 'Total days','Github URL','watchers','stars','forks','branches', 'commits']]

full_num = pd.get_dummies(full_num, columns=['Country', 'Platform'], drop_first=True)


#full_num.to_csv(NUMERICAL_DATA_PLUS_GIT_FILE)
#
#
# # minmax = preprocessing.MinMaxScaler()
# # full_scaled = minmax.fit_transform(full_num)
# # scaleddata = pd.DataFrame(full_scaled)
#
def binarize_roi(roi):
    if roi > 0:
        return 1
    else:
        return 0


def binarized_github(git):
    if pd.isna(git):
        return 0
    else:
        return 1

full_num['binarize_Git'] = full_num['Github URL'].apply(binarized_github)
full_num['binary_ROI'] = full_num['ROI'].apply(binarize_roi)


full_num = full_num.drop('Github URL', axis=1)
full_num = full_num.drop('ROI', axis=1)
full_num.to_csv('num_plus_git.csv', index=False)


