from math import ceil as Ceil
from tkinter import Tk as App
from tkinter import Label as Label
from tkinter import Frame as Page
from tkinter import PhotoImage as Photo
from tkinter import StringVar as VarString
from time import sleep as Sleep

class Uniflix(App): # main class of the app
    def __init__(self,  *args, **kwargs):
        App.__init__(self, *args, **kwargs)
        self.Title = 'Uniflix' #title of the app
        self.Icon = Photo(file = 'Res/SapLogo.png') #logo
        self.iconphoto(True, self.Icon) #window icon
        self.title(self.Title)
        self.geometry('1280x720+0+0')
        #self.wm_state('zoomed')

        self.Screens =\
        {
            Start().Name : Start(self)
        } #all pages of the app

        for Screen in self.Screens.values(): #placing every page with max dimentsion
            Screen.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        self.Raise('Start') #raise the start page
        self.Screens['Start'].Animate() #start the animation of start page

    def Raise(self, Screen = str()): #this function raise the selected frame to the top
        self.Screens[Screen].tkraise()

class Start(Page): #class for the starting animation page
    def __init__(self, Parent = None,  *args, **kwargs):
        self.Parent = Parent #setting parent attribute
        self.Name = 'Start' #setting name
        super().__init__(Parent, *args, **kwargs) #calling the init method of super class page
        self.bg = '#000000' #background
        self.fg = '#E50914' #forground
        self.config(bg = self.bg) #setting the background
        self.Font = lambda x : ('Bebas Neue ', x) #font of the page

        self.Animrames = ['UNIFLIX'[: i] for i in range(1, len('Uniflix') + 1)]
        self.LabelText = VarString() #variable for changing animation text
        self.LabelText.set(self.Animrames[0]) #setting the variable as the initial frame

        self.LogoLebel = Label(self) #creating a logo (letters)
        self.LogoLebel.config(bg = self.bg) #setting tthe background to match the frame
        self.LogoLebel.config(font = self.Font(72)) #setting the font size (72 pt)
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
        for i in range(int(60)): #for loop(1 second) for the start frame to fade in
            StartColor = HexFade(StartColor, Fade, self.fg) #updating the values
            self.LogoLebel.config(fg = StartColor) #updating the forground color
            self.update() #updating the frame
            Sleep(FrameTime) #waitng "a frame"

        #print(self.Name + ' stand time') #debug
        for i in range(int(30)): #for loop (1/2 second) for start frame to stand still
            self.LogoLebel.config(fg = self.fg) #setting the foreground
            self.update() #updating the frame
            Sleep(FrameTime) #waitng "a frame"

        print('writing')
        for Frame in self.Animrames:
            self.LabelText.set(Frame)
            self.update() #updating the frame
            Sleep(FrameTime * 3)

        #print(self.Name + ' fanding out') #debug
        EndColor = self.fg #staring color
        for i in range(int(30)): #for loop (1/2 second) for the logo to fade out
            EndColor = HexFade(EndColor, Fade, self.bg) #updating the value
            self.LogoLebel.config(fg = EndColor) #updating the foregroung color
            self.update() #updating the frame
            Sleep(FrameTime) #waitng "a frame"

class Home(Page): #main class of the main page of the app
    def __init__(self,  *args, **kwargs):
        pass

if __name__ == '__main__':
    App = Uniflix()
    App.mainloop()