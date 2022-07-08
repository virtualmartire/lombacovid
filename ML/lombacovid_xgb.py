import pandas as pd
import numpy as np
from math import *
import json
from datetime import timedelta
import matplotlib.pyplot as plt


from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import median_absolute_error, mean_absolute_percentage_error

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
    timeseries['Hours'] = timeseries.index.hour
    timeseries['minute'] = timeseries.index.minute
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
    timeseries = timeseries.loc[:, (timeseries != 0).any(axis=0)]
    timeseries.head()
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
data = json.load(f)

# creazione dizionario per creazione dataset covid
keys = []

for key in data:
    keys.append(key)


dataz = {}
for i in range(1,len(keys)):
    dataz[keys[i]] = data[keys[i]]

# for i in range(1,len(keys)):
#     print(keys[i],len(data[keys[i]]))


# creazione database covid a 550 elementi (parte da 01/01/21) 
# -> tolgo i giorni con prima/seconda/terza dose pari a zero
data_covid = pd.DataFrame()
data_covid['rapporto_positivi_tamponi'] = pd.DataFrame(dataz['perc_story'])
data_covid['ospedalizzati'] = pd.DataFrame(dataz['ospedalizzati_story'])
# data_covid['terapie'] = pd.DataFrame(dataz['terapie_story']) # -> non uso terapie

# numero di giorni da togliere per prima/seconda/terza dose pari a 0
zero = len(data_covid['rapporto_positivi_tamponi']) - len(dataz['terzadose_story'])
n = zero 

# creazione dataset "data_covid"
data_covid.drop(index=data_covid.index[:n],inplace=True)
data_covid['prima_dose']= data['primadose_story']
data_covid['seconda_dose']= data['secondadose_story']
data_covid['terza_dose']= data['terzadose_story']
data_covid['date'] = pd.date_range('2021-01-01', periods=550, freq='D')
data_covid['date'] = pd.to_datetime(data_covid['date'])
data_covid.set_index('date',inplace=True)

print('dataset usato:')
print(data_covid.head())


# xgboost time series forecasting with prima,seconda,terza dose
# -> database con lag per ospedalizzati: shift(7) ospedalizzati e tolgo ultimi 7 giorni dagli altri
new_df = pd.DataFrame()
new_df['ospedalizzati'] = data_covid['ospedalizzati'].shift(-7).dropna()
new_df['rapporto_positivi_tamponi'] = data_covid.rapporto_positivi_tamponi.head(len(new_df))
new_df['prima_dose'] = data_covid.prima_dose.head(len(new_df))
new_df['seconda_dose'] = data_covid.seconda_dose.head(len(new_df))
new_df['terza_dose'] = data_covid.terza_dose.head(len(new_df))
new_df.dropna(inplace=True)

# predizioni prossimi giorni
df_future_prediction = pd.DataFrame()
df_future_prediction['rapporto_positivi_tamponi'] = data_covid.rapporto_positivi_tamponi.tail(len(data_covid)-len(new_df))
df_future_prediction['prima_dose'] = data_covid.prima_dose.tail(len(data_covid)-len(new_df))
df_future_prediction['seconda_dose'] = data_covid.seconda_dose.tail(len(data_covid)-len(new_df))
df_future_prediction['terza_dose'] = data_covid.terza_dose.tail(len(data_covid)-len(new_df))

# feature engineering timestamp index: uso la funzione creata
ts_feature(new_df)
ts_feature(df_future_prediction)

# eliminazione colonne vuote
new_df = new_df.loc[:, (new_df != 0).any(axis=0)]
df_future_prediction = df_future_prediction.loc[:, (df_future_prediction != 0).any(axis=0)]

# predizione prossimi 7 giorni
x = new_df.drop(columns='ospedalizzati')
y = new_df['ospedalizzati']

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
