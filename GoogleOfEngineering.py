from collections import OrderedDict as OrdDict
from DBManagement import SearchInDatabase
from googleapiclient.discovery import build as Activate
from re import finditer

APIKey = 'AIzaSyA-dlBUjVQeuc4a6ZN4RkNUYDFddrVLxrA' #API Key need to perform the research
YoutubeAPI = Activate('youtube', 'v3', developerKey = APIKey) #activation of youtube service by youtube API Key
Playlist = YoutubeAPI.playlistItems() #playlist of videos
YoutubePrefix = 'https://www.youtube.com/watch?v='

CEnd = '\033[0m' # end of coloured text
ErrorText = lambda S: f'\33[31m{S}{CEnd}' #function for errors (red text)
WarningText = lambda S: f'\33[33m{S}{CEnd}' #function for warnings (yellow text)
OKText = lambda S: f'\33[92m{S}{CEnd}' #function for success operations (green text)
Link = lambda S: f'\33[90m{S}{CEnd}'


def GetVideoIDs(PlaylistID = ''): #this function get youtube ids
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

def GetVideoData(ID = ''): #this function get the video metadata given the video id
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

def DisplayQuery(Data = None): #this function display the result in the proper way
    #print(f'{sum([len(Data[Query]) for Query in Data])} risultati trovati')
    if Data is not None:
        for Key, Matches in Data.items():
            print(Key)
            for Match in Matches:
                print(f'\t[{Match["Course"]}] {Match["VideoTitle"]}')
                print(Link(f'\t{Match["VideoLink"]}'))
                print('\t...')
                print(OKText(f'\t[{Match["StartTimestamp"]}|{Match["EndTimestamp"]}] {Match["TimestampDescription"].replace("   ", " ")}'))
                print('\t...')
                print('\t'+'-' * 110)
    else:
        print(ErrorText('Nessun risultato'))

# LEGACY

def SearchData(Query = '', Data = []): #this function search between the data of the videos
    Matches = OrdDict() #ordered dictionary of results

    for Lesson in Data: #for loop for every lesson in the database
        Argument = OrdDict() #dictionary for every line of the lesson description
        for Key, Value in Lesson['Description'].items(): #for loop for every line of the description
            if Query.lower() in Key.lower(): #check if the query is in the line of the description
                Argument[Key] = Value #set the argument (key) and the timestamps (value)
        if len(Argument) > 0: #check if the result in the lesson is not empty
            Argument['Link'] = Lesson['Link'] #link of the video lesson
            Matches[Lesson['Title']] = Argument #set the title of the video lesson (key) and the result(argument)

    return Matches

def Search(Query = '', Data = OrdDict()): #this function search in the database and filter properly the result
    Matches = OrdDict() #ordered dictionary of results

    for KeyLesson, ValueLesson in Data.items(): #loop for all the lesson
        Argument = OrdDict() #temporary dictionary for arguments in lesson
        for KeyArgument, ValueArgument in ValueLesson.items(): #loop for every argument in a lesson
            if Query.lower() in KeyArgument.lower(): #check if the query is in the argument (case sensitive disabled)
                Argument[KeyArgument] = ValueArgument #add the result to temporary dictionary
        if len(Argument) > 0: #check if the temporary dictionary does really have at least an elements
            Matches[KeyLesson] = Argument #add the temporary dictionary to the results

    return Matches

def DisplayResult(Argument = '', Matches = OrdDict()): #this function display the results of queries indented properly
    print(Argument)
    if len(Matches) > 0: #check if there is some results
        for KeyMatch, ValueMatch in Matches.items(): # loop for every lesson present in the results
            print('\t', KeyMatch) #proper indentation
            for KeyArgument, ValueArgument in ValueMatch.items(): #loop for every argument of every lesson
                print('\t' * 2, KeyArgument, ValueArgument) #proper indentation
    else:
        print('\t', 'Nessun risultato')

if __name__ == '__main__':
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
    UInput = input('Cerca: ')

    if len(UInput) > 0:
        UInput = [Query[1 :] if Query.startswith(' ') else Query for Query in UInput.lower().split(',')]
        Matches = SearchInDatabase(list(set(UInput)))
        DisplayQuery(Matches)
    else:
        print(ErrorText('no results, empty query'))
