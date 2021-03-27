Trovate nelle cartelle qui accanto tutto il codice sottostante il progetto lombacovid.it aggiornato al giorno 27 marzo 2021.

+++ BACKEND +++

Nella cartella "backend" sono presenti tutti gli algoritmi con i quali, giornalmente, aggiorno i dati del sito.

"macinino.py" è il main. Dopo aver scaricato i dataset csv del Governo elabora le informazioni desiderate utilizzando la libreria "pandas". Il modulo "grafichini.py" è quello con cui, servendomi della libreria "matplotlib", genero i grafici.

Nella cartella "pantarei" sono contenuti gli output del main. Nella cartella "backup", sempre generata dal main, sono contenuti i suoi output dell'esecuzione precedente.

"neuralvax.py" è il codice di una rete neurale che utilizzavo per leggere otticamente i dati dei vaccini da una web-dashboard quando il dataset csv non era ancora disponibile.

La totalità del codice backend è scritta in Python.

+++ FRONTEND +++

Nella cartella "frontend" sono presenti tutti i codici che costituiscono il sito nel browser.

Si tratta di semplice HTML con un po' di javascript per gestire le parti dinamiche del sito (i dati sono presi dai file json generati dagli algoritmi suddetti e messi nella cartella "pantarei"). Gli stili CSS sono situati in una cartella apposita omonima e sono fondamentalmente costuiti da un template di w3.css.
