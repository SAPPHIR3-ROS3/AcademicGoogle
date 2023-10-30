# Academic Google
Data una qualsiasi playlist con i timestamp nella descrizione, questo script troverà qualsiasi rifierimento con minutaggio preciso così da evitare di perdere tempo nella ricerca di un qualsiasi argomento

## Corsi disponibili di base
* Analisi Matematica I
* Informatica I: Python
* Informatica I: Modelli
* Fisica 1-2
* Sistemi di Calcolo
* Robotics I
* Robotics II
* Tecniche di Programmazione
* Ricerca Operativa
* Basi di Dati
* Statistica
* Web Information Retraial
> N.B.  
> i corsi possono essere modificati "in Courses.json"
## Prerequisiti
* ultima versione di [python 3](https://www.python.org/) (consigliata la versione 3.6+ che è stata testata)

## Istruzioni d'uso
* Setup (eseguire come ***amministratore***)
  > N.B.
  > assicurarsi che il terminale sia nella stella cartella del file altrimenti python non riuscirà a vedere i file interessati
* avviare il terminale/cmd/powershell come ***amministratore*** e digitare
  ```console
  pip install -r requirements.txt
  ```
  > N.B.
  > se "pip" non funziona sostituire con "pip3"

* ### How-to
* su Windows nel prompt dei comandi
  ```console
  python GoogleOfEngineering.py
  ```
* su Linux/MacOS sul terminale
  ```console
  python3 GoogleOfEngineering.py
  ```
* una volta avviato il programma digitare gli argomenti a cui si è interessati (es. Integrali, Limiti ecc.) separati da una virgola (arg1, arg2, ...)
* gli argomenti verranno suddivisi per query e per corso

## Contatti
se ci fossero problemi con il programma non esitate a lasciare una Issue su Github o contattatemi su discord a YourSenpai#1953