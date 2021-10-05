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
    p = getpass.getpass()
    
    os.chdir(os.path.dirname(sys.argv[0]) + '/config')
    
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
    	util.decrypt(f,p)
    
    
    mainpage()

if __name__ == "__main__":
    start()
