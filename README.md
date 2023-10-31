# Academic Google
Data una qualsiasi playlist con i timestamp nella descrizione, questo script troverà qualsiasi rifierimento con minutaggio preciso così da evitare di perdere tempo nella ricerca di un qualsiasi argomento

## Corsi disponibili di base
* Analisi Matematica I
> N.B.  
> i corsi possono essere modificati "in Courses.json"

## Istruzioni d'uso
### Setup (eseguire come ***amministratore***)
* in caso di download del codice sorgente avviare il terminale/cmd/powershell come ***amministratore*** e digitare
```console
pip install -r requirements.txt
```
> N.B.
> se "pip" non funziona sostituire con "pip3"

> N.B.
> assicurarsi che il terminale sia nella stella cartella del file altrimenti python non riuscirà a vedere i file interessati

### Compilazione
copiare e incollare sul terminale il comando in build.txt e inserire il percorso assoluto del file "AcademicGoogle.py" nelle virgolette vuote (per windows non è necessario il secondo comando)

### How-to-use da sorgente
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