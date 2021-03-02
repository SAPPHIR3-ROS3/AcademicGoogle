from collections import OrderedDict as OrdDict
from googleapiclient.discovery import build as Activate
from re import findall

APIKey = 'AIzaSyA-dlBUjVQeuc4a6ZN4RkNUYDFddrVLxrA' #API Key need to perform the research
YoutubeAPI = Activate('youtube', 'v3', developerKey = APIKey) #activation of youtube service by youtube API Key
Playlist = YoutubeAPI.playlistItems() #playlist of videos
YoutubePrefix = 'https://www.youtube.com/watch?v='

Courses =\
{
'Analisi Matematica I' : 'PLAQopGWlIcyZlCmXWE_KvtMi57Mwbyf6C',
'Informatica I: Python' : 'PLAQopGWlIcyaYO89pmFViY4z_y8lj2IQA',
'Informatica I: Modelli' : 'PLAQopGWlIcyalkb2baN9mnotsdBm5Vbkc',
'Fisica 1-2' : 'PLAQopGWlIcyYqImhBYHb6ffUiLx6HyVAv',
'Sistemi di Calcolo' : 'PLAQopGWlIcybT12h7fjVvlGAeSqOKDnTA',
'Robotics I' : 'PLAQopGWlIcyaqDBW1zSKx7lHfVcOmWSWt',
'Robotics II' : 'PLAQopGWlIcya6LnIF83QlJTqvpYmJXnDm',
'Tecniche di Programmazione' : 'PLAQopGWlIcybv3YLRHGS4yZR00X3RvSBm',
'Ricerca Operativa' : 'PLAQopGWlIcyZankm1hHCSOdBilSGC3Svg',
'Basi di Dati' : 'PLAQopGWlIcyZ7CN1sefdnCusfoodLP931',
'Statistica' : 'PLAQopGWlIcyYS5uAXk6M6lD2uXW2_dnCG',
'Web Information Retraial' : 'PLAQopGWlIcya-9yzQ8c8UtPOuCv0mFZkr'
}

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
    Duration = Duration.replace('H', ':').replace('M', ':') #formatting correctly the duration as timestamps
    DescriptionList = [Line.strip() for Line in Video['snippet']['description'].split('\n')] #splitting the description in lines
    RawDescription = Video['snippet']['description']
    Timestamps = r'(\d{1,2}:\d{2}:\d{2}|\d{2}:\d{2})\s(.+)'
    ####r'(\d{2}:\d{2}(:\d{2})?)\s(.+)' to use in the description
    # for Line in range(len(DescriptionList)): #for loop for every line of the description
    #     if not Line == len(DescriptionList) - 1: #check if is not the last
    #         Value = [DescriptionList[Line][0], DescriptionList[Line + 1][0]] #timestamps
    #     else: #last line
    #         Value = [DescriptionList[Line][0], Duration] #timestamps
    #
    #     Key = ' '.join(DescriptionList[Line][1:]) #argument as string
    #     Description[Key] = Value #argument title (key) timestamps (value)

    Description = [list(Line)[:: - 1] for Line in findall(Timestamps, str(RawDescription))]

    VideoMetaData =\
    {
        'Link' : YoutubePrefix + ID,
        'Title' : Title, #title of the video (string)
        'Duration' :Duration, # duration HH:MM:SS (string)
        'Description' : Description # description (string : list of timestamps)(OrdDict)
    }

    return VideoMetaData

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

if __name__ == '__main__':
    PLID = Courses['Web Information Retraial']

    VideoIDs = GetVideoIDs(PLID)

    for ID in VideoIDs:
        Video = GetVideoData(ID)

        for Att in Video:
            if Att == 'Description':
                for i in Video[Att]:
                    #print(i,  ':', Video[Att][i])
                    #print(i)
                    print(i[0], ':', i[1])
            else:
                print(Att, ':', Video[Att])
            # print(Att, ':', Video[Att])
        print()
