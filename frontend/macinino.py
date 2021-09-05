"""Prende i dati di ieri (past.csv), di oggi (present.csv) e dei vaccini (GitHub raw) per calcolare ed esportare
un po' di situazioni."""

import pandas as pd
import numpy as np
import datetime
import os
import json

print()

#
##
### PREPARO GLI INPUT
##
#

# Carico l'ultimo dataset disponibile
present = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv')
lombardia_present = present[ present['denominazione_regione'] == 'Lombardia' ]

# Verifico che l'ultimo dataset disponibile sia quello di oggi
oggi = datetime.date.today().strftime("%Y-%m-%d")
ultimo_aggiornamento = lombardia_present['data'].values[0][:10]
if oggi != ultimo_aggiornamento:
	exit("File smarmellati. Ciao!")
else:
	print("Elaboro...")

# Carico i restanti dataset: past e vaccini
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
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
lombardia_vaccini_janssen = lombardia_vaccini[ lombardia_vaccini['fornitore'] == 'Janssen' ]
lombardia_vaccini_janssen_tot = lombardia_vaccini_janssen['prima_dose'].sum()
#
primadose_tot = lombardia_vaccini['prima_dose'].sum() - lombardia_vaccini_janssen_tot			#<---
secondadose_tot = lombardia_vaccini['seconda_dose'].sum() + lombardia_vaccini_janssen_tot

#
##
### ESPORTO
##
#

with open('./story.json') as story_json_file:
	story_dict = json.load(story_json_file)

story_dict['perc_story'] += [float(percentuale)]						#è una python list
story_dict['ospedalizzati_story'] += [float(ospedalizzati_attuali)]
story_dict['terapie_story'] += [float(terapie_attuali)]
story_dict['deceduti_story'] += [float(deceduti_oggi)]
story_dict['primadose_story'] += [float(primadose_tot)]
story_dict['secondadose_story'] += [float(secondadose_tot)]

giorno = datetime.date.today().strftime("%d/%m/%Y")
story_dict['data'] = str(giorno)

with open('./story.json', "w") as story_json_file:
	json.dump(story_dict, story_json_file)

#
##
### CHIUDO
##
#

print()
print("Fatto. Dati aggiornati al " + str(giorno) + ".")