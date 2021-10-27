import string
from collections import Counter
import re
import numpy as np
import pandas
import sqlalchemy
import notion.client
from cryptography.fernet import Fernet
import base64, hashlib

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
    for i,e in enumerate(ls):
        ls[i] = re.sub('[^a-z0-9\.]','',e)
        encode[i] = ls[i][0]
    ## For elements that have a non unique firtst character
    non_d =  [k for (k,v) in Counter(encode).items() if v > 1]
    ## Builidng stings one element at a time therefore  while loop
    while non_d:
        for e in non_d:
            # Get the remaining string 
            rem_string = [(i,x[len(e):]) for (i,x) in enumerate(ls) if x[0:len(e)] == e]
            cur_element_count = len(rem_string)
            max_len = max([len(x) for (i,x) in rem_string])
            # Get first unique char
            j = -1
            while cur_element_count:
                j += 1
                cur_element = [x[1].ljust(max_len)[j] for x in rem_string]
                cur_element_count =  len([k for (k,v) in Counter(cur_element).items() if v > 1])
            #Add unique char to the encoding string
            for (i,x) in rem_string:
                try:
                    encode[i] += x[j]
                except IndexError:
                    pass

        non_d =  [k for (k,v) in Counter(encode).items() if v > 1]

    ## Now match encoding to current string 
    l = len(string)
    match = [(i,x[l:]) for (i,x) in enumerate(encode) if x[:l] == string]
    # Retun matches - hidden files only return if begin with '.'
    # Remove string that has already been inputted
    if l == 0:
        match = [(i,x) for (i,x) in enumerate(encode) if x[0] != '.']
    return match
        


       

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
    
    work_index = engine.execute('select work_index()').fetchall()[0][0]

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
