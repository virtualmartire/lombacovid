from turtle import color
import pandas as pd
import numpy as np
from math import *
import json
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import median_absolute_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
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

def plot_test(y_test, y_pred, perc_error):
    
    y_pred_1 = y_pred.head(1)
    y_pred_2 = y_pred.tail(1)

    y_pred_a = y_pred_2 * (1+perc_error)
    y_pred_b = y_pred_2 * (1-perc_error)
    y_pred_up = pd.concat([y_pred_1, y_pred_a])
    y_pred_down = pd.concat([y_pred_1, y_pred_b])

    plt.plot(y_test, label = "ground truth", color="green")
    plt.fill_between(y_pred_up.index, y_pred_up.to_numpy()[:,0], y_pred_down.to_numpy()[:,0], color="orange", alpha=0.3)
    plt.legend()
    plt.show()

    return

#
##
### DATASET
##
#

# recupero del dataset remoto e aggiornato

dataframe = pd.read_csv('https://www.lombacovid.it/story.csv')

dataframe.drop(columns='terapie_story', inplace=True)
dataframe.drop(columns='deceduti_story', inplace=True)

dataframe.rename(columns = {'ospedalizzati_story':'ospedalizzati_oggi',
                            'perc_story':'perc_oggi'},
                            inplace = True)

# replace date
dataframe['new_date'] = pd.date_range(start='2020-09-01', periods=len(dataframe))
dataframe['new_date'] = pd.to_datetime(dataframe['new_date'])
dataframe.drop(columns='data', inplace=True)
dataframe.set_index('new_date',inplace=True)

# feature engineering

running_average = 4     # <---
dataframe['perc_oggi'] = dataframe['perc_oggi'].rolling(window=running_average).mean()
dataframe = dataframe.dropna()

past_days = 7           # <---
for i in range(1, past_days):
    dataframe[f'ospedalizzati_past{i}'] = dataframe['ospedalizzati_oggi'].shift(i).dropna()
    dataframe[f'perc_past{i}'] = dataframe['perc_oggi'].shift(i).dropna()
dataframe = dataframe.dropna()

future_target = 7       # <---
dataframe['ospedalizzati_target'] = dataframe['ospedalizzati_oggi'].shift(-future_target).dropna()
dataframe = dataframe.dropna()

timeserieFeatureExtractor(dataframe)

dataframe.drop(columns=['primadose_story','secondadose_story','terzadose_story'], inplace=True)

#
##
### TRAIN
##
#

x = dataframe.drop(columns='ospedalizzati_target')
y = dataframe['ospedalizzati_target']

split_val, split_test = 5, 15

x_train, y_train = x[:-(split_val+split_test)], y[:-(split_val+split_test)]
x_val, y_val = x[-(split_val+split_test):-split_test], y[-(split_val+split_test):-split_test]
x_test, y_test = x[-split_test:], y[-split_test:]

# model = XGBRegressor(
#         n_estimators=100, 
#         random_state = 42,
#         n_jobs = 3,
#         colsample_bytree=0.4,
#         subsample=0.5,
#         max_depth=7,
#         gamma=1e5,
#         eta=1e-1,
#         min_child_weight=1.0).fit(x_train, y_train)


model = XGBRegressor(
            n_estimators=356, 
            eta=0.1,
            n_jobs = -1,
            colsample_bytree=1,
            min_child_weight=1.0,
            subsample=0.5,
            max_depth=4,
            gamma=0.45,
            reg_alpha = 0.1,
            reg_lambda = 2.5,
            random_state = 42).fit(x_train, y_train)

#
##
### VALIDATE
##
#

perc_error = 0.07        # <---

y_pred = pd.DataFrame(model.predict(x_val), index=y_val.index)

# calcolo degli errori

print("\nError on validation data:")
calcError(y_val, y_pred)

print("\nError on train data:")
calcError(y_train, model.predict(x_train))

# test grafico

plot_test(y_val, y_pred, perc_error)

# feature importance

sorted_idx = model.feature_importances_.argsort()
plt.title('Feature importance XGB')
plt.barh(x.columns[sorted_idx], model.feature_importances_[sorted_idx])
plt.show()

#
##
### TEST
##
#

y_pred = pd.DataFrame(model.predict(x_test), index=y_test.index)

# calcolo degli errori

print("\nError on test data:")
calcError(y_test, y_pred)

# test grafico

plot_test(y_test, y_pred, perc_error)