import os
import sys
import time
import time as t

import pandas
import pyfiglet
import readchar
import sqlalchemy


def sm_done_class(task_id, password, config):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/School'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update classes set revision = revision + 1, last_date = now() where task_id = ' + str(id)
    connection.execute(query)


def sm_done_assessment(task_id, password, config):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/School'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update assessments set done = 1 where id = ' + str(id)
    connection.execute(query)


def sql_to_dataframe(table_name, database, password, config):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    df = pandas.read_sql_table(table_name, con=connection)
    return df



def main_page(password):
    response = ''
    os.chdir(os.path.dirname(sys.argv[0]))
    os.system('clear')
    file_types = pandas.read_csv('./config/file_types.csv', header=None).values
    programs = pandas.read_csv('./config/programs.csv', header=None).values
    config = pandas.read_csv('./config/config.csv').values
    os.chdir(config[1][1])
    current_task = sql_to_dataframe('task_list', 'School', password, config).iloc[0]

    pyfiglet.print_figlet(config[2][1] + '\'s Dashboard', colors=config[3][1])

    print(
        'A collection of projects, made mostly for myself and will most likely not work on other machines, created so I '
        'can easily run my work\n\n' +
        time.strftime("%Y-%m-%d %H:%M", time.localtime()) +
        '\n\n'
        'Current Job: ' + current_task[1] +
        '\n\n'
        'Show info - r'
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
        if current_task['id'][0] == 't':
            sm_done_class(current_task['id'], password, config)
            main_page(password)
        elif current_task['id'][0] == 'a':
            sm_done_assessment(current_task['id'], password, config)
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
    tasks = sql_to_dataframe('task_list', 'School', password, config)
    if len(tasks) > 0:
        current_task = tasks.iloc[offset]
        print(t.strftime("%Y-%m-%d", t.localtime()))
        print('Jobs to do: ' + str(len(tasks)))
        print('Current Task: ' + current_task['task_name'])
        print('Due: ' + str(current_task['task_date'])[0:10])
        print('y for done\ns for Skip\nr for Refresh\nq for exit\nl for list all: ')
        response = readchar.readkey()

        if response == 'q':
            response = 1
            if response == 1:
                main_page(password)
        elif response == 'r':
            offset = 0
            refresh(offset, password, config)
        elif response == 's':
            if offset < len(tasks) - 1:
                offset += 1
            refresh(offset, password, config)
        elif response == 'l':
            os.system('clear')
            pyfiglet.print_figlet('Timetable', colors=config[3][1])
            print('Jobs to do: ' + str(len(tasks)))

            for row in sorted(tasks['task_name']):
                print(tasks.loc[tasks['task_name'] == row]['task_name'].values[0] + ' : ' + str(
                    tasks.loc[tasks['task_name'] == row]['task_date'].values[0])[0:10])
            print('Press Y to set all to done or press any key to return to main: ')
            exe = readchar.readkey()
            if exe == 'Y':
                for row in tasks.index:
                    current_task = tasks.loc[row]
                    if current_task['id'][0] == 't':
                        sm_done_class(current_task['id'], password, config)
                    elif current_task['id'][0] == 'a':
                        sm_done_assessment(current_task['id'], password, config)
                refresh(offset, password, config)
            else:
                refresh(offset, password, config)
        elif response == 'y':
            offset = 0
            if current_task['id'][0] == 't':
                sm_done_class(current_task['id'], password, config)
                refresh(offset, password, config)
            elif current_task['id'][0] == 'a':
                sm_done_assessment(current_task['id'], password, config)
                refresh(offset, password, config)
        else:
            refresh(offset, password, config)
    else:
        print('No Jobs')
        print('return to main')
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
            sql_to_dataframe('task_list', 'School', password, config)
            break
        except:
            print("Oops!  That not the password.  Try again...")

    main_page(password)


start()
