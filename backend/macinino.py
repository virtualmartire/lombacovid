"""Prende i dati di ieri (past.csv) e di oggi (present.csv) per calcolare un po' di situazioni.
Poi salva tutto nelle rispettive stories e html."""

import pandas as pd
import numpy as np
from datetime import date
import os
import shutil

import grafichini as graph
import dusi
import neuralvax

#
##
### PREPARO GLI INPUT
##
#

#controllo che esistano, altrimenti non se ne fa niente
dusi.download()

#faccio il backup
shutil.rmtree('backup')
os.system('cp -r pantarei backup')
shutil.copy('past.csv', 'backup')
shutil.copy('timestep.txt', 'backup')
shutil.copy('timestep_vax.txt', 'backup')

past = pd.read_csv('past.csv')
present = pd.read_csv('present.csv')

lombardia_present = present[ present['denominazione_regione'] == 'Lombardia' ]
lombardia_past = past[ past['denominazione_regione'] == 'Lombardia' ]

neuralvax.screenshot()

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

#vaccinati
vax_tot_hp = neuralvax.gino_leggi()
print("Ciao, sono Gino. Ecco cosa ho trovato:")
print(vax_tot_hp)
confirmed = input("Qual è quello giusto? (0-9/n) ")
if confirmed == "n":
	vax_tot = int( input("Ok dimmi tu: ") )
else:
	vax_tot = int(vax_tot_hp[int(confirmed)])
vax_perc = np.around(vax_tot / 10060965 * 100, 2)

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

#story dei vaccinati
f = open('pantarei/vaccinati_story.txt', 'a')
f.write( "\n" + str(vax_tot) )
f.close()

""" """

#grafico rapporti
graph.curve(path = "pantarei/perc_story.txt", filename = "rapporto", color = "#f33a30", ylabel = "rapporto = pos/tam")

#grafico ospedalizzati
graph.curve("pantarei/ospedalizzati_story.txt", "ospedalizzati", "#f99726", "ospedalizzati")

#grafico terapie
graph.curve("pantarei/terapie_story.txt", "terapie_attuali", "#44a546", "t.i. occupate")

#grafico deceduti
graph.histo("pantarei/deceduti_story.txt", "deceduti_giornalieri", "#1c8af2", "deceduti")

#grafico vaccinati
graph.vax("pantarei/vaccinati_story.txt", "tot_vaccinati", "#9023a8", "tot vaccinati")

""" """

#html del rapporto
f = open('pantarei/perc.txt', 'w')
f.write( str(percentuale) + "%" )
f.close()

#html degli ospedalizzati
f = open('pantarei/ospedalizzati.txt', 'w')
f.write( str(ospedalizzati) )
f.close()

#html delle terapie attuali
f = open('pantarei/terapie_attuali.txt', 'w')
f.write( str(terapie_attuali) )
f.close()

#html dei deceduti oggi
f = open('pantarei/deceduti_oggi.txt', 'w')
f.write( str(deceduti_oggi) )
f.close()

#html della percentuale di vaccinati totali
f = open('pantarei/vax_perc.txt', 'w')
f.write( str(vax_perc) + "%")
f.close()

""" """

giorno = date.today().strftime("%d/%m/%Y")
f = open('pantarei/data.txt', 'w')
f.write( str(giorno) )
f.close()

#
##
### CHIUDO
##
#

os.remove("past.csv")
os.rename(r'present.csv', r'past.csv')

print("Fatto. Dati aggiornati al " + str(giorno) + ".")