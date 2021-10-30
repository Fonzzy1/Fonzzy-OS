import string
from collections import Counter
import re
import numpy as np
import pandas
import sqlalchemy
import notion.client
from cryptography.fernet import Fernet
import base64, hashlib
import os
import pyfiglet
import readchar
import math
'''
set of functions to make everything a bit cleaner
'''



def sm_done_recurring(task_id, password, config):
    """
    sets job done for tbl_jobs recurring

    task_id(int): the value in the id collum in tbl_jobs_recuring
    password(str): sql database password
    config(dataframe): config dataframe for username and driver

    returns: nothing
    """
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update tbl_jobs_recurring set last_date = last_date + interval redo_time week where id = ' + str(id)
    connection.execute(query)


def sm_done_due(task_id, password, config):
    """
    sets job done for tbl_jobs due

    task_id(int): the value in the id collum in tbl_jobs_due
    password(str): sql database password
    config(dataframe): config dataframe for username and driver

    returns: nothing
    """
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update tbl_jobs_due set done = 1 where id = ' + str(id)
    connection.execute(query)


def sm_done_not_due(task_id, password, config):
    """
    sets job done for tbl_jobs_not_due

    task_id(int): the value in the id collum in tbl_jobs_not_due
    password(str): sql database password
    config(dataframe): config dataframe for username and driver

    returns: nothing
    """
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update tbl_jobs_not_due set done = 1 where id = ' + str(id)
    connection.execute(query)


def sql_to_dataframe(table_name, database, password, config, where=''):
    """
    table_name(str): the table we want to reads
    database(str): the database that contains the table
    password(str): sql database password
    config(dataframe): config dataframe for username and driver
    where(str, default = ''): where statement for select, if left empty then returns the whole table

    returns: df(dataframe): the selected sql table
    """
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

def fuzzy_find(ls,string):
    """
    Takes in list of objects that need to be fuzzy found
    Takes in search string

    Returns the shortest noncommon input string
    """

    ## Encode the strings into shortest
    # Clean the strings
    ls = [x.lower() for x in ls]
    encode = [''] * len(ls)
    leftover = ls.copy()
    for i,e in enumerate(ls):
        ls[i] = re.sub('[^a-z0-9\.]','',e)
        encode[i] = ls[i][0]
        leftover[i] = leftover[i][1:]
    ## For elements that have a non unique firtst character
    non_d =  [k for (k,v) in Counter(encode).items() if v > 1]
    ## Builidng stings one element at a time therefore  while loop
    while non_d:
        for e in non_d:
            # Get the remaining string 
            index = [i for (i,x) in enumerate(encode) if x == e]
            rem_string = [ (i,x+str(i)) for (i,x) in enumerate(leftover) if i in index] 
            cur_element_count = 0
            max_len = max([len(x) for (i,x) in rem_string])
            # Get first unique char
            j = -1
            while cur_element_count < 1:
                j += 1
                cur_element = [ x[1].ljust(max_len)[j] for x in rem_string]
                cur_element_count =  len([k for (k,v) in Counter(cur_element).items() if v < len(cur_element) ])
            #Add unique char to the encoding string
            for (i,x) in rem_string:
                try:
                    encode[i] += x.ljust(max_len)[j]
                    leftover[i] = leftover[i][j:]
                except IndexError:
                    pass

        non_d =  [k for (k,v) in Counter(encode).items() if v > 1]

    ## Now match encoding to current string
    string= re.sub('[^a-z0-9\.]','',string.lower())
    l = len(string)
    match_encode = [(i,x[l:]) for (i,x) in enumerate(encode) if x[:l] == string]
    match_string= [(i,(x+' ')[x.index(string)+l]) for (i,x) in enumerate(ls) if string in x and i not in [i for (i,x) in match_encode]]
    match = match_encode + match_string
    return match
    
