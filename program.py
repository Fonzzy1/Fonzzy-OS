import os
import util
import pyfiglet
import readchar
import pandas

def programs_page(config):
    """
    Allows for opening of programs from os

    programs(dataframe): list of programs with associated terminal commands
    config(dataframe): config file in dataframe form

    """

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    programs = pandas.read_csv(dname +'/config/programs.csv', header=None)
    

    #Split dataframe and print
    program_list = programs[0].tolist()
    call_list = programs[1].tolist()
    ss = ''
    hold = util.fuzzy_find(program_list,ss)
    c = False
    while not c:
        #Print header
        os.system('clear')
        pyfiglet.print_figlet('Programs', colors=config[3][1])
        print(ss)
        index = hold.copy()
        print(index)
        max_len =  max([len(x) for i,x in index])
        for i,x in index:
            print(str(x.ljust(max_len) + ': ' + program_list[i]))

        key = readchar.readkey()

        if '\r' in key:
            c = True
        elif key == '\x7f':
            ss = ss[0:len(ss) -1]
            hold = util.fuzzy_find(program_list,ss)
        else:
            ss += key
            hold = util.fuzzy_find(program_list,ss)
 
    if '\x1b' in key:
        response  = index[0][0]
        call = call_list[response]    
        os.system("tmux split-window -h \"{}\"".format(call))
    else:
        os.system('clear')
        response  = index[0][0]
        pyfiglet.print_figlet(program_list[response], colors=config[3][1])
        os.system(call_list[response])

    os.system('clear')
