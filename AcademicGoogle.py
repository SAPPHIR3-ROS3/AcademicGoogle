from DBManagement import CreateDatabase
from DBManagement import Verify
from DBManagement import Delete
from DBManagement import SearchInDatabase
from os.path import exists as Exists
from time import sleep as Sleep

Title =\
"""

░█████╗░░██████╗░█████╗░██████╗░███████╗███╗░░░███╗██╗░██████╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝████╗░████║██║██╔════╝
███████║██║░░░░░███████║██║░░██║█████╗░░██╔████╔██║██║██║░░░░░
██╔══██║██║░░░░░██╔══██║██║░░██║██╔══╝░░██║╚██╔╝██║██║██║░░░░░
██║░░██║╚██████╗██║░░██║██████╔╝███████╗██║░╚═╝░██║██║╚██████╗
╚═╝░░╚═╝░╚═════╝╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░░░░╚═╝╚═╝░╚═════╝
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░██████╗░░██████╗░░██████╗░░██████╗░██╗░░░░░███████╗░░░░░░░░░░
██╔════╝░██╔═══██╗██╔═══██╗██╔════╝░██║░░░░░██╔════╝░░░░░░░░░░
██║░░███╗██║░░░██║██║░░░██║██║░░███╗██║░░░░░█████╗░░░░░░░░░░░░
██║░░░██║██║░░░██║██║░░░██║██║░░░██║██║░░░░░██╔══╝░░░░░░░░░░░░
╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗░░░░░░░░░░
░╚═════╝░░╚═════╝░░╚═════╝░░╚═════╝░╚══════╝╚══════╝░░░░░░░░░░ 

"""
HDOCS =\
"""scrivi
'--help' per vedere questo messaggio
'--verify' per verificare o aggiornare il database
'--delete' per eliminare il database (il database verrà ricreato al prosimo avvio)
qualsiasi altra cosa verra cercata nel database locale se ci sono ',' verranno fatte più ricerche
""" # help documentation

CEnd = '\033[0m' # end of coloured text
ErrorText = lambda S: f'\33[31m{S}{CEnd}' # function for errors (red text)
WarningText = lambda S: f'\33[33m{S}{CEnd}' # function for warnings (yellow text)
OKText = lambda S: f'\33[92m{S}{CEnd}' # function for success operations (green text)
Link = lambda S: f'\33[90m{S}{CEnd}' # function for link of the videos (grey text)

def ConvertTimeStamp(Timestamp = ''): # this fucntion convert a timestamp in a single number
    Timestamp = reversed([int(Part) for Part in Timestamp.split(':')]) # reverse the list composed byhours minutes seconds (as int)
    Timestamp = sum([Part * (60**i) for i, Part in enumerate(Timestamp)]) # convert the timestamp in seconds
    return Timestamp

def DisplayQuery(Data = None): # this function display the result in the proper way
    if Data is not None: # check if the data received is actually data
        if sum([len(Data[Query]) for Query in Data]) > 0: # check if the query has given some result
            print(f'{sum([len(Data[Query]) for Query in Data])} risultati trovati') # print print the sum of all result found

            for Key, Matches in Data.items(): # for loop for every query searched
                print(Key, '\n') # print the searched query
                for Match in Matches: # for loop for every result found in the database
                    print(f'\t[{Match["Course"]}] {Match["VideoTitle"]}') # playlist/origin
                    print(f'\t{Match["ChannelTitle"]}') # channel name
                    print(Link(f'\t{Match["VideoLink"]}?t={ConvertTimeStamp(Match["StartTimestamp"])}')) # link of the youtube video
                    print('\t...') # spacing
                    print(OKText(f'\t[{Match["StartTimestamp"]}|{Match["EndTimestamp"]}] {Match["TimestampDescription"].replace("   ", " ")}')) # timestamp and description of result
                    print('\t...') # spacing
                    print('\t'+'-' * 110) # division between result

        else:
            print(ErrorText('Nessun risultato')) # 0 results

    else:
        print(ErrorText('Nessun risultato')) # 0 results

def main(Research = ''): # program function
    
    if not Exists('Data.db'): # check if the database file exists
        print(ErrorText('sembra che il database non sia presente nella cartella'))
        print(WarningText('il database verrà creato adesso l\'operazione potrebbe richiedere alcuni minuti'))
        CreateDatabase()

    print(OKText(Title))

    if Research == '': # check if the program has been called before
        UInput = input('Cerca(scrivi --help per aiuto): ')

        if UInput == '': quit()
    else: # if the program has been called before the new research is used as query
        UInput = Research

    if len(UInput) > 0: # check if the query is not empty
        if UInput == '--help':
            print(HDOCS) #show the help docs
            input('premi invio per continuare')
            main() #program restart
        elif UInput == '--verify':
            Verify() # verify that the database is up to date
            input('premi invio per continuare')
            main() # program restart
        elif UInput == '--delete':
            Delete() # delete the database file
            input('premi invio per chiudere')
            quit()
        else:
            UInput = [Query[1 :] if Query.startswith(' ') else Query for Query in UInput.lower().split(',')] # fix the input
            Matches = SearchInDatabase(list(set(UInput))) # search queries in the database
            DisplayQuery(Matches) # displey the results the queries

    else: #if the query is empty
        print(ErrorText('nessun risultato, query vuota'))

    Research = input('premere il tasto INVIO per chiudere il pragramma o digita la tua prossima ricerca (sempre separata da virgole in caso di ricerche multiple) ') # check for new input

    if Research == '': # no new input
        quit() # program closes
    else:
        Sleep(1) # give time to the user to "prepare"
        main(Research) # recursive call with next research

if __name__ == '__main__':
    main()
