from collections import OrderedDict as OrdDict
from googleapiclient.discovery import build as Activate
from hashlib import sha256 as SHA256
from json import load as Load
from json import dumps as Dumps
from os import remove as Remove
from os.path import exists as Exists
from re import finditer
from sqlite3 import connect as Connect
from sqlite3 import PARSE_DECLTYPES as TimeStamps

CEnd = '\033[0m' # end of coloured text
ErrorText = lambda S: f'\33[31m{S}{CEnd}' # function for errors (red text)
WarningText = lambda S: f'\33[33m{S}{CEnd}' # function for warnings (yellow text)
OKText = lambda S: f'\33[92m{S}{CEnd}' # function for success operations (green text)

APIKey = 'AIzaSyA-dlBUjVQeuc4a6ZN4RkNUYDFddrVLxrA' #API Key need to perform the research
YoutubeAPI = Activate('youtube', 'v3', developerKey = APIKey) #activation of youtube service by youtube API Key
Playlist = YoutubeAPI.playlistItems() #playlist of videos
YoutubePrefix = 'https://youtu.be/' # youtube short link prefix
CompatibilityThreshold = 20 # if imcompatible part is greater then this the element will be conidered incompatible

def GetPlaylistID(url = ''): # extract the playlist id from the url
    return url.replace('https://www.youtube.com/playlist?list=', '')

if not Exists('Courses.json'):
    print(ErrorText('sembra che il file Courses.json non esista'))
    print(WarningText('il file è necessario per la creazione del database, ne verrà creato uno con una playlist di default (può essere rimosso dopo)'))
    with open('Courses.json', 'w') as JSON: JSON.write(Dumps({"Analisi Matematica I" : "PLAQopGWlIcyZlCmXWE_KvtMi57Mwbyf6C"}))

with open('Courses.json') as Json: # load the courses file
    Courses = {course : GetPlaylistID(playlist) for course, playlist in Load(Json).items()} # preloading the courses

def GetPlaylistPages(PlaylistID = ''): # playlist pages retrieval
    Pages = [None] #token IDs of the playlist pages
    i = 0 #page counter

    while True: #loop through all the pages of the playlist until there is no next page
        Request = Playlist.list(part='snippet', playlistId = PlaylistID, maxResults = 50, pageToken = Pages[i]) #specifing page
        Response = Request.execute() #effective request execution
        NextPageToken = Response.get('nextPageToken') #getting the next page token to get the next page

        if not NextPageToken: # check if token is None
            break

        Pages.append(NextPageToken) # add the token to token list
        i += 1 #increase of page counter

    return Pages

def GetVideoIDs(PlaylistID = ''): #this function get youtube ids
    Pages = GetPlaylistPages(PlaylistID) # get the page tonkes
    VideosID = []
    
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
    ChannelTitle = Video['snippet']['channelTitle'] # channel title
    Tags = '\t'.join(Video['snippet']['tags']) # hashtags (unused for now)
    Duration = Video['contentDetails']['duration'][2 : - 1] #removing useless part of duration
    Duration = Duration.replace('H', ':').replace('M', ':') #formatting correctly the duration of timestamp
    Duration = ':'.join([Part if len(Part) > 1 else '0' + Part for Part in Duration.split(':')]) #setting proper length of timestamps segment
    RawDescription = str(Video['snippet']['description']) # description
    Timestamps = r'(?=(\d{1,2}:\d{2}:\d{2}|\d{2}:\d{2})\s(.+)\n?(\d{1,2}:\d{2}:\d{2}|\d{2}:\d{2})?)' #regex to find start timestamp, argument and end timestamps
    Description = [[Group if not Group == None else Duration for Group in Line.groups()] for Line in finditer(Timestamps, RawDescription)]
    #formatting in a list properly the matches (timestamps and argument)
    Description = [(Group[1], Group[0], Group[2]) for Group in Description][: - 1] #correcting the order of sublist and removing last(duplicate)

    VideoMetaData =\
    {
        'Link' : YoutubePrefix + ID,
        'ChannelTitle' : ChannelTitle,
        'Title' : Title, # title of the video (string)
        'Tags' : Tags,
        'Duration' :Duration, # duration HH:MM:SS (string)
        'Description' : Description # description (string : list of timestamps)(OrdDict)
    } # video dictionary

    return VideoMetaData

def HasTimestamps(VideoID = ''): # this function check if the video has some timestamps
    Video = GetVideoData(VideoID) # data acquisition
    return True if len(Video['Description']) > 1 else False

def HowCompatible(PlaylistID = ''): # this function calcultate the compatibility percentage
    VideoIDs = GetVideoIDs(PlaylistID) # get the videos list
    Playlist = [HasTimestamps(ID) for ID in VideoIDs] # check how many videos have timestamps
    
    return int(round(Playlist.count(True)/len(Playlist), 2) * 100)

def CheckCoursesCompatibility(CoursesDictionary = dict()): # this function check and remove incompatible courses
    for Course, PLID in CoursesDictionary.copy().items(): # loop to check the compatibility of every playlist 
        print(OKText(f'Verifying {Course} ({PLID})'))
        Compatibility = HowCompatible(PLID) # check the compatibility of the playlist
        if Compatibility < (100 - CompatibilityThreshold): # check if the playlist doesn't surpass the compatibility threshold
            print(WarningText('incompatible, it will be skipped'))
            CoursesDictionary.pop(Course) # the playlist is considered not compatible enough therefore is removed 
        else:
            print(OKText(f'{Compatibility}% compatible'))

    return CoursesDictionary

