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
    


    #Print header
    os.system('clear')
    pyfiglet.print_figlet('Programs', colors=config[3][1])

    #Split dataframe and print
    program_list = programs[0].tolist()
    call_list = programs[1].tolist()
    for program in program_list:
        print(str(util.int_to_dict(program_list.index(program))) + ': ' + program)

    print('\\: cli')
    
    key = readchar.readkey()
    
    if key == '\\':
        cmd =input('')
        os.system(cmd)
        readchar.readkey()
    
    try:
        if '\x1b' in key:
        
            response = util.dict_to_int(key[1])
            response = int(response)    
            os.system("tmux split-window -h \"{}\"".format(call_list[response]))
        else: 
            response = util.dict_to_int(key)
            response = int(response)    
            os.system('clear')
            pyfiglet.print_figlet(program_list[response], colors=config[3][1])
            os.system(call_list[response])

    except IndexError:
        pass
    os.system('clear')
