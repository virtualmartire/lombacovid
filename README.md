Trovate nelle cartelle qui accanto tutto il codice sottostante il progetto lombacovid.it aggiornato al giorno 30 gennaio 2021.

+++ BACKEND +++

Nella cartella "backend" sono presenti tutti gli algoritmi con i quali, giornalmente, aggiorno i dati del sito.

"macinino.py" è il main. Esso si serve del modulo "dusi.py" per scaricare i dataset csv del Governo per poi, sostanzialmente, estrarre ed elaborare le informazioni desiderate utilizzando la libreria "pandas". Il modulo "grafichini.py" è quello con cui, servendomi della libreria "matplotlib", genero i grafici.

Nella cartella "pantarei" sono contenuti gli output del main. Nella cartella "backup", sempre generata dal main, sono contenuti i suoi output dell'esecuzione precedente.

"neuralvax.py" è il codice di una rete neurale che utilizzavo per leggere i dati dei vaccini da una web-dashboard quando il dataset csv non era ancora disponibile.

La totalità del codice backend è scritta in Python.

+++ FRONTEND +++

Nella cartella "frontend" sono presenti tutti i codici che costituiscono il sito nel browser.

Il protagonista è "index.php", che tramite il comando <?php include();?> sostituisce le parti dinamiche del sito (gli indici statistici, i grafici, ecc.) con ciò che il main backend di giorno in giorno produce (e che è salvato nella cartella "pantarei", la stessa di prima).

Tutto il resto è semplice HTML e CSS (quest'ultimo situato in una cartella apposita omonima e fondamentalmente costuito da un template di w3.css).