def fuzzy_loop(header, in_list):

    """
    Looping funtion for fuzzy find
    Returns index of inpit list 
    """
    q = 0
    ss = ''
    hold = fuzzy_find(in_list,ss)
    c = False
    while not c:
        #Print header
        os.system('clear')
        pyfiglet.print_figlet(header, colors="GREEN")
        
        
        h = (os.get_terminal_size()[1] - 6) * 3/4
        w = os.get_terminal_size()[0]
        
        print(ss)
        print( '-' * w)
        index = hold.copy()
        
        col_array = np.full(len(in_list),' '* (max(max([len(x) for x in in_list]),1)+20))
        
        
        try:
            max_len = max(max([len(x) for i,x in index]),1)
        except ValueError:
            max_len = 1
        for i,e  in enumerate(in_list):
            if i in [i for i,x in index]:
                x = [x for j,x in index if j == i][0]
                if i == index[q][0]:
                    col_array[i] = str((x.ljust(1))[0] + ': \033[42;35m ' + in_list[i] + ' \033[m  ')
                else:
                    col_array[i] = str((x.ljust(1))[0] + ': \033[44;33m ' + in_list[i] + ' \033[m  ')
            else:
                x = ' '
                col_array[i] = str((x.ljust(1))[0] + ': '+ in_list[i] )
         

        cols  = math.ceil(len(col_array)/h)
        rows = math.ceil(len(col_array)/cols)
        pad = cols * rows - len(col_array)
        print_array = np.reshape(np.pad(col_array,(0,pad), constant_values=''), (cols,rows)).T
        for row in print_array:
            printline = ''
            for col in row:
                printline += col +  (math.floor(w/cols)-len(re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])','',col)))*' '         	
            print(printline)


        key = readchar.readkey()
        
        if '\x1b' in key:
            alt = '\x1b'
        else:
            alt = ''

        if '\r' in key:
            c = True
        elif key == '\x1b\x1b':
            return 'exit'
        elif key == '\x7f':
            ss = ss[0:len(ss) -1]
            q = 0
            hold = fuzzy_find(in_list,ss)
        elif key == '\x1b[A':
            q -= 1
            q = q % len(index)        
        elif key == '\x1b[B':
            q += 1
            q = q % len(index) 
        else:
            ss += key
            hold = fuzzy_find(in_list,ss)
            q = 0
    
    
    return [index[q][0],alt]
    


        


       

def int_to_dict(int):
    """
    allows for indexes to be converted to unique characters
    """
    ls_char = list(string.printable)
    ls_char.remove('n')
    ls_char.remove('b')  # remove n and b to work with projects page
    ls_char.remove('m')
    ls_char.remove('g')
    ls_char.remove('o')
    ls_char.remove('\\')
    char = ls_char[int]
    return char


def dict_to_int(str):
    """"
    returns  char to relevant index

    """
    ls_char = list(string.printable)
    ls_char.remove('n')
    ls_char.remove('b')  # remove n and b to work with projects page
    ls_char.remove('m')
    ls_char.remove('g')
    ls_char.remove('o')
    ls_char.remove('\\')
    index = ls_char.index(str)
    return index


def get_work(password, config):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable'
    engine = sqlalchemy.create_engine(db_connection_str)
    connection = sqlalchemy.create_engine(db_connection_str)
    
    work_index = engine.execute('select 1 - sum(index_score) from vw_jobs').fetchall()[0][0]

    jobs = pandas.DataFrame(columns=['id', 'project', 'description', 'index_score'])
    ls = pandas.read_sql_table('tbl_jobs_work', con=connection)
    
    for index,row in ls.iterrows():
        jobs.loc[len(jobs)] = ['jw_'+str(row['id']),'Work',row['description'],work_index]


    return jobs


def done_work(id, password, config):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable'
    connection = sqlalchemy.create_engine(db_connection_str)
    task_id = int("".join(filter(str.isdigit, id)))
    query = 'delete from tbl_jobs_work where id = ' + str(task_id)
    connection.execute(query)
        
        
def encrypt(filename, p):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    my_password = p.encode()
    key_int = hashlib.md5(my_password).hexdigest()
    key = base64.urlsafe_b64encode(key_int.encode("utf-8"))
    
    f = Fernet(key)

    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()

    # encrypt data
    encrypted_data = f.encrypt(file_data)

    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, p):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    my_password = p.encode()
    key_int = hashlib.md5(my_password).hexdigest()
    key = base64.urlsafe_b64encode(key_int.encode("utf-8"))
    
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
