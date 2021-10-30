import os
import sys
import shutil
import numpy as np
import pandas as pd
import pyfiglet
import readchar
import util
import math
from share import upload, email

import subprocess
from git import git_manager
from program import programs_page

def project_page(response, config, file_types, execs):
    """
    A simplification of the cd, ls navigation of the terminal
    Also uses a system to open files by checking the extension and then calling in the terminal

    response(str): the next step in the file list
    config(dataframe): config file in dataframe form
    file_types(dataframe): uses dataframe to associate extension with program
    """

    # Print Header

    try:	
        is_git = subprocess.check_output('git rev-parse --is-inside-work-tree',shell = True, stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError:
        is_git = False
    # List all the files in current directory, remove the one we dont want
    project_list = os.listdir()
    unwanted = ['__init__.py', '__pycache__']
    for item in unwanted:
        try:
            project_list.remove(item)
        except:
            pass
    
    n = len(project_list) 
    project_list.append('New')
    project_list.append('Back')
    project_list.append('Programs')
    project_list.append('Upload')
    project_list.append('Email')
    if is_git:    
        project_list.append('Git')
    
    key = util.fuzzy_loop(response, project_list)
    
    if key == 'exit':
       return
    
    
    if key[0] >= n:
    # make new file or dir
        if  project_list[ key[0]] == 'New':
            print("File(f) or Directory(d)")
            dorf = readchar.readkey()
            file_name = input("Name: ")
            if dorf == 'f':
                os.system("touch " + file_name)
            if dorf == 'd':
                os.mkdir('./' + file_name)
                os.chdir('./' + file_name)

            project_page('New File Added', config, file_types, execs)

        # go up a dir
        elif project_list[ key[0]] == 'Back':
            os.chdir('..')
            project_page(os.path.basename(os.getcwd()), config, file_types, execs)
        
        elif project_list[ key[0]] == 'Git' and is_git:
            git_manager()
            project_page(os.path.basename(os.getcwd()), config, file_types, execs)
    
        elif project_list[ key[0]] == 'Programs':
            programs_page(config)
            project_page(os.path.basename(os.getcwd()), config, file_types, execs)
    
        elif project_list[ key[0]] == 'Upload':
            upload(os.path.basename(os.getcwd()))
            project_page(os.path.basename(os.getcwd()), config, file_types, execs)
        
        elif project_list[ key[0]] == 'Email':
            email(os.path.basename(os.getcwd()))
            project_page(os.path.basename(os.getcwd()), config, file_types, execs)

    # open file with extension
    elif os.path.isfile(project_list[ key[0]]):
        file_name = project_list[ key[0]]
        try:
            extention = file_name.split('.')[1]
            index =  np.where(file_types[0] == extention)[0][0]
            programs =file_types[1][index].split(';')
        except IndexError:
            programs = execs['key'].tolist()

        programs.append('Delete')
        programs.append('Rename')
        programs.append('Move')
        programs.append('Upload')
        programs.append('Email')
        key2 = util.fuzzy_loop(file_name, programs)
        
        if key2 != 'exit':


            if programs[ key2[0]] == 'Delete':
                conf = input('Type y to confirm: ')
                if conf.lower() == 'y':
                    os.remove(file_name)

            elif programs[ key2[0]] == 'Rename':
                new_name = input('Change file name to: ')
                os.rename(file_name, new_name)

            elif programs[ key2[0]] == 'Move':
                new_loc = input('New file destination: ')
                shutil.move(file_name,new_loc)
            
            elif programs[ key2[0]] == 'Upload':
               upload(file_name)
               
            
            elif programs[ key2[0]] == 'Email':
                email(file_name)

            else:
                if not '\x1b' in key2:
                        command = execs['value'][np.where(execs['key'] == programs[key2[0]])[0][0]]
                        full_command = command.format(file_name)
                        os.system(full_command)  
                        if execs['wait'][np.where(execs['key'] == programs[key2[0]])[0][0]] == 1:
                            readchar.readkey()               
                else:
                        command = execs['value'][np.where(execs['key'] == programs[key2[0]])[0][0]]
                        full_command = command.format(file_name)
                        if execs['wait'][np.where(execs['key'] == programs[key2[0]])[0][0]] == 1:
                        	os.system("tmux split-window -h \"{};read -n 1\"".format(full_command))
                        else:
                            os.system("tmux split-window -h \"{}\"".format(full_command))

		        
		 
        project_page(os.path.basename(os.getcwd()), config, file_types, execs)






    elif os.path.isdir(project_list[ key[0]]):
         os.chdir('./' + project_list[ key[0]])
         project_page(project_list[ key[0]], config, file_types, execs)
  
    else:
        return
