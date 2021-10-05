import os
import sys
import shutil
import numpy as np
import pandas as pd
import pyfiglet
import readchar
import util


def project_page(response, config, file_types, execs):
    """
    A simplification of the cd, ls navigation of the terminal
    Also uses a system to open files by checking the extension and then calling in the terminal

    response(str): the next step in the file list
    config(dataframe): config file in dataframe form
    file_types(dataframe): uses dataframe to associate extension with program
    """

    # Print Header
    os.system('clear')
    pyfiglet.print_figlet(response, colors=config[3][1])


    # List all the files in current directory, remove the one we dont want
    project_list = os.listdir()
    unwanted = ['__init__.py', '__pycache__']
    for item in unwanted:
        try:
            project_list.remove(item)
        except:
            pass
    for item in project_list:
        if item.startswith('.'):
            project_list.remove(item)
    project_list = sorted(project_list)

    # Print the page
    for project in project_list:
        print(str(util.int_to_dict(project_list.index(project))) + ': ' + project)
    print('Go to file, n for new file, b for back, any other key to quit: ')
    response = readchar.readkey()

    # make new file or folder for weather or not . in name
    if util.dict_to_int(response) >= len(project_list):
    	return
    	
    elif response == 'n':
        file_name = input("File Name: ")
        if '.' in file_name:
            os.system("touch " + file_name)
        else:
            os.mkdir('./' + file_name)

        project_page('New File Added', config, file_types, execs)

    # go up a dir
    elif response == 'b':
        os.chdir('..')
        project_page(os.path.basename(os.getcwd()), config, file_types, execs)

    
    # open file with extension
    elif os.path.isfile(project_list[util.dict_to_int(response)]):
        file_name = project_list[util.dict_to_int(response)]
        try:
            extention = file_name.split('.')[1]
            index =  np.where(file_types[0] == extention)[0][0]
            programs =file_types[1][index].split(';')
        except IndexError:
            programs = execs['key'].tolist()

        os.system('clear')
        pyfiglet.print_figlet(file_name, colors=config[3][1])

        for exec in programs:
            print(str(util.int_to_dict(programs.index(exec))) + ': ' + exec)
        print('b: Delete file')
        print('n: Rename file')
        print('m: Move file')

        response2 = readchar.readkey()

        if response2 == 'b':
            os.remove(file_name)

        elif response2 == 'n':
            new_name = input('Change file name to: ')
            os.rename(file_name, new_name)

        elif response2 == 'm':
            new_loc = input('New file destination: ')
            shutil.move(file_name,new_loc)


        else:
            try:
                index = util.dict_to_int(response2)	
                command = execs['value'][np.where(execs['key'] == programs[index])[0][0]]
                full_command = command.format(file_name)
                os.system(full_command)
                if execs['wait'][np.where(execs['key'] == programs[index])[0][0]] == 1:
                    wait = readchar.readkey()
            except IndexError:
                pass
        project_page(os.path.basename(os.getcwd()), config, file_types, execs)






    elif os.path.isdir(project_list[util.dict_to_int(response)]):
        index = util.dict_to_int(response)
        try:
            os.chdir('./' + project_list[index])
            project_page(project_list[index], config, file_types, execs)
        except:
            pass

    else:
        return
        
