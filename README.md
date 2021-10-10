# Google of Enginering
Trova qualsiasi elemento presente nei corsi universitari sul canale youtube del DIAG

## Materie disponibili
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

## Prerequisiti
* ultima versione di [python 3](https://www.python.org/) (consigliata la versione 3.6+ che è stata testata)
  * modulo googleAPI

## Istruzioni d'uso
* Setup (eseguire come ***amministratore***)
  > N.B.
  > assicurarsi che il terminale sia nella stella cartella del file altrimenti python non riuscirà a vedere i file interessati
* su Windows nel prompt dei comandi/powershell
  ```console
  python AutoSetupCLIversion.py
  ```
* su Linux/MacOS sul terminale
  ```console
  python3 AutoSetupCLIversion.py
  ```
* manuale
  * avviare il terminale/cmd/powershell come ***amministratore*** e digitare
    ```console
    pip install googleapi
    ```
    > N.B.
    > se "pip" non funziona usare "pip3"

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
se ci fossero problemi con il programma non esitate alasciare una Issue su Github o contattatemi su discord a YourSenpai#1953