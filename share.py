import os
import datetime


def email(file_name):
    if os.path.isdir( '../' + file_name):
        os.system('zip -r '+file_name+'.zip ../'+file_name)
        os.system('mutt -a \'' + file_name +  '.zip\'')
        os.system('rm '+file_name+ '.zip')
    elif os.path.isfile(file_name):
        os.system('mutt -a \'' + file_name +  '\'')
