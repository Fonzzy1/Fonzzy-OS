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


def main_page(password):
    """
    Main landing page for the OS with one key press  for each subsequent page
    Also includes job and scheduling system

    password(str): SQL database password
    """

    # retrieve inspirational quote, get statement often fails so loop try until it works
    quote = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    try:
        test = '{quoteText} - {quoteAuthor}'.format(**loads(quote.text))
    except:
        main_page(password)

    # Read the config file and push it to a dataframe
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    os.system('clear')
    file_types = pandas.read_csv('./config/file_types.csv', header=None).values
    programs = pandas.read_csv('./config/programs.csv', header=None).values
    config = pandas.read_csv('./config/config.csv').values
    os.chdir(config[1][1])

    # Mode, job and schedule reads from vw_schedule and vw_jobs
    # Mode works such that if you are within a schedule item you will then be shown jobs with the same project
    # eg. if in schedule with project  'work' then only jobs with project 'work' will be shown

    try:  # Test to see if anything is in table_vw_Current_schedule, if not will set current mode to ''
        current_mode = util.sql_to_dataframe('vw_current_schedule', 'timetable', password, config).iloc[0, 1]
    except IndexError:
        current_mode = ''

    # Select task list corresponding to the mode
    try:
        if current_mode != '':
            current_task = util.sql_to_dataframe('vw_jobs', 'timetable', password, config,
                                                 where='project = \'' + current_mode + '\'').iloc[0]
        else:
            current_task = util.sql_to_dataframe('vw_jobs', 'timetable', password, config).iloc[0]
    except IndexError:
        current_task = '     '

    # select the schedule items for current and next
    current_schedule = util.sql_to_dataframe('vw_schedule', 'timetable', password, config).iloc[0]
    current_schedule_next = util.sql_to_dataframe('vw_schedule', 'timetable', password, config).iloc[1]

    # Print the page
    pyfiglet.print_figlet(config[2][1] + '\'s Dashboard', colors=config[3][1])

    print(
        '{quoteText} - {quoteAuthor}'.format(**loads(quote.text)) + '\n\n' +
        time.strftime("%Y-%m-%d %H:%M", time.localtime()) +
        '\n\n'
        'Current Job: ' + current_task[1] + ' ' + current_task[2] + '\n' +
        'Next Event: ' + current_schedule[1] + ' - ' + current_schedule[2] + ' at ' + current_schedule[4].strftime(
            '%-I:%M %p') + ' on ' + current_schedule[3].strftime('%a') + '\n' +
        'Coming Up: ' + current_schedule_next[1] + ' - ' + current_schedule_next[2] + ' at ' + current_schedule_next[
            4].strftime('%-I:%M %p') + ' on ' + current_schedule_next[3].strftime('%a') +
        '\n\n'
        'Time Table - t'
        '\n\n'
        'Finished Current Job - y'
        '\n\n'
        'Other Projects - p'
        '\n\n'
        'Programs - o'
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
        main_page(password)

    # set jobs done
    elif response == 'y':
        if current_task[0][1] == 'd':
            util.sm_done_due(current_task[0], password, config)
            main_page(password)
        elif current_task[0][1] == 'n':
            util.sm_done_not_due(current_task[0], password, config)
            main_page(password)
        elif current_task[0][1] == 'r':
            util.sm_done_recurring(current_task[0], password, config)
            main_page(password)

    # Programs page
    elif response == 'o':
        programs_page(programs, config)
        main_page(password)


    elif response == 'p':
        initial_head = config[2][1] + '\'s Projects'
        project_page(initial_head, config, file_types)
        main_page(password)

    elif response == 'q':
        os.system('clear')
        os.system('exit')
        quit(1)

    else:
        main_page(password)

    response = readchar.readkey()
    if response:
        main_page(password)
