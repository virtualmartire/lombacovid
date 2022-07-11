import pandas as pd
import numpy as np
from math import *
import json
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import median_absolute_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from pandas.plotting import register_matplotlib_converters

import seaborn as sns
register_matplotlib_converters()
sns.set_style("whitegrid")
plt.rc("figure", figsize=(17, 10),dpi=100)
plt.rc("font", size=14)

#
##
### FUNZIONI VARIE
##
#

def timeserieFeatureExtractor(timeseries):

    #timeseries['dayofweek'] = timeseries.index.dayofweek
    #timeseries['quarter'] = timeseries.index.quarter
    timeseries['month'] = timeseries.index.month
    timeseries['year'] = timeseries.index.year
    #timeseries['dayofyear'] = timeseries.index.dayofyear
    #timeseries['dayofmonth'] = timeseries.index.day
    #timeseries['weekofyear'] = timeseries.index.weekofyear
    #timeseries['daysinmonth'] = timeseries.index.daysinmonth
    timeseries['weekend'] = np.where(timeseries.index.dayofweek > 4, 1, 0)
    timeseries.fillna(0,inplace=True)

    return 

def calcError(y_test, y_pred):
    
    R2 = r2_score(y_test, y_pred)
    MSE = mean_squared_error(y_test, y_pred)
    RMSE = sqrt(MSE)
    MAE = mean_absolute_error(y_test, y_pred)
    MAPE = mean_absolute_percentage_error(y_test, y_pred)
    medianAbsEr = median_absolute_error(y_test, y_pred)
    
    print(f'R2: {R2}')
    print(f'Mean Squared Error: {MSE}')
    print(f'Root Mean Sqarred Error: {RMSE}')
    print(f'Mean Absolute Error: {MAE}')
    print(f'Mean Absolute Percentage Error: {MAPE}')
    #print(f'Median Absolute Error: {medianAbsEr}')

    return

#
##
### DATASET
##
#

# lettura json

f = open('ML/lombacovid_data.json.json')
data_dict = json.load(f)

# riempimento colonne

max_len = len(data_dict['perc_story'])
min_len = len(data_dict['primadose_story'])
zeros_tofill = list(np.zeros(max_len - min_len))

data_dict['primadose_story'] = zeros_tofill + data_dict['primadose_story']
data_dict['secondadose_story'] = zeros_tofill + data_dict['secondadose_story']
data_dict['terzadose_story'] = zeros_tofill + data_dict['terzadose_story']

# creazione dataframe

dataframe = pd.DataFrame.from_dict(data_dict)

dataframe.drop(columns='data', inplace=True)
dataframe.drop(columns='terapie_story', inplace=True)
dataframe.drop(columns='deceduti_story', inplace=True)

dataframe.rename(columns = {'ospedalizzati_story':'ospedalizzati_oggi',
                            'perc_story':'perc_oggi'},
                            inplace = True)

dataframe['date'] = pd.date_range('2020-09-01', periods=max_len, freq='D')
dataframe['date'] = pd.to_datetime(dataframe['date'])
dataframe.set_index('date',inplace=True)

# feature engineering

running_average = 4     # <---

dataframe['perc_oggi'] = dataframe['perc_oggi'].rolling(window=running_average).mean()
dataframe.dropna()

past_days = 7           # <---
future_target = 4       # <---

for i in range(1, past_days):
    dataframe[f'ospedalizzati_past{i}'] = dataframe['ospedalizzati_oggi'].shift(i).dropna()
    dataframe[f'perc_past{i}'] = dataframe['perc_oggi'].shift(i).dropna()

dataframe['ospedalizzati_target'] = dataframe['ospedalizzati_oggi'].shift(-future_target).dropna()

timeserieFeatureExtractor(dataframe)

#
##
### FITTING
##
#

x = dataframe.drop(columns='ospedalizzati_target')
y = dataframe['ospedalizzati_target']

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.85, test_size=0.15, random_state=10)

model = XGBRegressor(
        n_estimators=200, 
        max_depth=6, 
        learning_rate=0.1,
        random_state = 42,
        n_jobs = 3).fit(x_train, y_train)

#
##
### TESTING
##
#

y_pred = model.predict(x_test)

# calcolo degli errori

print("Error on test data:")
calcError(y_test, y_pred)


### PLOT TRAIN VS TEST

plt.plot(y_pred,'b+',label='prediction')
plt.plot(y_test.reset_index(drop=True),'yo',label='test')
plt.legend()
plt.title('Train vs Test')
plt.show()


# test grafico

test_interval = dataframe.tail(30)

fixed_interval = test_interval.head(16)['ospedalizzati_oggi']
true_final = test_interval.tail(14)['ospedalizzati_oggi']
pred_final = model.predict(test_interval.head(16).drop(columns='ospedalizzati_target').tail(14))

pred_final = pd.DataFrame(pred_final, index=true_final.index)

plt.plot(fixed_interval)
plt.plot(true_final, label='ground truth')
plt.plot(pred_final, label = 'prediction')
plt.legend()
plt.show()

# # plot y_test
# plt.rc("figure", figsize=(16, 10),dpi=100)
# plt.plot(y_test.reset_index()['ospedalizzati_target'], 'yo', label='test')
# plt.plot()
# plt.plot(y_pred, 'r+', markersize=12, label='pred')
# plt.legend()
# plt.title('Test set')
# plt.show()

# mean_train = np.mean(y_train)   # calcolo media train 
# baseline_predictions = np.ones(y_test.shape) * mean_train  # creo vettore lungo y_test con elementi = media train
# mse_baseline = sqrt(mean_squared_error(y_test,baseline_predictions)) # calcolo errore su vettore media e y_test
# print("\nBaseline median RMSE is {:.2f}".format(mse_baseline))