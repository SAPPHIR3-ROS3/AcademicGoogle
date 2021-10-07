from subprocess import check_output as Shell
from os import name as SysName
from os import system as Sys
Dependencies = {'googleAPI' : 'googleAPI'} # dependencies need to run the program

CEnd = '\033[0m' # end of coloured text
ErrorText = lambda S: f'\33[31m{S}{CEnd}' #function for errors (red text)
WarningText = lambda S: f'\33[33m{S}{CEnd}' #function for warnings (yellow text)
OKText = lambda S: f'\33[92m{S}{CEnd}' #function for success operations (green text)

def CheckDependencies(): # function to check all the needd dependencies in the script
    ModulesList= [i.decode() for i in Shell('pip list', shell = True).split()][4 :] #
    Modules = [ModulesList[i] for i in range(len(ModulesList)) if i % 2 == 0]
    Versions = [ModulesList[i] for i in range(len(ModulesList)) if i % 2 == 1]
    ModuleString = ' '.join([i.replace('-', '') + '==' + j for i,j in zip(Modules,Versions)])

    MissingModules = [Dependency for Dependency in Dependencies if Dependencies[Dependency] not in ModuleString]

    return MissingModules

if __name__ == '__main__':
    ModulesToIstall = CheckDependencies()
    Sys('cls' if  SysName =='nt' else 'clear')

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

        UInput = input('do you want to create a local database (faster research more memorry required)? <y/n> ')

        if UInput.lower() == 'y':
            from DBManagement import CreateDatabase
            CreateDatabase()

            print(WarningText('It SHOULD be all set'))
            print(OKText('Restart this program to test it out'))
            print(WarningText("(Try running as Administrator if tha script did not work properly)"))

        elif UInput.lower() == 'n':
            print('you can create database anytime with "python DBManagement.py -c" or "python3 DBManagement.py -c"')

        else:
            print(ErrorText('invalid imput'))
            print(ErrorText('exiting'))
            quit()

    else:
        print(OKText('All set you are ready to start'))

