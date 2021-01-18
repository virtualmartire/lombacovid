Trovate nelle cartelle qui accanto tutto il codice sottostante il progetto lombacovid.it aggiornato al giorno 18 novembre 2021.

+++ BACKEND +++

Nella cartella "backend" sono presenti tutti gli algoritmi con i quali, giornalmente, aggiorno i dati del sito.

"macinino.py" è il main. Esso si serve del modulo "dusi.py" per scaricare il dataset csv della Protezione Civile per poi, sostanzialmente, estrarre ed elaborare le informazioni desiderate utilizzando la libreria "pandas". Il modulo "grafichini.py" è quello con cui, servendomi della libreria "matplotlib", genero i grafici.

Una nota a parte va fatta per l'estrazione dei dati sui vaccini: a oggi, questi ultimi vengono pubblicati non attraverso formati standard (e realmente utilizzabili) dell'Analisi dei Dati, ma attraverso una web-dashboard [https://app.powerbi.com/view?r=eyJrIjoiMzg4YmI5NDQtZDM5ZC00ZTIyLTgxN2MtOTBkMWM4MTUyYTg0IiwidCI6ImFmZDBhNzVjLTg2NzEtNGNjZS05MDYxLTJjYTBkOTJlNDIyZiIsImMiOjh9] che si può solamente visualizzare. Per questo motivo, nel file "neuralvax.py" trovate il codice della rete neurale (keras_ocr) che uso per rendere trattabili questi dati: l'input è lo screenshot della suddetta pagina (ottenibile in modo facile e automatico attraverso la libreria "selenium"), mentre l'output è, appunto, il numero intero dei vaccinati attuali in Lombardia (che poi divido per la popolazione di modo da ottenere una percentuale utile...).

Nella cartella "pantarei" sono contenuti gli output del main. Nella cartella "backup", sempre generata dal main, sono contenuti i suoi output dell'esecuzione precedente.

La totalità del codice backend è scritta in Python.

+++ FRONTEND +++

Nella cartella "frontend" sono presenti tutti i codici che costituiscono il sito nel browser.

Il protagonista è "index.php", che tramite il comando <?php include();?> sostituisce le parti dinamiche del sito (gli indici statistici, i grafici, ecc.) con ciò che il main backend di giorno in giorno produce (e che è salvato nella cartella "pantarei", la stessa di prima).

Tutto il resto è semplice HTML e CSS (quest'ultimo situato in una cartella apposita omonima e fondamentalmente costuito da un template di w3.css).
