import os
import sys
import shutil
import numpy as np
import pandas as pd
import pyfiglet
import readchar
import util
import math
import subprocess


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
    hidden_list = []
    for item in project_list:
        if item.startswith('.'):
            project_list.remove(item)
            hidden_list.append(item)
            
    project_list = sorted(project_list, key=lambda v: (v.casefold(), v))
    hidden_list = sorted(hidden_list, key=lambda v: (v.casefold(), v))
    project_list = project_list + hidden_list

    # Print the page
    h = (os.get_terminal_size()[1] - 10) * 3/4
    
    project_print = np.array([str(util.int_to_dict(project_list.index(project))) + ': ' + project for project in project_list])
    cols  = math.ceil(len(project_print)/h)
    rows = math.ceil(len(project_print)/cols)
    pad = cols * rows - len(project_print)
    project_array = np.reshape(np.pad(project_print,(0,pad), constant_values=''), (cols,rows)).T
    for row in project_array:
        print(('{: <30}'*cols).format(*row))
    if is_git:    
        print('Go to file, n for new, b for back, g for git, any other key to quit: ')
    else:
        print('Go to file, n for new, b for back, any other key to quit: ')
    response = readchar.readkey()

    # make new file or dir
    if response == 'n':
    	
        dorf = input("File(f) or Directory(d)")
        file_name = input("Name: ")
        if dorf == 'f':
            os.system("touch " + file_name)
        if dorf == 'd':
            os.mkdir('./' + file_name)
            os.chdir('./' + file_name)

        project_page('New File Added', config, file_types, execs)

    # go up a dir
    elif response == 'b':
        os.chdir('..')
        project_page(os.path.basename(os.getcwd()), config, file_types, execs)
        
    elif response == 'g' and is_git:
        git_manager()
        project_page(os.path.basename(os.getcwd()), config, file_types, execs)


    elif util.dict_to_int(response) >= len(project_list):
    	return
    
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
            conf = input('Type y to confirm: ')
            if conf.lower() == 'y':
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
        
def git_manager():
    title = subprocess.check_output('basename `git rev-parse --show-toplevel`', shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    
    os.system('clear')
    
    pyfiglet.print_figlet(title)
    
    status = os.popen('git status -s').read().split('\n')[:-1]
    n_status = len(status)
    ansi_dic = {'M':'\u001b[33m','A':'\u001b[32m','D':'\u001b[31m','R':'\u001b[35m','C':'\u001b[36m','?':'\u001b[37m'}
    print_status = np.array([ansi_dic[file[1]] + file for file in status], dtype='str')
        
    
    branch = os.popen('git branch -a').read().split('\n')[:-1]
    n_branch = len(branch)
    for index, b in enumerate(branch):
        if '*' in b:
            branch[index] = '\u001b[32m' + b + "\u001b[0m"
        else:
            branch[index] = '\u001b[35m' + b + "\u001b[0m"
    print_branch = np.array(branch, dtype='str')
    
    pr  = os.popen('gh pr list').read().split('\n')[:-1]
    n_pr = len(pr)
    for index, p in enumerate(pr):
        pr[index] = p.split("\t")[1]
    print_pr = np.array(pr, dtype='str')		
    
    
    issue = os.popen(' gh issue list').read().split('\n')[:-1]
    n_issue = len(issue)
    for index, i in enumerate(issue):
         issue[index]  = i.split('\t')[2]
       
    print_issue = np.array(issue, dtype='str')
    
    rows = max([n_branch,n_status, n_pr,n_issue])
    
    
    pad_status = np.pad(print_status,(0,rows - n_status),constant_values='')
    pad_branch = np.pad(print_branch,(0,rows - n_branch),constant_values='')
    pad_pr = np.pad(print_pr,(0,rows - n_pr),constant_values='')
    pad_issue = np.pad(print_issue,(0,rows - n_issue),constant_values='')
    
    h = os.get_terminal_size()[1] -rows -  15 
    w = os.get_terminal_size()[0]
    col_w = math.floor(w/4) - 1
    
    print_array  = np.array([pad_status,pad_branch,pad_pr,pad_issue]).T

    header = np.array(['Status','Branch','Pull Req','Issues'])
   
    h = os.get_terminal_size()[1] -rows -  20 
    w = os.get_terminal_size()[0]


    print(str("{:<"+str(col_w) + "}|{:<"+str(col_w) + "}|{:<"+str(col_w) + "}|{:<"+str(col_w) + "}").format(*header))
    print('-'*w)
    for row in print_array:
        print(str("{:<"+str(col_w) + "}|{:<"+str(col_w) + "}|{:<"+str(col_w) + "}|{:<"+str(col_w) + "}").format(*row))
    print('-'*w)

    os.system('git log --graph --abbrev-commit --decorate --format=format:\'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(auto)%d%C(reset)\' -'+str(h))
    input('')
