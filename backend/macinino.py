"""Script che aggiunge tutte le righe mancanti al dataset considerato l'ultimo aggiornamento e
l'ultimo dato disponibile. Da eseguire una volta a settimana quando vengono pubblicati i dati."""

import pandas as pd
import numpy as np
import datetime
import json
import ftplib


def main(story_csv: pd.DataFrame):

	### PREPARO GLI INPUT ###

	# Recupero la data dell'ultimo aggiornamento di lombacovid e valuto se procedere

	data_ultimo_aggiornamento = story_csv['data'].values[-1]
	oggi_slash = datetime.date.today().strftime('%d/%m/%Y')
	if oggi_slash == data_ultimo_aggiornamento:
		print("Sito già aggiornato!")
		return story_csv, False

	data_ultimo_aggiornamento = data_ultimo_aggiornamento.split("/")
	data_ultimo_aggiornamento.reverse()
	data_ultimo_aggiornamento = list(map(int, data_ultimo_aggiornamento))

	yesterday_dataobj = datetime.date(*data_ultimo_aggiornamento)
	oggi_dataobj = (yesterday_dataobj + datetime.timedelta(days=1))
	yesterday = yesterday_dataobj.strftime("%Y%m%d")
	oggi = oggi_dataobj.strftime("%Y%m%d")
	oggi_slash = oggi_dataobj.strftime('%d/%m/%Y')				# oggi e yesterday secondo l'algoritmo

	# Verifico che il dataset di oggi esista

	oggi_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-'+oggi+'.csv'
	try:
		present = pd.read_csv(oggi_url)
	except:
		print(f"Dataset del {oggi_slash} non ancora disponibile. Arrivederci!")
		return story_csv, False
	lombardia_present = present[ present['denominazione_regione'] == 'Lombardia' ]

	# Carico i restanti dataset: past e vaccini

	yesterday_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-'+yesterday+'.csv'
	past = pd.read_csv(yesterday_url)
	lombardia_past = past[ past['denominazione_regione'] == 'Lombardia' ]

	vaccini = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')
	lombardia_vaccini = vaccini[ vaccini['area'] == 'LOM' ]


	### ELABORO ###

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


	### ESPORTO ###

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

	### CHIUDO ###

	print()
	print(f"Dati aggiornati al {oggi_slash}.")

	return story_csv, True


if __name__ == "__main__":
	
	story_csv = pd.read_csv('https://www.lombacovid.it/story.csv')
	
	break_condition = True
	while break_condition == True:
		story_csv, break_condition = main(story_csv)

	story_csv.set_index('data', inplace=True)
	story_csv.to_csv('frontend/story.csv')
	with open('credentials.json', 'r') as credentials_file:
		credentials_dict = json.load(credentials_file)
	session = ftplib.FTP('ftp.lombacovid.it', credentials_dict['id'], credentials_dict['password'])
	with open('frontend/story.csv', 'rb') as story_file:
		session.storbinary('STOR www.lombacovid.it/story.csv', story_file)

	session.quit()