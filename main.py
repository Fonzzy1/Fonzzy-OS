import os
import sys
import time
import pandas
import pandas as pd
import pyfiglet
import readchar
import sqlalchemy
from requests import get
from json import loads



def sm_done_recurring(task_id, password, config):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update tbl_jobs_recurring set last_date = now() where id = ' + str(id)
    connection.execute(query)


def sm_done_due(task_id, password, config):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update tbl_jobs_due set done = 1 where id = ' + str(id)
    connection.execute(query)


def sm_done_not_due(task_id, password, config):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update tbl_jobs_not_due set done = 1 where id = ' + str(id)
    connection.execute(query)


def sql_to_dataframe(table_name, database, password, config, where = ''):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    if where == '':
        df = pandas.read_sql_table(table_name, con=connection)
    else:
        query = 'select * from ' + table_name + ' where ' + where + ';'
        df = pandas.read_sql_query(query, con=connection)
    return df



def main_page(password):
    response = ''
    os.chdir(os.path.dirname(sys.argv[0]))
    os.system('clear')
    file_types = pandas.read_csv('./config/file_types.csv', header=None).values
    programs = pandas.read_csv('./config/programs.csv', header=None).values
    config = pandas.read_csv('./config/config.csv').values
    os.chdir(config[1][1])
    try:
        current_mode = sql_to_dataframe('vw_current_schedule', 'timetable', password, config).iloc[0,1]
    except IndexError:
        current_mode = ''
    try:
        if current_mode != '':
            current_task = sql_to_dataframe('vw_jobs', 'timetable', password, config, where='project = \'' + current_mode + '\'').iloc[0]
        else:
            current_task = sql_to_dataframe('vw_jobs', 'timetable', password, config).iloc[0]
    except IndexError:
         current_task = '     '
    current_schedule = sql_to_dataframe('vw_schedule', 'timetable', password, config).iloc[0]
    current_schedule_next = sql_to_dataframe('vw_schedule', 'timetable', password, config).iloc[1]
    quote = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    try:
        test ='{quoteText} - {quoteAuthor}'.format(**loads(quote.text))
    except:
        main_page(password)
    pyfiglet.print_figlet(config[2][1] + '\'s Dashboard', colors=config[3][1])

    print(
        '{quoteText} - {quoteAuthor}'.format(**loads(quote.text)) + '\n\n' +
        time.strftime("%Y-%m-%d %H:%M", time.localtime()) +
        '\n\n'
        'Current Job: ' + current_task[1] + ' ' + current_task[2] + '\n' +
        'Next Event: ' + current_schedule[1] + ' - ' + current_schedule[2] +' at ' + current_schedule[4].strftime('%-I:%M %p') + ' on ' + current_schedule[3].strftime('%a') + '\n' +
        'Coming Up: ' + current_schedule_next[1] + ' - ' + current_schedule_next[2] + ' at ' + current_schedule_next[4].strftime('%-I:%M %p') + ' on ' + current_schedule_next[3].strftime('%a') + '\n' +
        '\n\n'        'Show info - r'
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

    response = readchar.readkey()

    if response == 'r':

        f = open("README.md", "r")
        os.system('clear')
        print(f.read())
        print('Enter any key to return: ')
        response = readchar.readkey()
        if response:
            main_page(password)

    elif response == 't':
        refresh(0, password, config)

    elif response == 'y':
        if current_task[0][1] == 'd':
            sm_done_due(current_task[0], password, config)
            main_page(password)
        elif current_task[0][1] == 'n':
            sm_done_not_due(current_task[0], password, config)
            main_page(password)
        elif current_task[0][1] == 'r':
            sm_done_recurring(current_task[0], password, config)
            main_page(password)


    elif response == 'o':
        programs_page(password, programs, config)


    elif response == 'p':
        initial_head = config[2][1] + '\'s Projects'
        project_page(initial_head, password, config, file_types)

    elif response == 'q':
        os.system('clear')
        os.system('exit')
        quit(1)

    else:
        main_page(password)


def project_page(response, password, config, file_types):
    project_list = os.listdir()
    os.system('clear')
    ascii_art = pyfiglet.print_figlet(response, colors=config[3][1])
    unwanted = ['__init__.py', '__pycache__']
    for item in unwanted:
        try:
            project_list.remove(item)
        except:
            break
    for item in project_list:
        if item.startswith('.'):
            project_list.remove(item)
    project_list = sorted(project_list)
    for project in project_list:
        print(str(project_list.index(project)) + ': ' + project)
    print('Go to file, q to quit, n for new file: ')
    response = readchar.readkey()
    if response == 'q':
        os.chdir(os.path.dirname(sys.argv[0]))
        main_page(password)
    elif response == 'n':
        file_name = input("File Name: ")
        os.system("touch " + file_name)
        project_page('New File Added', password, config, file_types)




    elif '.' in project_list[int(response)]:
        for row in file_types:
            if project_list[int(response)].endswith(row[0]):
                os.system(row[1] + ' ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page(password)

    else:
        try:
            os.chdir('./' + project_list[int(response)])
            project_page(project_list[int(response)], password, config, file_types)
        except:
            project_page('Oops, Try Again', password, config, file_types)


def programs_page(password, programs, config):
    os.system('clear')
    pyfiglet.print_figlet('Programs', colors=config[3][1])
    program_list = programs[0].tolist()
    call_list = programs[1].tolist()
    for program in program_list:
        print(str(program_list.index(program)) + ': ' + program)
    response = readchar.readkey()
    try:
        response = int(response)
    except:
        main_page(password)
    os.system(call_list[response] + ' &')
    os.system('clear')
    main_page(password)


def refresh(offset, password, config):
    os.system('clear')
    pyfiglet.print_figlet('Timetable', colors=config[3][1])
    timetable = pd.DataFrame(columns=['Time','MON','TUE','WED','THU','FRI','SAT','SUN'])
    timetable['Time'] = ['06','07','08','09', '10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
    timetable.index = timetable['Time']
    for day in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
        for time in timetable['Time']:
            clause = 'day = \''+str(day)+'\' and start <= \'' + str(time) + ':00:00\' and end > \'' + str(time) + ':00:00\' '
            val = sql_to_dataframe('vw_week_calendar', 'timetable', password, config, where = clause)
            if not val.empty:
                text = str(val.loc[0][0] + '-' + val.loc[0][1]).center(16,' ')
            else:
                text = '     ######     '
            timetable[day][time] = text
            os.system('clear')
            pyfiglet.print_figlet('Timetable', colors=config[3][1])
            print(timetable.to_string(index=False, col_space=[4, 16, 16, 16, 16, 16, 16, 16], justify='center'))
            print('Press any key to return')

    response = readchar.readkey()
    if response:
        main_page(password)

def start():
    os.system('clear')
    os.chdir(os.path.dirname(sys.argv[0]))
    config = pandas.read_csv('./config/config.csv').values
    pyfiglet.print_figlet(config[2][1] + '\'s Dashboard', colors=config[3][1])
    while True:
        try:
            password = input('Password: ')
            sql_to_dataframe('tbl_jobs_due', 'timetable', password, config)
            break
        except Exception as e:
            print("Oops!  That not the password.  Try again...")

    main_page(password)


start()
