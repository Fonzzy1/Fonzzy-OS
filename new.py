import os
import sqlalchemy
import pyfiglet


def new_js(password, config):
    os.system('clear')
    pyfiglet.print_figlet('New', colors=config[3][1])
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable' 
    connection = sqlalchemy.create_engine(db_connection_str)
    type = input('Job (j) or Scheduled Event (s)?')
    if type == 'j':
        jtype = input('Is the Job Due (d), Not Due (n) or Reccuring (r)')
        if jtype =='d':
            project = input('Project: ')
            desc = input('Description: ')
            length = input('Length: ')
            date = input('Due Date: ')
            time =  input('Due Time: ')
            connection.execute('insert into tbl_jobs_due(project,description, length, due_date, due_time) values (\''+project+ '\',\''+desc+ '\',\''+length+ '\',\''+date+ '\',\''+time+ '\')')
        if jtype =='n':
            project = input('Project: ')
            desc = input('Description: ')
            length = input('Length: ')
            connection.execute('insert into tbl_jobs_not_due(project,description, length) values (\''+project+ '\',\''+desc+ '\',\''+length+ '\')')
        if jtype =='r':
            project = input('Project: ')
            desc = input('Description: ')
            length = input('Length: ')
            redo = input('Redo Time: ')
            last =  input('Last Date: ')
            connection.execute('insert into tbl_jobs_recurring(project,description, length, redo_time, last_date) values (\''+project+ '\',\''+desc+ '\',\''+length+ '\',\''+redo+ '\',\''+last+ '\')')
    if type == 's':
        jtype = input('Is the Event Recurring (r) or One Off (o)')
        if jtype =='o':
            project = input('Project: ')
            desc = input('Description: ')
            date = input('Date: ')
            time = input('Time: ')
            length =  input('Length: ')
            connection.execute('insert into tbl_schedule_one_off(project,description, date, time, length) values (\''+project+ '\',\''+desc+ '\',\''+date+ '\',\''+time+ '\',\''+length+ '\')')
        if jtype =='r':
            project = input('Project: ')
            desc = input('Description: ')
            day = input('Day: ')
            time = input('Time: ')
            length =  input('Length: ')
            connection.execute('insert into tbl_schedule_one_off(project,description, day, time, length) values (\''+project+ '\',\''+desc+ '\',\''+day+ '\',\''+time+ '\',\''+length+ '\')')
