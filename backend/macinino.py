"""Prende da GitHub i dati di ieri e di oggi per calcolare ed esportare un po' di situazioni."""

import pandas as pd
import numpy as np
import datetime
import json
import ftplib

print()

#
##
### PREPARO GLI INPUT
##
#

oggi_dash = datetime.date.today().strftime('%Y-%m-%d')
oggi_slash = datetime.date.today().strftime('%d/%m/%Y')
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

# Carico l'ultimo dataset disponibile
present = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv')
lombardia_present = present[ present['denominazione_regione'] == 'Lombardia' ]

# Verifico che l'ultimo dataset disponibile sia quello di oggi
ultimo_aggiornamento = lombardia_present['data'].values[0][:10]
if oggi_dash != ultimo_aggiornamento:
	exit("File smarmellati. Ciao!")
# e che il sito non sia già stato aggiornato
story_csv = pd.read_csv('https://www.lombacovid.it/story.csv')		# <---
if oggi_slash == story_csv['data'].values[-1]:
	exit("Sito già aggiornato!")

print("Elaboro...")

# Carico i restanti dataset: past e vaccini
yesterday_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-'+yesterday+'.csv'
past = pd.read_csv(yesterday_url)
lombardia_past = past[ past['denominazione_regione'] == 'Lombardia' ]

vaccini = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')
lombardia_vaccini = vaccini[ vaccini['area'] == 'LOM' ]

#
##
### ELABORO
##
#

#tamponi
tot_tamponi_present = lombardia_present['tamponi'].values[0]
tot_tamponi_past = lombardia_past['tamponi'].values[0]
tamponi_oggi = tot_tamponi_present - tot_tamponi_past

#nuovi positivi
nuovi_positivi = lombardia_present['nuovi_positivi'].values[0]

#rapporto
percentuale = np.around(nuovi_positivi / tamponi_oggi * 100, 2)					#<---

#in ospedale adesso
ospedalizzati_attuali = lombardia_present['totale_ospedalizzati'].values[0]		#<---

#in T.I. adesso
terapie_attuali = lombardia_present['terapia_intensiva'].values[0]				#<---

#deceduti oggi
tot_deceduti_present = lombardia_present['deceduti'].values[0]
tot_deceduti_past = lombardia_past['deceduti'].values[0]
deceduti_oggi = tot_deceduti_present - tot_deceduti_past						#<---

#vaccinati
lombardia_vaccini_janssen = lombardia_vaccini[ lombardia_vaccini['forn'] == 'Janssen' ]
lombardia_vaccini_janssen_tot = lombardia_vaccini_janssen['d1'].sum()
#
primadose_tot = lombardia_vaccini['d1'].sum() - lombardia_vaccini_janssen_tot					#<---
secondadose_tot = lombardia_vaccini['d2'].sum() + lombardia_vaccini_janssen_tot					#<---
terzadose_tot = lombardia_vaccini['db1'].sum()													#<---
quartadose_tot = lombardia_vaccini['db2'].sum()													#<---

#
##
### ESPORTO
##
#

nuova_riga = pd.DataFrame([[str(oggi_slash),
							float(percentuale),
							float(ospedalizzati_attuali),
							float(terapie_attuali),
							float(deceduti_oggi),
							float(primadose_tot),
							float(secondadose_tot),
							float(terzadose_tot),
							float(quartadose_tot)]],

							columns=story_csv.columns.tolist())

story_csv = pd.concat([story_csv, nuova_riga])
story_csv.set_index('data', inplace=True)
story_csv.to_csv('frontend/story.csv')

with open('credentials.json', 'r') as credentials_file:
	credentials_dict = json.load(credentials_file)
session = ftplib.FTP('ftp.lombacovid.it', credentials_dict['id'], credentials_dict['password'])
with open('frontend/story.csv', 'rb') as story_file:
    session.storbinary('STOR www.lombacovid.it/story.csv', story_file)

session.quit()

#
##
### CHIUDO
##
#

print()
print("Fatto. Dati aggiornati al " + str(oggi_slash) + ".")