def FetchPlaylist(Course, PLID): # this function insert the timestamps nel databases
    Database = Connect('Data.db', detect_types = TimeStamps) # database file creation
    DBShell = Database.cursor() # shell to run queries
    VideoIDs = GetVideoIDs(PLID) # retraial of all videos id of a specified course(playlist)

    for VideoID in VideoIDs: # for loop for every video lesson in playlist course
        Video = GetVideoData(VideoID) # retriving video information

        for Line in Video['Description']: # for loop for every timestamp in the video lesson
            Parameters = dict() # parameters dictionary for the insertion query
            Parameters['Link'] = Video['Link']
            Parameters['Course'] = Course
            Parameters['ChannelTitle'] = Video['ChannelTitle']
            # Parameters['Tags'] = Video['Tags'] # not available at the moment (possible future implementation)
            Parameters['Title'] = Video['Title']
            Parameters['StartTimestamp'] = Line[1]
            Parameters['EndTimestamp'] = Line[2]
            Parameters['TimestampDescription'] = Line[0].replace(':',  '║').replace('-', ' ') # replacing "problematic" character
            Parameters['TimestampID'] = SHA256(str(Video['Link']+Video['ChannelTitle']+Video['Title']+Line[1]+Line[2]+Line[0]).encode()).hexdigest() # creation of a unique sha256 as Primary Key of the table
            # print(f'timestamp {Parameters["TimestampID"]} marked at video {VideoID} of {Course}') # debug
            DBShell.execute('INSERT INTO Timestamps VALUES (:TimestampID, :Course, :ChannelTitle, :Link, :Title, :StartTimestamp, :EndTimestamp, :TimestampDescription)', Parameters) # values insertion in the table
            Database.commit() # database update
    
    Database.close() # closing connection of the database
    print(OKText(f'{Course} ({PLID}) fetched'))

def CreateDatabase(): # this function create the database with timestamps from scratch
    global Courses
    if Exists('Data.db'): Remove('Data.db') # when creating the database, the file might already exists so it's removed to avoid error
    Database = Connect('Data.db', detect_types = TimeStamps) # database file creation
    DBShell = Database.cursor() # shell to run queries
    DBShell.execute\
    (
        """
        CREATE TABLE Courses (
        PlaylistID text PRIMARY KEY NOT NULL,
        CourseName text NOT NULL
        )
        """
    ) # reference table of playlist of the courses

    print(OKText('Courses table created'))

    Courses = CheckCoursesCompatibility(Courses)

    for Course, PLID in Courses.items(): # loop for filling the courses table
        DBShell.execute('INSERT INTO Courses VALUES (:PLID, :CourseName)', {'PLID' : GetPlaylistID(PLID), 'CourseName' : Course}) #secured execution of the query to insert value from
    
    print(OKText('Courses table filled'))

    DBShell.execute\
    (
        """
        CREATE TABLE IF NOT EXISTS Timestamps (
        TimestampID text PRIMARY KEY NOT NULL,
        Course text NOT NULL,
        ChannelTitle text NOT NULL,
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
        FetchPlaylist(Course, PLID)

    print(OKText('Timestamps table filled'))

def Verify(): # this function verify that the database is up to date
    with open('Courses.json') as Json: # open the json file with courses
        LocalCourses = Load(Json) # load the file as a json
    Query = "SELECT CourseName, PLID FROM Courses" # query to find if the course has been fetched
    Database = Connect('Data.db', detect_types = TimeStamps) # database file creation
    DBShell = Database.cursor() # shell to run queries
    DBShell.execute(Query) # query is executed
    CurrentCourses = {Match[0] : Match[1] for Match in DBShell.fetchall()} # the courses in the database are fetched in the dictionary
    NewCourses = dict() # courses in the local file but not in the database

    for Course in LocalCourses: # check if the local courses are the same of the database
        if not Course in CurrentCourses.keys() or not CurrentCourses[Course] == LocalCourses[Course]: # check if there is the same name and same key in the database and iin the file
            NewCourses[Course] = LocalCourses[Course] # the course is in the local gile but not in the database

    NewCourses = CheckCoursesCompatibility(NewCourses) # remove incompatible playlist

    for Course, PLID in NewCourses.items(): # loop for every course in the courses dictionary
        FetchPlaylist(Course, PLID) # insert the timestamps of the playlist in the database

def Delete(): # this function delete the database file to reset the program
    if Exists('Data.db'): # check if the file exists
        deletion = input(WarningText('Do you want to delete the database?<y/n>'))[0].lower() # ask for confirmation
        if deletion == 'y': # deletion confimed
            Remove('Data.db') # file is removed
            print(OKText('Data.db deleted, database is now non-existent'))
        else:
            print(OKText('Deletion cancelled, the database is untouched'))

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
                ChannelTitle,
                VideoTitle,
                StartTimestamp,
                EndTimestamp,
                TimestampDescription,
                VideoLink
                FROM Timestamps 
                WHERE TimestampDescription LIKE '%'||:Query||'%'
                OR VideoTitle LIKE '%'||:Query||'%'
                ORDER BY Course"""
                DBShell.execute(Selection, {'Query' : Query}) # query in database to find result ordered by relevance and chronological order
                QueryResult = DBShell.fetchall() # saving the result
                QueryKeys = ['Course', 'ChannelTitle', 'VideoTitle', 'StartTimestamp', 'EndTimestamp', 'TimestampDescription', 'VideoLink'] # keys of the dictionary (not to deal with indexes)
                Results[Query] = [{Key : Value for Key, Value in zip(QueryKeys, Match)} for Match in QueryResult] # transforming result in a better format
                # dictionary of queries as keys and an ordered list of dictionaries which rappresents a match as values

            return Results
