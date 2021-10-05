import os
import util
import pyfiglet
import readchar


def programs_page(programs, config):
    """
    Allows for opening of programs from os

    programs(dataframe): list of programs with associated terminal commands
    config(dataframe): config file in dataframe form

    """

    #Print header
    os.system('clear')
    pyfiglet.print_figlet('Programs', colors=config[3][1])

    #Split dataframe and print
    program_list = programs[0].tolist()
    call_list = programs[1].tolist()
    for program in program_list:
        print(str(util.int_to_dict(program_list.index(program))) + ': ' + program)

    #

    try:
        response = util.dict_to_int(readchar.readkey())
        response = int(response)    
        os.system('clear')
        pyfiglet.print_figlet(program_list[response], colors=config[3][1])
        os.system(call_list[response])
    except:
        pass
    os.system('clear')
