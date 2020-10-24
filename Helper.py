from collections import OrderedDict as OrdDict
try: # check if needed module is installed
    from googleapiclient.discovery import build as Activate
except ImportError: #if not installed python will install it
    from os import system as Shell
    Shell('pip install google-api-python-client')
    try: #try again checking if it's installed
        from googleapiclient.discovery import build as Activate
    except ImportError: #if python can not access the module the script will close
        print('Esegui lo script come admin')
        quit() #closing python

APIKey = 'AIzaSyA-dlBUjVQeuc4a6ZN4RkNUYDFddrVLxrA' #API Key need to perform the research
ID = 'PLAQopGWlIcyZlCmXWE_KvtMi57Mwbyf6C' #Playlist ID
Youtube = Activate('youtube', 'v3', developerKey = APIKey) #activation of youtube service by youtube API Key
Playlist = Youtube.playlistItems() #playlist of videos

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

    return Data

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

    for KeyMatch, ValueMatch in Matches.items(): # loop for every lesson present in the results
        print('\t', KeyMatch) #proper indentation
        for KeyArgument, ValueArgument in ValueMatch.items(): #loop for every argument of every lesson
            print('\t' * 2, KeyArgument, ValueArgument) #proper indentation

if __name__ == '__main__':
    Lessons = UpdateData() #retrieve data
    Prompt = "inserire l'argomento da cercare "
    Note = '(argomenti multipli vanno separati da una virgola e uno spazio: <arg1>, <arg2>)'
    Prompt += Note + ': '
    print('Dati aggiornati')
    Queries = input(Prompt).split(', ') #input split to list

    for Arg in Queries: #loop for every query
        Result = Search(Arg, Lessons) #retrieving result out of query
        DisplayResult(Arg, Result) #displaying the single result
