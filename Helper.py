from collections import OrderedDict as OrdDict
from googleapiclient.discovery import build as Activate

def FetchPages(): #this function retrieve all the "pages" of video
    Tokens = [None] #token IDs of the palylist pages
    i = 0 #page counter

    while True: #loop through all the pages of the playlist until there is no next page
        Request = Playlist.list(part='snippet', playlistId = ID, maxResults = 50, pageToken = Tokens[i]) #specifing page
        Response = Request.execute() #effective request execution
        NextPageToken = Response.get('nextPageToken') #getting the next page token to get the next page

        if not NextPageToken: # check if token is None
            break

        Tokens.append(NextPageToken) # add the token to token list
        i += 1 #increase of page counter

    return Tokens

def DataToDict(Tokens):
    Data = OrdDict()  #raw data
    Index = 'Analisi Matematica 1, Prof. Camilli - Indice lezioni' #index of lesson

    for Token in Tokens: #loop for every page of results
        Videos = Playlist.list(part='snippet', playlistId = ID, maxResults = 50, pageToken = Token) #setting the page
        Videos = Videos.execute() #request execution

        for Video in Videos['items']: #loop for every video of the playlist
            Video = Video['snippet'] #video metadata
            Key = Video['title'] # video title
            Format = [Line.split() for Line in Video['description'].split('\n')] #separeting description by line

            if Key == Index: #check if it is the first video
                del Video #delete the selected video
            else:
                Value =\
                    {
                        ' '.join(Line[1:]) :
                            ([Line[0], Format[Format.index(Line) + 1][0]] if not Line == Format[-1] else Line[0][0])
                        for Line in Format[3:]
                    } # set the argument as key and minutes

                Data[Key] = Value #lesson title as key and argument minutes as value

    return Data

def UpdateData():
    PageTokens = FetchPages()
    Data = DataToDict(PageTokens)
    print('Dati aggiornati')

    return Data

def FetchVideos(): #this function get youtube ids
    Pages = FetchPages() #fatching all the pages of a playlist
    VideosID = []

    for Page in Pages: #loop for every page of results
        Videos = Playlist.list(part='contentDetails', playlistId = ID, maxResults = 50, pageToken = Page) #setting the page
        Videos = Videos.execute() #request execution

        for Video in Videos['items']: #loop for every video of the playlist
            VideosID.append(Video['contentDetails']['videoId']) #append video link

    return VideosID

def GetVideoData(ID = ''): #this function get the video metadata given the video id
    Video = YoutubeAPI.videos().list(part = 'snippet, contentDetails', id = ID) #youtube API video obj
    Video = Video.execute()['items'][0] # video metadata
    Title = Video['snippet']['title'] #video title
    Duration = Video['contentDetails']['duration'][2 : - 1] #removing useless part of duration
    Duration = Duration.replace('H', ':').replace('M', ':') #formatting correctly the duration as timestamps
    DescriptionList = [Line.split() for Line in Video['snippet']['description'].split('\n')[3 :]] #splitting the description in lines
    Description = OrdDict() #ordered dictionary of description

    for Line in range(len(DescriptionList)): #for loop for every line of the description
        if not Line == len(DescriptionList) - 1: #check if is not the last
            Value = [DescriptionList[Line][0], DescriptionList[Line + 1][0]] #timestamps
        else: #last line
            Value = [DescriptionList[Line][0], Duration] #timestamps

        Key = ' '.join(DescriptionList[Line][1:]) #argument as string
        Description[Key] = Value #argument title (key) timestamps (value)

    VideoMetaData =\
    {
        'Link' : YoutubePrefix + ID,
        'Title' : Title, #title of the video (string)
        'Duration' :Duration, # duration HH:MM:SS (string)
        'Description' : Description # description (string : list of timestamps)(OrdDict)
    }

    return VideoMetaData

def GetPlaylistData(): #retrive all the data of the videos
    PlaylistData = [] #list for all the videos

    for ID in VideoIDs: #for loop for every video
        PlaylistData.append(GetVideoData(ID)) #appending the data for every video

    return PlaylistData

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

def DisplayQuery(Query = '', Data = OrdDict()): #this function display the result in the proper way
    print(Query)
    if len(Data) > 0: #check if there is some result
        for Lesson, Arguments in Data.items(): #for loop for lesson with result
            print('\t', Lesson)
            for Argument, Timestamps in Arguments.items(): #for loop for every result of the lesson
                if not Argument == 'Link': #print all the result except the link
                    print('\t' * 2, Argument, Timestamps)
    else: #case of no result
        print('\t', 'Nessun risultato')

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

APIKey = 'AIzaSyA-dlBUjVQeuc4a6ZN4RkNUYDFddrVLxrA' #API Key need to perform the research
ID = 'PLAQopGWlIcyZlCmXWE_KvtMi57Mwbyf6C' #Playlist ID
YoutubeAPI = Activate('youtube', 'v3', developerKey = APIKey) #activation of youtube service by youtube API Key
YoutubePrefix = 'https://www.youtube.com/watch?v='
Playlist = YoutubeAPI.playlistItems() #playlist of videos
VideoIDs = FetchVideos()[1: ]
VideoLinks = [YoutubePrefix + ID for ID in VideoIDs] #youtube video links

if __name__ == '__main__':
    print('Benvenuto in Google of Calculus I')
    Lessons = GetPlaylistData() #retrieve data of all videos
    Prompt = "inserire l'argomento da cercare "
    Note = '(argomenti multipli vanno separati da una virgola e uno spazio: <arg1>, <arg2>)'
    Prompt += Note + ': '
    Queries = input(Prompt)

    if not Queries == '':
        Queries = Queries.split(', ') #input split to list
        Queries = list(set(Queries)) #remove duplicates for Queries
        for Arg in Queries: #loop for every query
            if not Arg == '':
                Result = SearchData(Arg, Lessons) #retrieving result out of query
                DisplayQuery(Arg, Result) #displaying the single result

    else:
        print('nessuna query inserita')
