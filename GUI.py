from math import ceil as Ceil
from tkinter import Tk as App
from tkinter import Label as Label
from tkinter import Frame as Page
from tkinter import PhotoImage as Photo
from tkinter import StringVar as VarString
from time import sleep as Sleep

class Uniflix(App):
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

class Start(Page):
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
        self.LabelText.set(self.Animrames[0])

        self.LogoLebel = Label(self)
        self.LogoLebel.config(bg = self.bg)
        self.LogoLebel.config(font = self.Font(72))
        self.LogoLebel.config(textvariable = self.LabelText)
        self.LogoLebel.place \
        (
            anchor = 'n',
            relx = 0.5,
            rely = 0.0,
            relwidth = 1,
            relheight = 1
        )

    def Animate(self):
        FPS = 60.0
        FrameTime = 1.0/FPS

        def ExHex(HexCode = ''):
            Red = int(HexCode[1 : 3], 16)
            Green = int(HexCode[3 : 5], 16)
            Blue = int(HexCode[5 :], 16)

            return [Red, Green, Blue]

        def HexFade(HexCode = '', Step = [], HexcodeDest = ''):
            Start = ExHex(HexCode)
            Dest = ExHex(HexcodeDest)

            for i in range(3):
                if Dest[i] - Step[i] < Start[i] < Dest[i] + Step[i]:
                    Start[i] = Dest[i]

                elif Start[i] > Dest[i] and Start[i] + Step[i] > Dest[i]:
                    Start[i] -= Step[i]

                elif Start[i] < Dest[i] and Start[i] + Step[i] < Dest[i]:
                    Start[i] += Step[i]

            return '#' + ''.join([hex(i)[2:] if i > 15 else '0' + hex(i)[2:] for i in Start])

        self.LogoLebel.config(fg = self.bg)
        Fade = [abs(int(Ceil(float(i[0] - i[1]) / 10.0))) for i in zip(ExHex(self.fg), ExHex(self.bg))]

        print(self.Name + ' fanding in')
        StartColor = self.bg
        for i in range(int(60)):
            StartColor = HexFade(StartColor, Fade, self.fg)
            self.LogoLebel.config(fg = StartColor)
            self.update()
            Sleep(FrameTime)

        print(self.Name + ' stand time')
        for i in range(int(30)):
            self.LogoLebel.config(fg = self.fg)
            self.update()
            Sleep(FrameTime)

        print('writing')
        for Frame in self.Animrames:
            self.LabelText.set(Frame)
            self.update()
            Sleep(FrameTime * 3)

        print(self.Name + ' fanding out')
        EndColor = self.fg
        for i in range(int(30)):
            EndColor = HexFade(EndColor, Fade, self.bg)
            self.LogoLebel.config(fg = EndColor)
            self.update()
            Sleep(FrameTime)

class Home(Page):
    def __init__(self,  *args, **kwargs):
        pass

if __name__ == '__main__':
    App = Uniflix()
    App.mainloop()