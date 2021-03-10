from subprocess import check_output as Shell

Dependencies = {'googleAPI' : 'googleAPI', 'Pillow': 'Pillow'}

CEnd = '\033[0m'
ErrorText = lambda S: '\33[31m' + S + CEnd
WarningText = lambda S: '\33[33m' + S + CEnd
OKText = lambda S: '\33[92m' + S + CEnd

def CheckDependencies():
    ModulesList= [i.decode() for i in Shell('pip list', shell = True).split()][4 :]
    Modules = [ModulesList[i] for i in range(len(ModulesList)) if i % 2 == 0]
    Versions = [ModulesList[i] for i in range(len(ModulesList)) if i % 2 == 1]
    ModuleString = ' '.join([i.replace('-', '') + '==' + j for i,j in zip(Modules,Versions)])

    MissingModules = [Dependency for Dependency in Dependencies if Dependencies[Dependency] not in ModuleString]

    return MissingModules

if __name__ == '__main__':
    ModulesToIstall = CheckDependencies()
    if len(ModulesToIstall) > 0 :
        print(WarningText('you need to install the following modules:'))

        for Module in ModulesToIstall:
            print(ErrorText(Module))

        UInput = input('do you want to autoinstall them? <y/n>')
        Commands = ['pip install ' + Module for Module in ModulesToIstall]

        if UInput.lower() == 'y':
            for Command in Commands:
                Shell(Command, shell = True)

            print(WarningText('It SHOULD be all set'))
            print(OKText('Restart this program to test it out'))
            print(WarningText("(Try running as Administrator if it doesn't work)"))

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

