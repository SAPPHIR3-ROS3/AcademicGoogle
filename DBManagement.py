from GoogleOfEngineering import *
from hashlib import sha256 as SHA256
from sqlite3 import connect as Connect
from sqlite3 import PARSE_DECLTYPES as TimeStamps
from sys import argv as Args

DOCS =\
 """type
'python DBManagement.py -c' or 'python DBManagement.py --create' to create the file of the database with all the timestamps (faster results)
'python DBManagement.py -v' or 'python DBManagement.py --verify' to verify that that the database is up to date
""" # documentation

CEnd = '\033[0m' # end of coloured text
ErrorText = lambda S: f'\33[31m{S}{CEnd}' #function for errors (red text)
WarningText = lambda S: f'\33[33m{S}{CEnd}' #function for warnings (yellow text)
OKText = lambda S: f'\33[92m{S}{CEnd}' #function for success operations (green text)

def CreateDatabase(): #this function create the database with timestamps from scratch
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
    print('Courses table filled')


    DBShell.execute\
    (
        """
        CREATE TABLE IF NOT EXISTS TimeStamps (
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

    print(OKText('Timestamps table filled'))

def Verify():
    pass #TODO

if __name__ == '__main__':
    if len(Args) == 1:
        print(DOCS)

    else:
        if any(['-c' in Args, '--create' in Args]):
            CreateDatabase()

        if any(['-v' in Args, '--verify' in Args]):
            Verify()