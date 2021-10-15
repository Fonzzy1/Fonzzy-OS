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
        
def issue_page():
    os.system('clear')
    pyfiglet.print_figlet("Issues")
    
    os.system('gh issue list')
    
    print('Create(n),Comment(c),Close(d),View(v),Edit(e)')
    response = readchar.readkey()

    
    command_dict = {'n':'create','c':'comment','d':'close','v':'view','e':'edit'}
    try:
        command = command_dict[response]
        num = input('Issue Number: ')        
        os.system('gh issue ' + command + ' ' + num)
        issue_page()
    except KeyError:
        return 
        
    
def pr_page():
    os.system('clear')
    pyfiglet.print_figlet("Pull Requests")
    
    os.system('gh pr list')
    
    print('Create(n),Comment(c),Close(d),View(v),Edit(e),Checkout(b),Diff(f),Merge(m),Review(r)')
    response = readchar.readkey()

    
    command_dict = {'n':'create','c':'comment','d':'close','v':'view','e':'edit','b':'checkout','f':'diff','m':'merge','r':'review'}
    try:
        command = command_dict[response]
        num = input('Number: ')
        os.system('gh pr ' + command + ' ' + num)
        pr_page()
    except KeyError:
        return 
 
def branch_page():
    os.system('clear')
    pyfiglet.print_figlet("Branches")
    
    os.system('git branch -a')
    
    print('Create(n),Close(d),Checkout(b)')
    response = readchar.readkey()

    
    command_dict = {'n':' checkout -b','d':'branch -D','b':'checkout'}
    try:
        command = command_dict[response]
        num = input('Branch Name: ')
        os.system('git ' + command + ' ' + num)
        branch_page()
    except KeyError:
        return 
        
def status_page():
    os.system('clear')
    pyfiglet.print_figlet("Status")
    
    os.system('git status -sb')
    
    print('Commit(c),Revert(r),Add(a),Pull(p),Push(s),diff(d)')
    response = readchar.readkey()
    
    command_dict = {'c':'commit','r': 'checkout -- ','a':'add','p':'pull','s':'push','d':'difftool --tool=vimdiff' }
    try:
        command = command_dict[response]
        num = input('File: ')
        os.system('git ' + command + ' ' + num)
        status_page()
    except KeyError:
        return 
        
def log_page():
        os.system('clear')
        os.system('git log --graph --abbrev-commit --decorate --all --format=format:\'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(auto)%d%C(reset)\'')
        print('Commit diff(d),Overall diff(o),Checkout(b)')
        response = readchar.readkey()

        try:
            if response == 'd':
                num = input('Commit: ')            
                os.system('git difftool {}~ {} --tool=vimdiff'.format(num,num))
            if response == '0':
                num = input('Commit: ')                  
                os.system('git difftool {} --tool=vimdiff'.format(num))
            if response == 'b':
                num = input('Commit: ')                  
                name = input('Branch Name: ')
                os.system('git checkout -b  {} {}'.format(name,num))                
        except KeyError:
            return 
        
        
    
	

def git_manager():
    title = subprocess.check_output('basename `git rev-parse --show-toplevel`', shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    
    w = os.get_terminal_size()[0]
    col_w = math.floor(w/4) - 1
    
    os.system('clear')
    
    pyfiglet.print_figlet(title)
    
    status = os.popen('git status -s').read().split('\n')[:-1]
    n_status = len(status)
    ansi_dic = {'M':'\u001b[33m','A':'\u001b[32m','D':'\u001b[31m','R':'\u001b[35m','C':'\u001b[36m','?':'\u001b[37m',' ':''}
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

    print_array  = np.array([pad_status,pad_branch,pad_pr,pad_issue]).T

    header = np.array(['Status','Branch','Pull Req','Issues'])
   
    h = os.get_terminal_size()[1] -rows -  20 

    print(str("{:<"+str(col_w) + "}|{:<"+str(col_w) + "}|{:<"+str(col_w) + "}|{:<"+str(col_w) + "}").format(*header))
    print('-'*w)
    for row in print_array:
        print(str("{:<"+str(col_w) + "}|{:<"+str(col_w) + "}|{:<"+str(col_w) + "}|{:<"+str(col_w) + "}").format(*row))
    print('-'*w)

    os.system('git log --graph --abbrev-commit --decorate --all --format=format:\'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(auto)%d%C(reset)\' -'+str(h))
    
    print('Issues(i), Pull Requests(p), Branches(b), Status(s), Logs(l)')
    response = readchar.readkey()
    
    if response == 'i':
        issue_page()
        git_manager()
    if response == 'p':
        pr_page()
        git_manager()
    if response == 'b':
        branch_page()
        git_manager()
    if response == 's':
        status_page()
        git_manager()
    if response == 'l':
        log_page()
        git_manager()
        
        

    
    
if __name__ == '__main__':
    git_manager()
