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

full_num = pd.read_csv(NUMERICAL_DATA_FILE, index_col=0)

# Ignore last label: ROI
feature_names = full_num.columns.tolist()[:-1]
#import ipdb; ipdb.set_trace()
y = full_num['binary_ROI']
X = full_num[feature_names]
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)
my_model = RandomForestClassifier(random_state=0).fit(train_X, train_y)

perm = PermutationImportance(my_model, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm, feature_names=val_X.columns.tolist())


y_pred = my_model.predict(val_X)
accuracy = accuracy_score(val_y, y_pred)
print(accuracy)



train, test = train_test_split(full_num, test_size=0.33)
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

logmodel = LogisticRegression()
logmodel.fit(train_X,train_y )


# cross-validation with 10folds
scores2 = cross_val_score(my_model, X, y, cv=10)
print(np.mean(scores2))

fullvalue = full_num .values
traindata = fullvalue[:, 0:-1]
testdata = fullvalue[:, -1]
xgbc = model.fit(x_train, y_train)
scores = cross_val_score(xgbc, traindata, testdata, cv=10)
print(np.mean(scores))

scores3 = cross_val_score(logmodel, X, y, cv=10)
print(np.mean(scores3))