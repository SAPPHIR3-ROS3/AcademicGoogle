from collections import OrderedDict as OrdDict
from googleapiclient.discovery import build as Activate

APIKey = 'AIzaSyA-dlBUjVQeuc4a6ZN4RkNUYDFddrVLxrA' #API Key need to perform the research
YoutubeAPI = Activate('youtube', 'v3', developerKey = APIKey) #activation of youtube service by youtube API Key
YoutubePrefix = 'https://www.youtube.com/watch?v='

Courses = {'Analisi Matematica I': 'PLAQopGWlIcyZlCmXWE_KvtMi57Mwbyf6C'}



def FetchPages(PlaylistID = ''): #this function retrieve all the "pages" of video
    Tokens = [None] #token IDs of the palylist pages
    i = 0 #page counter

    while True: #loop through all the pages of the playlist until there is no next page
        Request = Playlist.list(part='snippet', playlistId = PlaylistID, maxResults = 50, pageToken = Tokens[i]) #specifing page
        Response = Request.execute() #effective request execution
        NextPageToken = Response.get('nextPageToken') #getting the next page token to get the next page

        if not NextPageToken: # check if token is None
            break

        Tokens.append(NextPageToken) # add the token to token list
        i += 1 #increase of page counter

    return Tokens

def FetchVideos(PlaylistID = ''): #this function get youtube ids
    Pages = FetchPages(PlaylistID) #fatching all the pages of a playlist
    VideosID = []

    for Page in Pages: #loop for every page of results
        Videos = Playlist.list(part='contentDetails', playlistId = ID, maxResults = 50, pageToken = Page) #setting the page
        Videos = Videos.execute() #request execution

        for Video in Videos['items']: #loop for every video of the playlist
            VideosID.append(Video['contentDetails']['videoId']) #append video link

    return VideosID

def GetPlaylistData(): #retrive all the data of the videos
    PlaylistData = [] #list for all the videos

    for ID in VideoIDs: #for loop for every video
        PlaylistData.append(GetVideoData(ID)) #appending the data for every video

    return PlaylistData

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

def DataToDict(Tokens, Start =''):
    Data = OrdDict()  #raw data
    Index = Start #index of lesson

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

