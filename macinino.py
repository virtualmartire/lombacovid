"""Prende i dati di ieri (past.csv) e di oggi (present.csv) per calcolare un po' di situazioni.
Poi salva tutto nelle rispettive stories e html."""

import pandas as pd
import numpy as np
import grafichini as graph
from datetime import date
import dusi
import os
import shutil

print("Caricamento...")

#prima di tutto BACKUP
shutil.rmtree('backup')
os.system('cp -r pantarei backup')

#
##
### LEGGO I DATI
##
#

dusi.download()

past = pd.read_csv('past.csv')
present = pd.read_csv('present.csv')

lombardia_present = present[ present['denominazione_regione'] == 'Lombardia' ]
lombardia_past = past[ past['denominazione_regione'] == 'Lombardia' ]

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
percentuale = np.around(nuovi_positivi / tamponi_oggi * 100, 2)

#in ospedale adesso
ospedalizzati = lombardia_present['totale_ospedalizzati'].values[0]

#in T.I. adesso
terapie_attuali = lombardia_present['terapia_intensiva'].values[0]

#deceduti oggi
tot_deceduti_present = lombardia_present['deceduti'].values[0]
tot_deceduti_past = lombardia_past['deceduti'].values[0]
deceduti_oggi = tot_deceduti_present - tot_deceduti_past

#
##
### ESPORTO
##
#

#story dei rapporti
f = open('pantarei/perc_story.txt', 'a')
f.write( "\n" + str(percentuale) )
f.close()

#story degli ospedalizzati
f = open('pantarei/ospedalizzati_story.txt', 'a')
f.write( "\n" + str(ospedalizzati) )
f.close()

#story delle terapie
f = open('pantarei/terapie_story.txt', 'a')
f.write( "\n" + str(terapie_attuali) )
f.close()

#story dei deceduti
f = open('pantarei/deceduti_story.txt', 'a')
f.write( "\n" + str(deceduti_oggi) )
f.close()

""" """

#grafico rapporti
graph.curve(path = "pantarei/perc_story.txt", filename = "rapporto", color = "#ff0000", ylabel = "rapporto = pos/tam")

#grafico ospedalizzati
graph.curve("pantarei/ospedalizzati_story.txt", "ospedalizzati", "#33cc33", "ospedalizzati")

#grafico terapie
graph.curve("pantarei/terapie_story.txt", "terapie_attuali", "#005ce6", "T.I. occupate")

#grafico deceduti
graph.histo("pantarei/deceduti_story.txt", "deceduti_giornalieri", "#6600cc", "deceduti")

""" """

#html del rapporto
f = open('pantarei/perc.txt', 'w')
f.write("<span id='perc'>" + str(percentuale) + "%</span>")
f.close()

#html dei nuovi positivi
f = open('pantarei/nuovipos.txt', 'w')
f.write("<span id='nuovipos'>" + str(nuovi_positivi) + "</span>")
f.close()

#html dei tamponi di oggi
f = open('pantarei/tam.txt', 'w')
f.write("<span id='tam'>" + str(tamponi_oggi) + "</span>")
f.close()

#html degli ospedalizzati
f = open('pantarei/ospedalizzati.txt', 'w')
f.write("<span id='ospedalizzati'>" + str(ospedalizzati) + "</span>")
f.close()

#html delle terapie attuali
f = open('pantarei/terapie_attuali.txt', 'w')
f.write("<span id='terapie_attuali'>" + str(terapie_attuali) + "</span>")
f.close()

#html dei deceduti oggi
f = open('pantarei/deceduti_oggi.txt', 'w')
f.write("<span id='deceduti_oggi'>" + str(deceduti_oggi) + "</span>")
f.close()

""" """

giorno = date.today().strftime("%d/%m/%Y")
f = open('pantarei/data.txt', 'w')
f.write("<span>" + str(giorno) + "</span>")
f.close()

#
##
### CHIUDO
##
#

os.remove("past.csv")
os.rename(r'present.csv', r'past.csv')

print("Fatto. Dati aggiornati al " + str(giorno) + ".")