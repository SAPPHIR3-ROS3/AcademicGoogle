from os import name as SysName
from os import system as Sys
from subprocess import check_output as Shell

Dependencies = {'googleAPI' : 'googleAPI'} # dependencies need to run the program

CEnd = '\033[0m' # end of coloured text
ErrorText = lambda S: f'\33[31m{S}{CEnd}' # function for errors (red text)
WarningText = lambda S: f'\33[33m{S}{CEnd}' # function for warnings (yellow text)
OKText = lambda S: f'\33[92m{S}{CEnd}' # function for success operations (green text)

def IsAdmin(): # this function check if the user is admin
    try: # if the user is on UNIX-like systems
        from os import getuid as GetUID
        Admin = (GetUID() == 0) # the SUDO user on UNIX systems is always 0
    except AttributeError: # if the user is on windows
        from ctypes import windll as WinDLL
        Admin = WinDLL.shell32.IsUserAnAdmin() != 0 # the windows API automatic checking
    return Admin

def CheckDependencies(): # function to check all the needd dependencies in the script
    ModulesList= [i.decode() for i in Shell('pip list', shell = True).split()][4 :] # from the list generated from pip list it generates a list of the installed modules
    Modules = [ModulesList[i] for i in range(len(ModulesList)) if i % 2 == 0] # extract modules name
    Versions = [ModulesList[i] for i in range(len(ModulesList)) if i % 2 == 1] # extract the version of the modules
    ModuleString = ' '.join([i.replace('-', '') + '==' + j for i,j in zip(Modules,Versions)]) # format properly the modules and their versions

    MissingModules = [Dependency for Dependency in Dependencies if Dependencies[Dependency] not in ModuleString] # check if the needed dependencies are installed

    return MissingModules

if __name__ == '__main__':
    ModulesToIstall = CheckDependencies()
    Sys('cls' if  SysName =='nt' else 'clear')

    if IsAdmin():
        if len(ModulesToIstall) > 0 :
            print(WarningText('you need to install the following modules:'))

            for Module in ModulesToIstall:
                print(ErrorText(Module))

            UInput = input('do you want to autoinstall them? <y/n> ')
            Commands = ['pip install ' + Module for Module in ModulesToIstall]

            if UInput.lower() == 'y':
                for Command in Commands:
                    Shell(Command, shell = True)

            elif UInput.lower() == 'n':
                print(WarningText('copy and paste the following commands in cmd/powershell/terminal'))

                for Command in Commands:
                    print(Command)

            else:
                print(ErrorText('invalid imput'))
                print(ErrorText('exiting'))
                quit()

        else:
            print(OKText('All set you are ready to start'))

        print('creating the database the operation may require a few minutes (do not close this window)')
        Shell('python DBManagement.py -c', shell = True)

    else:
        print(ErrorText('you do NOT have Admin privileges please restart this script as Admin'))

    input('press enter key to exit')
