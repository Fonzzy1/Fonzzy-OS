import os
import sys
import util
import pandas
import pyfiglet
import getpass
from main import mainpage

def start():
    """
    start funtion for the os

    decrypts the config files


    """

    try:
        os.chdir('/home/fonzzy/Documents/ssh-mate/config')
        test = pandas.read_csv('config.csv')
        test.iloc[1,1]
    
    except IndexError:
        p = getpass.getpass()
    
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
    	    util.decrypt(f,p)
    
    
    mainpage()

if __name__ == "__main__":
    start()
