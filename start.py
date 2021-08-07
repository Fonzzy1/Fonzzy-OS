import os
import sys
import util
import pandas
import pyfiglet
from main import main_page

def start():
    """
    start funtion for the os

    takes in the config file and read it to a dataframe

    user inputs sql password, database is then pinged to see if password is correct

    """
    os.system('clear')
    os.chdir(os.path.dirname(sys.argv[0]))
    config = pandas.read_csv('./config/config.csv').values
    pyfiglet.print_figlet(config[2][1] + '\'s Dashboard', colors=config[3][1])
    while True:
        try:
            password = input('Password: ')
            util.sql_to_dataframe('tbl_jobs_due', 'timetable', password, config)
            break
        except Exception as e:
            print("Oops!  That not the password.  Try again...")
    main_page(password)

if __name__ == "__main__":
    start()