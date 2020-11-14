Deps = ['googleapi', 'pytube']
from subprocess import check_output as Shell

if __name__ == '__main__':
    CEnd = '\033[0m'
    ErrorText = lambda S: '\33[31m' + S + CEnd
    WarningText = lambda S: '\33[33m' + S + CEnd

    ModulesList= [i.decode() for i in Shell('pip list', shell = True).split()][4 :]
    Modules = [ModulesList[i] for i in range(len(ModulesList)) if i % 2 == 0]
    Versions = [ModulesList[i] for i in range(len(ModulesList)) if i % 2 == 1]
    ModuleString = ' '.join([i.replace('-', '') + '==' + j for i,j in zip(Modules,Versions)])

    for Dep in Deps:
        if not Dep in ModuleString:
            print(ErrorText('it seems that you have not the' + Dep + 'dependency in this python version'))
            Shell('pip install ' + Dep)

            if not Dep in ModuleString:
                print(ErrorText('you do not have required permission to install the module ' + Dep))
                print(WarningText('try execute this script as admin'), '\n')
                break
