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
    key = util.fuzzy_loop('Programs', program_list)
 
    if key == 'exit':
        return
        
    elif '\x1b' in key:
        call = call_list[key[0]]    
        os.system("tmux split-window -h \"{}\"".format(call))
    else:
        os.system('clear')
        pyfiglet.print_figlet(program_list[key[0]], colors=config[3][1])
        os.system(call_list[key[0]])

    os.system('clear')
