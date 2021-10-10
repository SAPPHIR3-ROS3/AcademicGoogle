from collections import OrderedDict as OrdDict
from DBManagement import CreateDatabase
from DBManagement import SearchInDatabase
from googleapiclient.discovery import build as Activate
from os.path import exists as Exists
from re import finditer
from time import sleep as Sleep

CEnd = '\033[0m' # end of coloured text
ErrorText = lambda S: f'\33[31m{S}{CEnd}' # function for errors (red text)
WarningText = lambda S: f'\33[33m{S}{CEnd}' # function for warnings (yellow text)
OKText = lambda S: f'\33[92m{S}{CEnd}' # function for success operations (green text)
Link = lambda S: f'\33[90m{S}{CEnd}' # function for link of the videos (grey text)

def GetVideoIDs(PlaylistID = ''): # this function get youtube ids
    Pages = [None] #token IDs of the playlist pages
    VideosID = []
    i = 0 #page counter

    while True: #loop through all the pages of the playlist until there is no next page
        Request = Playlist.list(part='snippet', playlistId = PlaylistID, maxResults = 50, pageToken = Pages[i]) #specifing page
        Response = Request.execute() #effective request execution
        NextPageToken = Response.get('nextPageToken') #getting the next page token to get the next page

        if not NextPageToken: # check if token is None
            break

        Pages.append(NextPageToken) # add the token to token list
        i += 1 #increase of page counter

    for Page in Pages: #loop for every page of results
        Videos = Playlist.list(part='contentDetails', playlistId = PlaylistID, maxResults = 50, pageToken = Page) #setting the page
        Videos = Videos.execute() #request execution

        for Video in Videos['items']: #loop for every video of the playlist
            VideosID.append(Video['contentDetails']['videoId']) #append video link

    return VideosID

def GetVideoData(ID = ''): # this function get the video metadata given the video id
    Video = YoutubeAPI.videos().list(part = 'snippet, contentDetails', id = ID) #youtube API video obj
    Video = Video.execute()['items'][0] # video metadata
    Title = Video['snippet']['title'] #video title
    Duration = Video['contentDetails']['duration'][2 : - 1] #removing useless part of duration
    Duration = Duration.replace('H', ':').replace('M', ':') #formatting correctly the duration of timestamp
    Duration = ':'.join([Part if len(Part) > 1 else '0' + Part for Part in Duration.split(':')]) #setting proper length of timestamps segment
    DescriptionList = [Line.strip() for Line in Video['snippet']['description'].split('\n')] #splitting the description in lines
    RawDescription = str(Video['snippet']['description'])
    Timestamps = r'(?=(\d{1,2}:\d{2}:\d{2}|\d{2}:\d{2})\s(.+)\n?(\d{1,2}:\d{2}:\d{2}|\d{2}:\d{2})?)' #regex to find start timestamp, argument and end timestamps

    Description = [[Group if not Group == None else Duration for Group in Line.groups()] for Line in finditer(Timestamps, RawDescription)]
    #formatting in a list properly the matches (timestamps and argument)
    Description = [(Group[1], Group[0], Group[2]) for Group in Description][: - 1] #correcting the order of sublist and removing last(dup licate)

    VideoMetaData =\
    {
        'Link' : YoutubePrefix + ID,
        'Title' : Title, #title of the video (string)
        'Duration' :Duration, # duration HH:MM:SS (string)
        'Description' : Description # description (string : list of timestamps)(OrdDict)
    }

    return VideoMetaData

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
    Title =\
    """

░██████╗░░█████╗░░█████╗░░██████╗░██╗░░░░░███████╗  ░█████╗░███████╗
██╔════╝░██╔══██╗██╔══██╗██╔════╝░██║░░░░░██╔════╝  ██╔══██╗██╔════╝
██║░░██╗░██║░░██║██║░░██║██║░░██╗░██║░░░░░█████╗░░  ██║░░██║█████╗░░
██║░░╚██╗██║░░██║██║░░██║██║░░╚██╗██║░░░░░██╔══╝░░  ██║░░██║██╔══╝░░
╚██████╔╝╚█████╔╝╚█████╔╝╚██████╔╝███████╗███████╗  ╚█████╔╝██║░░░░░
░╚═════╝░░╚════╝░░╚════╝░░╚═════╝░╚══════╝╚══════╝  ░╚════╝░╚═╝░░░░░

███████╗███╗░░██╗░██████╗░██╗███╗░░██╗███████╗███████╗██████╗░██╗███╗░░██╗░██████╗░
██╔════╝████╗░██║██╔════╝░██║████╗░██║██╔════╝██╔════╝██╔══██╗██║████╗░██║██╔════╝░
█████╗░░██╔██╗██║██║░░██╗░██║██╔██╗██║█████╗░░█████╗░░██████╔╝██║██╔██╗██║██║░░██╗░
██╔══╝░░██║╚████║██║░░╚██╗██║██║╚████║██╔══╝░░██╔══╝░░██╔══██╗██║██║╚████║██║░░╚██╗
███████╗██║░╚███║╚██████╔╝██║██║░╚███║███████╗███████╗██║░░██║██║██║░╚███║╚██████╔╝
╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝╚══════╝╚═╝░░╚═╝╚═╝╚═╝░░╚══╝░╚═════╝░

    """
    print(OKText(Title))

    if not Exists('Data.db'): # check if the database file exists
        print(ErrorText('sembra che il database non sia presente nella cartella'))
        print(WarningText('digita "DBManagement.py -c" nella ricerca di sotto per tentare la creazione del database manualmente (l\'operazione può richiedere un poò di minuti)'))
        print(WarningText('assicurati che il file "Data.db" sia presente nella cartella altrimenti non avrai risultati dalle ricerche'))

    if Research == '': # check if the program has been called before
        UInput = input('Cerca: ')
    else: # if the program has been called before the new research is used as query
        UInput = Research

    if UInput == 'DBManagement.py -c': # check if the user input is a command
        CreateDatabase()

    if len(UInput) > 0: # check if the query is not empty
        UInput = [Query[1 :] if Query.startswith(' ') else Query for Query in UInput.lower().split(',')] # fix the input
        Matches = SearchInDatabase(list(set(UInput))) # search queries in the database
        DisplayQuery(Matches) # displey the results the queries

    else: #if the query is empty
        print(ErrorText('nessun risultato, query vuota'))

    Research = input('premere il tasto INVIO per chiudere il pragramma o digita la tua prossima ricerca (sempre separata da virgole in caso di ricerche multiple) ') # check for new input

    if Research == '': # no new input
        quit() # program closes
    else:
        Sleep(1)
        main(Research) # recursive call with next research

if __name__ == '__main__':
    main()
