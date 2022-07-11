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
from datetime import timedelta

import seaborn as sns
register_matplotlib_converters()
sns.set_style("whitegrid")
plt.rc("figure", figsize=(17, 10),dpi=100)
plt.rc("font", size=14)



# nuovo modello con xgb in cui ho shiftato i rapporti positivi/tamponi di 7 giorni in modo da farli coincidere con ospedalizzati



#
##
### FUNZIONI VARIE
##
#

def timeserieFeatureExtractor(timeseries):

    timeseries['dayofweek'] = timeseries.index.dayofweek
    timeseries['quarter'] = timeseries.index.quarter
    timeseries['month'] = timeseries.index.month
    timeseries['year'] = timeseries.index.year
    timeseries['dayofyear'] = timeseries.index.dayofyear
    timeseries['dayofmonth'] = timeseries.index.day
    timeseries['weekofyear'] = timeseries.index.weekofyear
    timeseries['daysinmonth'] = timeseries.index.daysinmonth
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

# secondo
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
dataframe.tail(10)

df_xgb_michi = pd.DataFrame()
df_xgb_michi['primadose_story'] = dataframe['primadose_story']
df_xgb_michi['secondadose_story'] = dataframe['secondadose_story']
df_xgb_michi['terzadose_story'] = dataframe['terzadose_story']
df_xgb_michi['ospedalizzati_oggi']=dataframe['ospedalizzati_oggi']
df_xgb_michi['perc_oggi_7days'] = dataframe['perc_oggi'].shift(7).fillna(method='bfill')
df_xgb_michi.fillna(0,inplace=True)


# feature eng.
running_average = 4    # <---
df_xgb_michi['perc_oggi_7days'] = df_xgb_michi['perc_oggi_7days'].rolling(window=running_average).mean()
df_xgb_michi.fillna(0,inplace=True)

past_days = 7
for i in range(1, past_days):
    df_xgb_michi[f'perc_oggi_days_{i}'] = df_xgb_michi['perc_oggi_7days'].shift(i).dropna()

for i in range(1, past_days):
    df_xgb_michi[f'ospedalizzati_oggi{i}'] = df_xgb_michi['ospedalizzati_oggi'].shift(i).dropna()
df_xgb_michi.fillna(0,inplace=True)

timeserieFeatureExtractor(df_xgb_michi)


# xgb model
x = df_xgb_michi[df_xgb_michi.index < '2022-06-22'].drop(columns='ospedalizzati_oggi')
y = df_xgb_michi[df_xgb_michi.index < '2022-06-22']['ospedalizzati_oggi']

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


# FETURE IMPORTANCE XGB -> per eliminare variabili inutili 
plt.rc("figure", figsize=(17, 10),dpi=100)
sorted_idx = model.feature_importances_.argsort()
plt.title('Feature importance XGB')
plt.barh(x.columns[sorted_idx], model.feature_importances_[sorted_idx])
plt.show()

# plot prediction
df_prediction = df_xgb_michi.loc[x.index[-1]+timedelta(days=1):]
prediction = model.predict(df_prediction.drop(columns = 'ospedalizzati_oggi'))
prediction = pd.DataFrame(prediction,index=df_prediction.index)               
plt.plot(prediction,'r',label='predict')
plt.plot(df_prediction.ospedalizzati_oggi,label='real')
plt.plot(df_xgb_michi[(df_xgb_michi.index > '2022-04-01') 
                      & (df_xgb_michi.index < '2022-06-22')].ospedalizzati_oggi,'g',label='original ts')
plt.legend()
plt.show()