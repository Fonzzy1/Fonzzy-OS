import os
import sys

import pyfiglet
import readchar

import util


def project_page(response, config, file_types):
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
    if response == 'n':
        file_name = input("File Name: ")
        if '.' in file_name:
            os.system("touch " + file_name)
        else:
            os.mkdir('./' + file_name)

        project_page('New File Added', config, file_types)

    # go up a dir
    elif response == 'b':
        os.chdir('..')
        project_page(os.path.basename(os.getcwd()), config, file_types)


    # open file with extension
    elif '.' in project_list[util.dict_to_int(response)]:
        index = util.dict_to_int(response)
        for row in file_types:
            if project_list[index].endswith(row[0]):
                os.system(row[1] + ' ./' + project_list[index] + ' &')
        os.system('clear')
        return

    else:
        index = util.dict_to_int(response)
        try:
            os.chdir('./' + project_list[index])
            project_page(project_list[index], config, file_types)
        except:
            pass
        return
