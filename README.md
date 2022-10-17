Trovate in questa repo tutto il codice sottostante il progetto lombacovid aggiornato al giorno 16 ottobre 2022.

# macinino

"macinino.py" è il motore backend del sito. Dopo aver recuperato i dati del progetto (dal file story.csv), aver controllato che il sito non sia già stato aggiornato e aver verificato che siano stati pubblicati dei dati nuovi, è l'algoritmo che aggiorna tutti i valori e li pubblica di nuovo sul server. Il Dockerfile presente in questa repo permette di riprodurlo in maniera completamente affidabile e portatile.

# frontend

"creator.js" è lo script che inserisce nella pagina i dati numerici, mentre "grafichini.js" è quello che, tramite Google Charts, disegna i grafici. E tutto il resto è noia.