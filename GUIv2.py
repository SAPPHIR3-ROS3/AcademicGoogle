from os import environ as Env
from PyQt5.QtGui import QIcon as Icon
from PyQt5.QtGui import QPixmap as Image
from PyQt5.QtWidgets import QFont as Font
from PyQt5.QtWidgets import QLabel as Label
from PyQt5.QtWidgets import QGridLayout as Grid
from PyQt5.QtWidgets import QWidget as Widget
from PyQt5.QtWidgets import QApplication as App
from PyQt5.QtWidgets import QMainWindow as MainWin
from PyQt5.QtWidgets.QSizePolicy import Expanding as Rel
from PyQt5.QtWidgets.QSizePolicy import Fixed as Fixed
from sys import argv as Args
from sys import exit as Exit
from urllib.request import urlopen as URL


class Uniflix(MainWin):
    Name = 'UNIFLIX'
    Colors =\
    {
        'bg' : '#000000',
        'lightbg' : '#221f1f',
        'fg' : '#E50914',
        'text' : '#FFFFFF'
    }

    def __init__(self, *args, **kwargs):
        super(Uniflix, self).__init__(*args, **kwargs)
        Data = URL('https://upload.wikimedia.org/wikipedia/en/4/45/Sapienza_University_of_Rome.png').read()
        self.ImageLogo = Image()
        self.ImageLogo.loadFromData(Data)
        self.Logo = Icon()
        self.Logo.addPixmap(self.ImageLogo)
        self.setWindowIcon(self.Logo)
        self.setWindowTitle('Uniflix')
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        self.setGeometry(1000, 100, 500, 320)

        self.Container =
        self.Screens =\
        {
            Start.Name : 0,
            Home.Name : 1
        }

class Start(Widget):
    Name = 'Start' #setting name

    def __init__(self, Parent, *args, **kwargs):
        super().__init__(self, Parent ,*args, **kwargs)
        self.setGeometry(Parent., 50)
        self.Parent = Parent #setting parent attribute
        self.bg = Parent.Colors['bg'] #background
        self.fg = Parent.Colors['fg'] #foreground
        self.setStyleSheet('background-color: ' + self.bg )
        self.Animframes = [Uniflix.Name[: i] for i in range(1, len(Uniflix.Name) + 1)]
        self.Layout = GridLayout()
        self.Logo = Label(self.Animframes[0])
        self.Logo.setStyleSheet('color: ' self.fg)
        self.Logo.setFont(Font('Bebas Neue', 72))
        self.Layout.addWidget(self.Logo, 0, 0)
        self.setLayout(self.Layout)

    def Animate():
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

            return '#' + ''.join([hex(i)[2:] if i > 15 else '0' + hex(i)[2:] for i in Start])

def FixLegacy():
    Env['QT_DEVICE_PIXEL_RATIO'] = '0'
    Env['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    Env['QT_SCREEN_SCALE_FACTORS'] = '1'
    Env['QT_SCALE_FACTOR'] = '1'

if __name__ == '__main__':
    FixLegacy()
    UniflixApp = App(Args)
    Main = Uniflix()
    Main.show()
    Exit(UniflixApp.exec_())