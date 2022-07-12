import pandas as pd
import numpy as np
from math import *
import json
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import median_absolute_error, mean_absolute_percentage_error
from xgboost import XGBRegressor

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
dataframe = dataframe.fillna(0)

past_days = 7           # <---
for i in range(1, past_days):
    dataframe[f'ospedalizzati_past{i}'] = dataframe['ospedalizzati_oggi'].shift(i)
for i in range(1, past_days):
    dataframe[f'perc_past{i}'] = dataframe['perc_oggi'].shift(i).dropna()

dataframe = dataframe.fillna(0)

future_target = 7       # <---
dataframe['ospedalizzati_target'] = dataframe['ospedalizzati_oggi'].shift(-future_target)
dataframe = dataframe.fillna(0)

timeserieFeatureExtractor(dataframe)


# ho tolto prima,seconda e terza dose
dataframe.drop(columns=['primadose_story','secondadose_story','terzadose_story'],inplace=True)

# no train/test, ma solo modello su tutto il dataframe
x = dataframe.head(-future_target).drop(columns='ospedalizzati_target')
y = dataframe.head(-future_target)['ospedalizzati_target']

model = XGBRegressor(
        n_estimators=200, 
        random_state = 42,
        n_jobs = 3,
        colsample_bytree=0.5,
        subsample=0.5,
        max_depth=3,
        gamma=1e5,
        eta=1e-1,
        min_child_weight=1.0).fit(x,y)

#
##
### TESTING
##
#

y_pred = model.predict(x)

# calcolo degli errori

print("\nError on test data:")
calcError(y, y_pred)

# feature importance

sorted_idx = model.feature_importances_.argsort()
plt.title('Feature importance XGB')
plt.barh(x.columns[sorted_idx], model.feature_importances_[sorted_idx])
plt.show()


# predizione di 7 giorni -> dovrebbero aumentare progressivamente; i valori più lontani sono meno precisi
prediction = model.predict(dataframe.tail(future_target).drop(columns='ospedalizzati_target'))
print('\nprevisione :',prediction)
plt.plot(prediction)    
plt.title('predizione future')
plt.show()



# prvisioni per dati input futuri

# nuovi dati giornalieri (prova)
new_osp = 1335
new_perc = 23.61
# new_primadose = 8129000
# new_secondadose = 8259919.0
# new_terzadose = 7220402.0

new_data = {'perc_oggi':new_perc,'ospedalizzati_oggi':new_osp
#             ,'primadose_story':new_primadose,
#             'secondadose_story':new_secondadose,
#             'terzadose_story':new_terzadose
            }

new_dataframe = dataframe[dataframe.columns[0:5]]
new_dataframe = new_dataframe.append(new_data,ignore_index=True)
new_dataframe['date'] = pd.date_range(dataframe.index[0],periods=len(new_dataframe))
new_dataframe.set_index('date',inplace=True)

# feature engineering
running_average = 4     # <---
new_dataframe['perc_oggi'] = new_dataframe['perc_oggi'].rolling(window=running_average).mean()
new_dataframe = new_dataframe.fillna(0)

past_days = 7           # <---
for i in range(1, past_days):
    new_dataframe[f'ospedalizzati_past{i}'] = new_dataframe['ospedalizzati_oggi'].shift(i)
for i in range(1, past_days):
    new_dataframe[f'perc_past{i}'] = new_dataframe['perc_oggi'].shift(i)
new_dataframe = new_dataframe.fillna(0)

future_target = 7       # <---
new_dataframe['ospedalizzati_target'] = new_dataframe['ospedalizzati_oggi'].shift(-future_target)
new_dataframe = new_dataframe.fillna(0)

timeserieFeatureExtractor(new_dataframe)


# previsione futura
future_prediction = model.predict(new_dataframe.tail(future_target).drop(columns='ospedalizzati_target'))
print('predizione future:',future_prediction)
plt.plot(future_prediction)
plt.title('predizione future')
plt.show()