import os

def download():
	file_path = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv"

	# Uso il comando bash /curl/ per effettuare il download
	# L'opzione -L introduce il link
	# L'opzione -O credo serva a rinominare l'output come il file di origine
	os.system('curl ' + file_path + ' > present.csv')

	# Ora dovresti avere il file nella stessa cartella in cui hai eseguito lo script

	if input("Past e Present impostati giusti? (s/n) ") == "n":
		os.remove("present.csv")
		exit("File smarmellati. Ciao!")