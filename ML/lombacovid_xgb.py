import pandas as pd
import numpy as np
from math import *
import json
from datetime import timedelta
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

##import warnings
##warnings.filterwarnings("ignore")



# funzioni varie
# ts feature engineering
def ts_feature(timeseries):
    timeseries['dayofweek'] = timeseries.index.dayofweek
    timeseries['quarter'] = timeseries.index.quarter
    timeseries['month'] = timeseries.index.month
    timeseries['year'] = timeseries.index.year
    timeseries['dayofyear'] = timeseries.index.dayofyear
    timeseries['dayofmonth'] = timeseries.index.day
    timeseries['weekofyear'] = timeseries.index.weekofyear
    timeseries['daysinmonth'] = timeseries.index.daysinmonth
    timeseries['weekend'] = np.where(timeseries['dayofweek'] > 4, 1, 0)
    timeseries.fillna(0,inplace=True)
    return 

# errori 
def calc_error(y_test,y_pred):
    R2 = r2_score(y_test,y_pred)
    MSE = mean_squared_error(y_test,y_pred)
    RMSE = sqrt(MSE)
    MAE = mean_absolute_error(y_test,y_pred)
    MAPE = mean_absolute_percentage_error(y_test,y_pred)
    #maxE = max_error(y_pred,y_test)
    medianAbsEr = median_absolute_error(y_test,y_pred)
    
    print(f'R2: {R2}')
    print('Mean Sqarred Error: {}'.format(MSE))
    print('Root Mean Sqarred Error: {}'.format(RMSE))
    print('Mean Absolute Error: {}'.format(MAE))
    print('Mean Absolute Percentage Error: {}'.format(MAPE))
    #print('MaxError: {}'.format(maxE))
    print('Median Absolute Error: {}'.format(medianAbsEr))
    return


# lettura json
f = open('ML/lombacovid_data.json.json')
data_dict = json.load(f)

max_len = len(data_dict['perc_story'])
min_len = len(data_dict['primadose_story'])
zeros_tofill = list(np.zeros(max_len - min_len))

data_dict['primadose_story'] = zeros_tofill + data_dict['primadose_story']
data_dict['secondadose_story'] = zeros_tofill + data_dict['secondadose_story']
data_dict['terzadose_story'] = zeros_tofill + data_dict['terzadose_story']

data_covid = pd.DataFrame.from_dict(data_dict)

data_covid.drop(columns='data', inplace=True)
data_covid.drop(columns='terapie_story', inplace=True)
data_covid.drop(columns='deceduti_story', inplace=True)

data_covid['date'] = pd.date_range('2020-09-01', periods=max_len, freq='D')
data_covid['date'] = pd.to_datetime(data_covid['date'])
data_covid.set_index('date',inplace=True)

print(data_covid.head(14))

data_covid['ospedalizzati_story'] = data_covid['ospedalizzati_story'].shift(-7).dropna()

print(data_covid.head(14))

# predizioni prossimi giorni
# df_future_prediction = pd.DataFrame()
# df_future_prediction['rapporto_positivi_tamponi'] = data_covid.rapporto_positivi_tamponi.tail(len(data_covid)-len(new_df))
# df_future_prediction['prima_dose'] = data_covid.prima_dose.tail(len(data_covid)-len(new_df))
# df_future_prediction['seconda_dose'] = data_covid.seconda_dose.tail(len(data_covid)-len(new_df))
# df_future_prediction['terza_dose'] = data_covid.terza_dose.tail(len(data_covid)-len(new_df))

# feature engineering timestamp index: uso la funzione creata
ts_feature(data_covid)
# ts_feature(df_future_prediction)

print(data_covid.head(14))

# predizione prossimi 7 giorni
x = data_covid.drop(columns='ospedalizzati_story')
y = data_covid['ospedalizzati_story']

# creazione modello su tutto dataset (x & y)
xgb_reg_final = XGBRegressor(
        n_estimators=200, 
        max_depth=6, 
        learning_rate=0.1,
        random_state = 42,
        n_jobs = 3).fit(x,y)

# predizione di 7 giorni
y_next_days = xgb_reg_final.predict(df_future_prediction)
df_next_days = pd.DataFrame(y_next_days).set_index(df_future_prediction.index+timedelta(days=7))

# grafico predizioni della validation e validation
plt.plot(df_next_days,'r',markersize=9,label = 'predicted next 7 days')
plt.show()
plt.plot(data_covid.ospedalizzati,label='ospedalizzati ts')
plt.plot(df_next_days,'r',markersize=9,label = 'predicted next 7 days')
plt.legend()
plt.title('Ospedalizzati next 7 days')
plt.show()
