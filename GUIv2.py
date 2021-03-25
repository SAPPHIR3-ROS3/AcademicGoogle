from math import ceil as Ceil
from os import environ as Env
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon as Icon
from PyQt5.QtGui import QPixmap as Image
from PyQt5.QtGui import QFont as Font
from PyQt5.QtWidgets import QLabel as Label
from PyQt5.QtWidgets import QGridLayout as Grid
from PyQt5.QtWidgets import QVBoxLayout as VLayout
from PyQt5.QtWidgets import QStackedWidget as Container
from PyQt5.QtWidgets import QWidget as Widget
from PyQt5.QtWidgets import QApplication as App
from PyQt5.QtWidgets import QMainWindow as MainWin
#from PyQt5.QtWidgets.QSizePolicy import Expanding as Rel
#from PyQt5.QtWidgets.QSizePolicy import Fixed as Fixed
from sys import argv as Args
from sys import exit as Exit
from time import sleep as Sleep
from urllib.request import urlopen as URL


class Uniflix(Widget):
    Name = 'UNIFLIX'
    Colors =\
    {
        'bg' : '#000000',
        'lightbg' : '#221F1F',
        'fg' : '#E50914',
        'text' : '#FFFFFF'
    }

    def __init__(self, *args, **kwargs):
        Widget.__init__(self,*args, **kwargs)
        Data = URL('https://upload.wikimedia.org/wikipedia/en/4/45/Sapienza_University_of_Rome.png').read()
        self.ImageLogo = Image()
        self.ImageLogo.loadFromData(Data)
        self.Logo = Icon()
        self.Logo.addPixmap(self.ImageLogo)
        self.setWindowIcon(self.Logo)
        self.setWindowTitle('Uniflix')
        self.PageLayout = VLayout()
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        self.setGeometry(1000, 100, 500, 320)

        self.setStyleSheet('background-color : ' + self.Colors['bg'])

        self.Screen =\
        {
            Start.Name : {'index' : 0, 'Page' : Start()}
        }

        self.Pages = Container()
        self.Pages.addWidget(self.Screen['Start']['Page'])
        self.Pages.setCurrentIndex(self.Screen['Start']['index'])
        self.PageLayout.addWidget(self.Pages)
        self.setLayout(self.PageLayout)
        self.show()

    def OpeningApp(self):
        self.Screen['Start']['Page'].Animate()

class Start(Widget):
    Name = 'Start' #setting name

    def __init__(self,*args, **kwargs):
        Widget.__init__(self,*args, **kwargs)
        #self.Parent = Parent #setting parent attribute
        self.bg = Uniflix.Colors['bg'] #background
        self.fg = Uniflix.Colors['fg'] #foreground
        self.Layout = Grid()
        self.setStyleSheet('background-color : ' +  self.bg)
        self.setLayout(self.Layout)

        self.Animframes = [Uniflix.Name[: i] for i in range(1, len(Uniflix.Name) + 1)]
        self.Logo = Label(self.Animframes[0])
        self.Logo.setStyleSheet('color : ' + self.fg)
        self.Logo.setFont(Font('Bebas Neue', 72))
        self.Logo.setAlignment(Qt.AlignCenter)

        self.Layout.addWidget(self.Logo, 0, 0)
        self.setLayout(self.Layout)

def FixLegacy(): #this function fix some warning of Pyqt5 that use legacy methods and functions
    Env['QT_DEVICE_PIXEL_RATIO'] = '0' #disable the ratio for specific device
    Env['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1' #enable the auto scaling factor for every screen
    Env['QT_SCREEN_SCALE_FACTORS'] = '1' # enable the manual scaling factors for a platform
    Env['QT_SCALE_FACTOR'] = '1' # enable normal scale factor

if __name__ == '__main__':
    FixLegacy()
    print('fixed legacy')
    UniflixApp = App(Args)
    Main = Uniflix()
    print('main class created')
    #Main.OpeningApp()
    Exit(UniflixApp.exec_())