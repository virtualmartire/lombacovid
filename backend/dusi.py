import os

def download():

	file_path1 = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv"

	# Uso il comando bash /curl/ per effettuare il download
	os.system('curl ' + file_path1 + ' > present.csv')
	# Ora dovresti avere il file nella stessa cartella in cui hai eseguito lo script

	file_path2 = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv"
	os.system('curl ' + file_path2 + ' > vaccini.csv')