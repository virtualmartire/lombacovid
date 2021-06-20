"""Prende i dati di ieri (past.csv), di oggi (present.csv) e dei vaccini (vaccini.csv) per calcolare ed esportare
un po' di situazioni."""

import pandas as pd
import numpy as np
from datetime import date
import os
import shutil
import json

import grafichini as graph

print()

#
##
### PREPARO GLI INPUT
##
#

past = pd.read_csv('past.csv')

#present devo salvarlo perché mi serve anche domani
os.system('curl https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv > present.csv')
present = pd.read_csv('present.csv')

#il dataset dei vaccini invece ha la history già di suo
vaccini = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')

lombardia_past = past[ past['denominazione_regione'] == 'Lombardia' ]
lombardia_present = present[ present['denominazione_regione'] == 'Lombardia' ]
lombardia_vaccini = vaccini[ vaccini['area'] == 'LOM' ]

#controllo che siano giusti, altrimenti non se ne fa niente
print()
print(lombardia_present.tail(1))
print()
print(lombardia_vaccini.tail(1))
print()
datacheck = input("Dataset impostati giusti? (s/n) ")
if datacheck == "n":
	os.remove('present.csv')
	print()
	exit("File smarmellati. Ciao!")
elif datacheck != "s":
	print()
	raise Exception("Risposta umana non riconosciuta.")

#faccio il backup
shutil.rmtree('backup')
os.system('cp -r pantarei backup')
shutil.copy('past.csv', 'backup')

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
secondadose_tot = lombardia_vaccini['seconda_dose'].sum() + lombardia_vaccini_janssen_tot		#<---
primadose_perc = np.around(primadose_tot / 10060965 * 100, 2)									#<---
secondadose_perc = np.around(secondadose_tot / 10060965 * 100, 2)								#<---

#
##
### ESPORTO
##
#

# Le stories
with open('pantarei/story.json') as story_json_file:
	story_dict = json.load(story_json_file)

story_dict['perc_story'] += [float(percentuale)]						#è una python list
story_dict['ospedalizzati_story'] += [float(ospedalizzati_attuali)]
story_dict['terapie_story'] += [float(terapie_attuali)]
story_dict['deceduti_story'] += [float(deceduti_oggi)]
story_dict['primadose_story'] += [float(primadose_tot)]
story_dict['secondadose_story'] += [float(secondadose_tot)]

with open('pantarei/story.json', "w") as story_json_file:
	json.dump(story_dict, story_json_file)

# I grafici
graph.curve(label = 'perc_story', filename = "rapporto", color = "#f33a30", ylabel = "rapporto = pos/tam")
graph.curve('ospedalizzati_story', "ospedalizzati", "#f99726", "ospedalizzati")
graph.curve('terapie_story', "terapie_attuali", "#44a546", "t.i. occupate")
graph.histo('deceduti_story', "deceduti_giornalieri", "#1c8af2", "deceduti")
graph.vax(filename = "vaccini", color = "#9023a8")

# Gli oggi
with open('pantarei/oggi.json') as oggi_json_file:
	oggi_dict = json.load(oggi_json_file)

oggi_dict['perc'] = str(percentuale) + "%"
oggi_dict['ospedalizzati_attuali'] = str(ospedalizzati_attuali)
oggi_dict['terapie_attuali'] = str(terapie_attuali)
oggi_dict['deceduti_oggi'] = str(deceduti_oggi)
oggi_dict['primadose_perc'] = str(primadose_perc) + "%"
oggi_dict['secondadose_perc'] = str(secondadose_perc) + "%"

giorno = date.today().strftime("%d/%m/%Y")
oggi_dict['data'] = str(giorno)

with open('pantarei/oggi.json', "w") as oggi_json_file:
	json.dump(oggi_dict, oggi_json_file)

#
##
### CHIUDO
##
#

os.remove('past.csv')
os.rename(r'present.csv', r'past.csv')

print("\nFatto. Dati aggiornati al " + str(giorno) + ".")
os.system('open /Users/stefanomartire/Documents/GitHub/lombacovid/backend/pantarei')