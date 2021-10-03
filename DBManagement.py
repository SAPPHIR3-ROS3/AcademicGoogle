from GoogleOfEngineering import *
from hashlib import sha256 as SHA256
from sqlite3 import connect as Connect
from sqlite3 import PARSE_DECLTYPES as TimeStamps
from sys import argv as Args

DOCS = """type
'python DBManagement.py -c' or 'python DBManagement.py --create' to create the file of the database with all the timestamps (faster results)
'python DBManagement.py -v' or 'python DBManagement.py --verify' to verify that that the database is up to date"""

def CreateDatabase():
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

    Database = Connect('Data.db', detect_types = TimeStamps)
    with Database:
        DBShell = Database.cursor()
        DBShell.execute\
        (
            """
            CREATE TABLE IF NOT EXISTS Courses (
            PlaylistID text PRIMARY KEY NOT NULL,
            CourseName text NOT NULL
            )
            """
        )
        print('Courses table created')

        for Course, PLID in Courses.items():
            DBShell.execute('INSERT INTO Courses VALUES (:PLID, :CourseName)', {'PLID' : PLID, 'CourseName' : Course})

        print('Courses table filled')

        for Course in Courses.keys():
            Course = Course.replace(' ', '').replace(':', '').replace('-', '║')
            Command = f'CREATE TABLE IF NOT EXISTS {Course}' + """(
            TimestampID text PRIMARY KEY NOT NULL,
            VideoLink text NOT NULL,
            VideoTitle text NOT NULL,
            StartTimestamp text NOT NULL,
            EndTimestamp text NOT NULL,
            TimestampDescription text NOT NULL
            )
            """
            DBShell.execute(Command)

            print(f'{Course} table created')

            VideoIDs = GetVideoIDs(PLID)

            for VideoID in VideoIDs:
                Video = GetVideoData(VideoID)
                print(f'timestamps for {VideoID}')

                for Line in Video['Description']:
                    Parameters = dict()
                    Parameters['Link'] = Video['Link']
                    Parameters['Title'] = Video['Title']
                    Parameters['StartTimestamp'] = Line[1]
                    Parameters['EndTimestamp'] = Line[2]
                    Parameters['TimestampDescription'] = Line[0].replace(':',  '║').replace('-', ' ')
                    Parameters['TimestampID'] = SHA256(str(Video['Link']+Video['Title']+Line[1]+Line[2]+Line[0]).encode()).hexdigest()
                    DBShell.execute(f'INSERT INTO {Course} '+'VALUES (:TimestampID, :Link, :Title, :StartTimestamp, :EndTimestamp, :TimestampDescription)', Parameters)

def Verify():
    pass

if __name__ == '__main__':
    if len(Args) == 1:
        print(DOCS)

    else:
        if any(['-c' in Args, '--create' in Args]):
            CreateDatabase()

        if any(['-v' in Args, '--verify' in Args]):
            Verify()