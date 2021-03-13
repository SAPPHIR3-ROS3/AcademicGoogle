from math import ceil as Ceil
from PIL.Image import new as Gen
from PIL.ImageTk import PhotoImage as PilImg
from tkinter import Tk as App
from tkinter import Button as Button
from tkinter import Label as Label
from tkinter import Frame as Page
from tkinter import PhotoImage as Photo
from tkinter import StringVar as VarString
from time import sleep as Sleep
from urllib.request import urlopen as URL

class Uniflix(App): # main class of the app
    Name = 'UNIFLIX'
    Colors =\
    {
        'bg' : '#000000',
        'fg' : '#E50914',
        'text' : '#FFFFFF'
    }#color of the app

    def __init__(self,  *args, **kwargs):
        App.__init__(self, *args, **kwargs)
        self.Title = 'Uniflix' #title of the app
        Logo = URL('https://upload.wikimedia.org/wikipedia/en/4/45/Sapienza_University_of_Rome.png').read() #raw data of the logo
        self.Icon = PilImg(data = Logo) #logo
        self.iconphoto(True, self.Icon) #window icon
        self.title(self.Title)
        #self.geometry('1280x720+800+0')
        self.wm_state('zoomed')

        self.Screens =\
        {
            Start.Name : Start(self),
            Home.Name : Home(self)
        } #all pages of the app

        for Screen in self.Screens.values(): #placing every page with max dimentsion
            Screen.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
            self.update()

        self.Raise('Start') #raise the start page
        self.Screens['Start'].Animate() #start the animation of start page
        self.Raise('Home')
        self.Screens['Home'].PlaceMoreWidgets()

    def Raise(self, Screen = str()): #this function raise the selected frame to the top
        self.Screens[Screen].tkraise()

    def LogoFont(Dim):
        return ('Bebas Neue ', Dim) #font of the page

class Start(Page): #class for the starting animation page
    Name = 'Start' #setting name

    def __init__(self, Parent = None,  *args, **kwargs):
        super().__init__(Parent, *args, **kwargs) #calling the init method of super class page
        self.Parent = Parent #setting parent attribute
        self.bg = Parent.Colors['bg'] #background
        self.fg = Parent.Colors['fg'] #foreground
        self.config(bg = self.bg) #setting the background

        self.Animrames = [Uniflix.Name[: i] for i in range(1, len(Uniflix.Name) + 1)]
        self.LabelText = VarString() #variable for changing animation text
        self.LabelText.set(self.Animrames[0]) #setting the variable as the initial frame

        self.LogoLebel = Label(self) #creating a logo (letters)
        self.LogoLebel.config(bg = self.bg) #setting tthe background to match the frame
        self.LogoLebel.config(font = Uniflix.LogoFont(72)) #setting the font size (72 pt)
        self.LogoLebel.config(textvariable = self.LabelText) #setting the text of the label as avariable text
        self.LogoLebel.place \
        (
            anchor = 'n',
            relx = 0.5,
            rely = 0.0,
            relwidth = 1,
            relheight = 1
        ) #placing at the center (and full screen) the logo label

    def Animate(self): #this function manage the animation of this page
        FPS = 60.0 #unit for frames in a second
        FrameTime = 1.0/FPS #unit of single frame

        def ExHex(HexCode = ''): #this sub function extract the hex value of the hex string passed
            Red = int(HexCode[1 : 3], 16) #extracting the red channel
            Green = int(HexCode[3 : 5], 16) #extracting the green channel
            Blue = int(HexCode[5 :], 16) #extracting the blue channel

            return [Red, Green, Blue]

        def HexFade(HexCode = '', Step = [], HexcodeDest = ''): #this sub function compute the next hexstring given step(per channel)
            Start = ExHex(HexCode) #extracting the values of the starting color
            Dest = ExHex(HexcodeDest) #extracting the value of the ending color

            for i in range(3): #for loop for every channel of the color
                if Dest[i] - Step[i] < Start[i] < Dest[i] + Step[i]: #check if the starting color channel is in the range dest +- step
                    Start[i] = Dest[i] #setting the start as the end

                elif Start[i] > Dest[i] and Start[i] + Step[i] > Dest[i]: #check if the step is allowed
                    Start[i] -= Step[i] #updating the starting color

                elif Start[i] < Dest[i] and Start[i] + Step[i] < Dest[i]: #check if the step is allowed
                    Start[i] += Step[i] #updating the starting color

            return '#' + ''.join([hex(i)[2:] if i > 15 else '0' + hex(i)[2:] for i in Start]) #formatting the values a hex string

        self.LogoLebel.config(fg = self.bg) #setting the background of the label to match the background of the frame
        Fade = [abs(int(Ceil(float(i[0] - i[1]) / 10.0))) for i in zip(ExHex(self.fg), ExHex(self.bg))] #computing the step for every channel

        #print(self.Name + ' fanding in') #debug
        StartColor = self.bg #setting the starting color
        self.LogoLebel.config(fg = StartColor)
        for i in range(int(60)): #for loop(1 second) for the start frame to fade in
            StartColor = HexFade(StartColor, Fade, self.fg) #updating the values
            self.LogoLebel.config(fg = StartColor) #updating the forground color
            self.update() #updating the frame
            Sleep(FrameTime) #waitng "a frame"

        #print(self.Name + ' stand time') #debug
        for i in range(int(10)): #for loop (1/4 second) for start frame to stand still
            self.LogoLebel.config(fg = self.fg) #setting the foreground
            self.update() #updating the frame
            Sleep(FrameTime) #waitng "a frame"

        #print('writing')
        for Frame in self.Animrames:
            self.LabelText.set(Frame)
            self.update() #updating the frame
            Sleep(FrameTime * 3)

        #print(self.Name + ' fanding out') #debug
        EndColor = self.fg #staring color
        self.LogoLebel.config(fg = EndColor)
        for i in range(int(30)): #for loop (1/2 second) for the logo to fade out
            EndColor = HexFade(EndColor, Fade, self.bg) #updating the value
            self.LogoLebel.config(fg = EndColor) #updating the foregroung color
            self.update() #updating the frame
            Sleep(FrameTime) #waitng "a frame"

