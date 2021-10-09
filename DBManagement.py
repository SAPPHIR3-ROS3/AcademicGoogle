from collections import OrderedDict as OrdDict
from googleapiclient.discovery import build as Activate
from hashlib import sha256 as SHA256
from os.path import exists as Exists
from re import finditer
from sqlite3 import connect as Connect
from sqlite3 import PARSE_DECLTYPES as TimeStamps
from sys import argv as Args

DOCS =\
 """type
'python DBManagement.py -c' or 'python DBManagement.py --create' to create the file of the database with all the timestamps (faster results)
'python DBManagement.py -v' or 'python DBManagement.py --verify' to verify that that the database is up to date
""" # documentation

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

CEnd = '\033[0m' # end of coloured text
ErrorText = lambda S: f'\33[31m{S}{CEnd}' #function for errors (red text)
WarningText = lambda S: f'\33[33m{S}{CEnd}' #function for warnings (yellow text)
OKText = lambda S: f'\33[92m{S}{CEnd}' #function for success operations (green text)

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

def CreateDatabase(): #this function create the database with timestamps from scratch
    Database = Connect('Data.db', detect_types = TimeStamps) # database file creation
    DBShell = Database.cursor() # shell to run queries
    DBShell.execute\
    (
        """
        CREATE TABLE IF NOT EXISTS Courses (
        PlaylistID text PRIMARY KEY NOT NULL,
        CourseName text NOT NULL
        )
        """
    ) # reference table of playlist of the courses

    print(OKText('Courses table created'))
    for Course, PLID in Courses.items(): # loop for filling the courses table
        DBShell.execute('INSERT INTO Courses VALUES (:PLID, :CourseName)', {'PLID' : PLID, 'CourseName' : Course}) #secured execution of the query to insert value from
    print(OKText('Courses table filled'))


    DBShell.execute\
    (
        """
        CREATE TABLE IF NOT EXISTS Timestamps (
        TimestampID text PRIMARY KEY NOT NULL,
        Course text NOT NULL,
        VideoLink text NOT NULL,
        VideoTitle text NOT NULL,
        StartTimestamp text NOT NULL,
        EndTimestamp text NOT NULL,
        TimestampDescription text NOT NULL
        )
        """
    ) # table with all timestamps of all courses

    print(OKText('Timestamps table created'))

    Database.commit() #database update

    for Course, PLID in Courses.items(): # loop for every course in the courses dictionary
        VideoIDs = GetVideoIDs(PLID) # retraial of all videos id of a specified course(playlist)

        for VideoID in VideoIDs: # for loop for every video lesson in playlist course
            Video = GetVideoData(VideoID) # retriving video information

            for Line in Video['Description']: # for loop for every timestamp in the video lesson
                Parameters = dict() # parameters dictionary for the insertion query
                Parameters['Link'] = Video['Link']
                Parameters['Course'] = Course
                Parameters['Title'] = Video['Title']
                Parameters['StartTimestamp'] = Line[1]
                Parameters['EndTimestamp'] = Line[2]
                Parameters['TimestampDescription'] = Line[0].replace(':',  '║').replace('-', ' ') # replacing "problematic" character
                Parameters['TimestampID'] = SHA256(str(Video['Link']+Video['Title']+Line[1]+Line[2]+Line[0]).encode()).hexdigest() # creation of a unique sha256 as Primary Key of the table
                #print(f'timestamp {Parameters["TimestampID"]} marked at video {VideoID} of {Course}')
                DBShell.execute('INSERT INTO Timestamps VALUES (:TimestampID, :Course, :Link, :Title, :StartTimestamp, :EndTimestamp, :TimestampDescription)', Parameters) #values insertion in the table
                Database.commit() #database update
    Database.close() #closing connection of the database
    print(OKText('Timestamps table filled'))

def Verify():
    pass #TODO

def SearchInDatabase(Queries = None): # this fucntion query in the database to find relevant result
    #print(f'searching {", ".join(Queries)} in the database')
    if Exists('Data.db') and Queries is not None: # check if the parameter is valid and if databse exists
        if isinstance(Queries, str): # check if queries is a single parameters
            Queries = [Queries] # format properly the query

        if isinstance(Queries, list): # check if the queries are a list (loop porpuses)
            Database = Connect('Data.db', detect_types = TimeStamps) # database file creation
            DBShell = Database.cursor() # shell to run queries
            Results = OrdDict() # ordered dictionary of the matches in the database

            for Query in Queries: # for loop for every query in the list
                Selection = """SELECT
                Course,
                VideoTitle,
                StartTimestamp,
                EndTimestamp,
                TimestampDescription,
                VideoLink
                FROM Timestamps WHERE TimestampDescription LIKE '%'||:Query||'%'
                ORDER BY Course"""
                DBShell.execute(Selection, {'Query' : Query}) # query in database to find result ordered by relevance and chronological order
                QueryResult = DBShell.fetchall() # saving the result
                QueryKeys = ['Course', 'VideoTitle', 'StartTimestamp', 'EndTimestamp', 'TimestampDescription', 'VideoLink'] # keys of the dictionary (not to deal with indexes)
                Results[Query] = [{Key : Value for Key, Value in zip(QueryKeys, Match)} for Match in QueryResult] # transforming result in a better format
                # dictionary of queries as keys and an ordered list of dictionaries which rappresents a match as values

            return Results

if __name__ == '__main__':
    if len(Args) == 1:
        print(DOCS)

    else:
        if any(['-c' in Args, '--create' in Args]):
            CreateDatabase()

        if any(['-v' in Args, '--verify' in Args]):
            Verify()