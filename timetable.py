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
    width = os.get_terminal_size()[0]
    width_col =  math.floor((width-4)/7)

    # Clear and print header
    os.system('clear')
    pyfiglet.print_figlet('Timetable', colors=config[3][1])

    # Set up empty dataframe to then fill
    timetable = pd.DataFrame(columns=['Time','MON','TUE','WED','THU','FRI','SAT','SUN'])
    timetable['Time'] = ['06','07','08','09', '10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
    timetable.index = timetable['Time']

    # Fill dataframe by row and column
    for day in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
        for time in timetable['Time']:

            # Check query of something exists in vw_week_calender, if not return '#####'
            clause = 'day = \''+str(day)+'\' and start <= \'' + str(time) + ':00:00\' and end > \'' + str(time) + ':00:00\' '
            val = util.sql_to_dataframe('vw_week_calendar', 'timetable', password, config, where = clause)
            if not val.empty:
                text = str(val.loc[0][0] + '-' + val.loc[0][1]).center(width_col,' ')
            else:
                text = '######'.center(width_col, ' ')
            timetable[day][time] = text #setting the value

            # Re-print the page
            os.system('clear')
            pyfiglet.print_figlet('Timetable', colors=config[3][1])
            print(timetable.to_string(index=False, col_space=[4, width_col, width_col, width_col, width_col, width_col, width_col, width_col], justify='center', max_colwidth=width_col))
            print('Press any key to return')

    response = readchar.readkey()
    return response