class NavigationBar(Page): #class of top navigation bar (menu button, logo, search button)
    Name = 'NavigationBar'

    def __init__(self, Parent, *args, **kwargs):
        super().__init__(Parent, *args, **kwargs) #super class constructor method
        self.Parent = Parent #setting the parent of the bar
        self.bg = Uniflix.Colors['bg'] #setting background color as attribute
        self.fg = Uniflix.Colors['fg'] #setting foreground color as attribute
        self.config(bg = self.bg) #changing the background color

        self.Menu = Button(self) #generating a button to trigger side menu
        self.Menu.config(borderwidth = 0) #setting the button with no border
        self.Menu.place \
        (
            anchor = 'nw',
            relx = 0,
            rely = 0
        ) #placing the sidemenu button top left

        self.Search = Button(self) #generating the button of the search
        self.Search.config(borderwidth = 0) #setting the button with no border
        self.Search.place \
        (
            anchor = 'ne',
            relx = 1,
            rely = 0
        ) #placing the search button top right

    def PlaceMoreWidgets(self): #this method generate and place additional widgets that can not be placed or completely used in the costructor
        self.MenuIMG = PilImg(Gen('RGB', (self.winfo_height() - 10, self.winfo_height() - 10), (255, 0, 0))) #generating a square image as bg of the button #temporary
        self.Menu.config(image = self.MenuIMG) #setting the image as button background

        self.LogoLabel = Label(self) #generating the logo
        self.LogoLabel.config(bg = self.bg) #setting the background to match with the frame
        self.LogoLabel.config(fg = self.fg) #setting the foreground to match with the frame
        self.LogoLabel.config(font = Uniflix.LogoFont(36)) #setting the font for the logo and the size
        self.LogoLabel.config(text = Uniflix.Name) #setting the text of the logo as the name of the app
        self.LogoLabel.place \
        (
            anchor = 'nw',
            x = self.MenuIMG.width() + 10,
            rely = 0,
            relheight = 1
        ) #placing the logo right after the menu button

        self.SearchIMG = PilImg(Gen('RGB',(self.winfo_height() - 10, self.winfo_height() - 10), (0, 0, 255))) #generating a square image as bg of the button #temporary
        self.Search.config(image = self.SearchIMG) #setting the image as button background

class Home(Page): #main class of the main page of the app
    Name = 'Home' #setting name
    def __init__(self, Parent = None,  *args, **kwargs):
        super().__init__(Parent, *args, **kwargs) #calling the init method of super class page
        self.Parent = Parent #setting parent attribute
        self.bg = Parent.Colors['bg'] #background
        self.config(bg = self.bg)
        self.fg = Parent.Colors['fg'] #foreground
        self.Text = Parent.Colors['text'] #text color

        self.NavBar = NavigationBar(self) #genrating navigation bar (and its widget)
        self.NavBar.place \
        (
            anchor = 'n',
            relx = 0.5,
            rely = 0,
            relwidth = 1,
            relheight = 0.06
        ) #placing the bar on top

    def PlaceMoreWidgets(self): #this function manage all the additional widgets of the page
        self.Parent.update() #updating the window
        self.NavBar.PlaceMoreWidgets() #placing the additiona widget of NavBar
        self.Parent.update() #updating the window



if __name__ == '__main__':
    App = Uniflix()
    App.mainloop()
