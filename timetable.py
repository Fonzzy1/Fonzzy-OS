import math
import os

import readchar

import util
import pandas as pd
import pyfiglet


def refresh(password, config):
    """
    Prints the timetable for the current week

    password(str): sql database password
    config(dataframe): config dataframe for username and driver

    returns: Response(char(1)): key pressed - not used, just implemented to wait for end of function


    """
    # Get Width of terminal so that the print statement doesn't suck
    width = os.get_terminal_size()[0] - 7
    width_col =  math.floor((width-4)/7)

    # Clear and print header
    os.system('clear')
    pyfiglet.print_figlet('Timetable', colors=config[3][1])
    print('Loading')
    # Set up empty dataframe to then fill
    timetable = pd.DataFrame(columns=['Time','MON','TUE','WED','THU','FRI','SAT','SUN'])
    timetable['Time'] = ['08:00','08:30','09:00','09:30', '10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00']
    timetable.index = timetable['Time']

    # Fill dataframe by row and column
    for day in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
        for time in timetable['Time']:

            # Check query of something exists in vw_week_calender, if not return '#####'
            clause = 'day = \''+str(day)+'\' and start <= \'' + str(time) + ':00\' and end > \'' + str(time) + ':00\' order by id asc limit 1'
            val = util.sql_to_dataframe('vw_week_calendar', 'timetable', password, config, where = clause)
            if not val.empty:
                text = str(val.loc[0][0] + '-' + val.loc[0][1]).center(width_col,' ')
            else:
                text = '-----'.center(width_col, ' ')
            timetable[day][time] = text #setting the value

    # Re-print the page
    os.system('clear')
    pyfiglet.print_figlet('Timetable', colors=config[3][1])
    print(timetable.to_string(index=False, col_space=[4, width_col, width_col, width_col, width_col, width_col, width_col, width_col], justify='center', max_colwidth=width_col,na_rep = '-----'))

    pyfiglet.print_figlet('Jobs', colors=config[3][1])
    
    current_job_list = util.sql_to_dataframe('vw_jobs', 'timetable', password, config)
    work_job_list = util.get_notion_jobs(password, config)

    total_jobs = current_job_list.append(work_job_list, ignore_index=True)
    total_jobs.sort_values(by=['index_score','id'], inplace=True, ignore_index=True, ascending=[False,True])
    for [index,job] in total_jobs[0:10].iterrows():
        print(str(index) + ' - ' + job[1] + '|' + job[2]+ ' ' + str(job[3]))
        
      
    print('Press 0-9 to set done, else press any other key to return')
    response = readchar.readkey()
    
    try:
    	index = int(response)
    	id = total_jobs.iloc[index][0]
    	
    	print(id)
    	print(index)
    	print(total_jobs[0:10])
    	if id[1] == 'd':
            util.sm_done_due(id, password, config)
    	elif id[1] == 'n':
            util.sm_done_not_due(id, password, config)
    	elif id[1] == 'r':
            util.sm_done_recurring(id, password, config)
    	elif id[1] == 'w':
            util.sm_done_notion(job[2][index], password, config)

    	 
    except ValueError:
    	pass	 
    return response

