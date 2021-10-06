import math
import os
import sys
import time
import pandas
import pyfiglet
import readchar
import sqlalchemy
from requests import get
from json import loads
import util
from timetable import refresh
from program import programs_page
from project import project_page
from new import new_js

def mainpage():
    """
    Main landing page for the OS with one key press  for each subsequent page
    Also includes job and scheduling system

   
    """


    # Read the config file and push it to a dataframe
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    os.system('clear')
    file_types = pandas.read_csv('./config/file_types.csv', header=None)
    programs = pandas.read_csv('./config/programs.csv', header=None).values
    config = pandas.read_csv('./config/config.csv').values
    execs = pandas.read_csv('config/execs.psv',delimiter='|')
    os.chdir(config[1][1])
    password = config[5][1]


    current_job_list = util.sql_to_dataframe('vw_jobs', 'timetable', password, config)
    work_job_list = util.get_work(password, config)

    total_jobs = current_job_list.append(work_job_list, ignore_index=True)
    total_jobs.sort_values(by=['index_score'], inplace=True, ignore_index=True, ascending=False)

    current_task = total_jobs.iloc[0]
    
    # select the schedule items for current and next
    
    schedule = util.sql_to_dataframe('vw_schedule', 'timetable', password, config, where = 'date + interval hour(time) hour + interval minute(time) + length * 60 minute > now() ' )
    current_schedule = schedule.iloc[0]
    current_schedule_next = schedule.iloc[1]
    
    # Print the page
    pyfiglet.print_figlet(config[2][1] + '\'s Dashboard', colors=config[3][1])

    print(
        time.strftime("%Y-%m-%d %H:%M", time.localtime())  + '\n\n' +
        'Current Job: ' + current_task[1] + ' ' + current_task[2] + '\n' +
        'Next Event: ' + current_schedule[1] + ' - ' + current_schedule[2] + ' at ' + str(current_schedule[4])[7:15] + ' on ' + current_schedule[3].strftime('%a') + '\n' +
        'Coming Up: ' + current_schedule_next[1] + ' - ' + current_schedule_next[2] + ' at ' + str(current_schedule_next[ 4])[7:15] + ' on ' + current_schedule_next[3].strftime('%a') +
        '\n\n'
        'Time Table - t'
        '\n\n'
        'Finished Current Job - y'
        '\n\n'
        'Other Projects - p'
        '\n\n'
        'Programs - o'
        '\n\n'
        'New - n'
        '\n\n'
        'Quit - q'
        '\n'
    )
    print('>> ')

    # Set up response system, where we read the key input and then move to the next page
    response = ''
    response = readchar.readkey()

    # Timetable page
    if response == 't':
        refresh(password, config)
        mainpage()

    # set jobs done
    elif response == 'y':

        if current_task[0][1] == 'd':
            util.sm_done_due(current_task[0], password, config)
            mainpage()
        elif current_task[0][1] == 'n':
            util.sm_done_not_due(current_task[0], password, config)
            mainpage()
        elif current_task[0][1] == 'r':
            util.sm_done_recurring(current_task[0], password, config)
            mainpage()
        elif current_task[0][1] == 'w':
            util.done_work(current_task[2], password, config)
            mainpage()

    # Programs page
    elif response == 'o':
        resp = programs_page(programs, config)
        mainpage()


    elif response == 'p':
        initial_head = config[2][1] + '\'s Projects'
        project_page(initial_head, config, file_types, execs)
        mainpage()

    elif response =='n':
        new_js(password,config)
        mainpage()



    elif response == 'q':
        os.system('clear')
        os.chdir(os.path.dirname(sys.argv[0]) + '/config')
        p = config[6][1]
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            util.encrypt(f,p)
        os.system('exit')
        quit(1)

    else:
        mainpage()

    response = readchar.readkey()
    if response:
        mainpage()


if __name__ == '__main__':
    mainpage()
