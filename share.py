import os
import datetime

def upload(file_name):
    if os.path.isdir( '../' + file_name):
        os.system('cp -R ../' +file_name + '  /home/fonzzy/Documents/pics-and-pdfs/' + file_name)
    elif os.path.isfile(file_name):
        os.system('cp ' +file_name + ' /home/fonzzy/Documents/pics-and-pdfs/' + file_name)
    cur_dir = os.getcwd()
    os.chdir('/home/fonzzy/Documents/pics-and-pdfs')
    os.system('git pull')
    os.system('git add .')
    os.system("git commit -m 'added " +file_name + "'" )
    os.system('git push')
    os.chdir(cur_dir)

def email(file_name):
    if os.path.isdir( '../' + file_name):
        os.system('zip -r '+file_name+'.zip ../'+file_name)
        os.system('mutt -a \'' + file_name +  '.zip\'')
        os.system('rm '+file_name+ '.zip')
    elif os.path.isfile(file_name):
        os.system('mutt -a \'' + file_name +  '\'')
