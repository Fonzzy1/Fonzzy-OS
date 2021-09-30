import string

import numpy as np
import pandas
import pandas as pd
import sqlalchemy
import notion.client

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


def int_to_dict(int):
    """
    allows for indexes to be converted to unique characters
    """
    ls_char = list(string.printable)
    ls_char.remove('n')
    ls_char.remove('b')  # remove n and b to work with projects page
    char = ls_char[int]
    return char


def dict_to_int(str):
    """"
    returns  char to relevant index

    """
    ls_char = list(string.printable)
    ls_char.remove('n')
    ls_char.remove('b')  # remove n and b to work with projects page
    index = ls_char.index(str)
    return index


def get_notion_jobs(password, config):
    SQL_Username = config[0][1]
    SQL_driver = config[4][1]
    db_connection_str = SQL_driver + '://' + SQL_Username + ':' + password + '@localhost/timetable'
    engine = sqlalchemy.create_engine(db_connection_str)
    work_index = engine.execute('select work_index()').fetchall()[0][0]

    jobs = pd.DataFrame(columns=['id', 'project', 'description', 'length', 'due_date', 'index_score'])
    client = notion.client.NotionClient(token_v2=config[5][1])

    cv = client.get_collection_view(config[6][1])

    for row in cv.collection.get_rows(search=config[7][1]):
        if not row.status in ('done','Paused/Blocked'):
            jobs.loc[len(jobs)] = np.array(['jw_' + str(len(jobs)), 'Work', row.name, row.priority, None, work_index])

    return jobs


def sm_done_notion(name, password, config):
    client = notion.client.NotionClient(token_v2=config[5][1])

    cv = client.get_collection_view(config[6][1])
    for row in cv.collection.get_rows(search=name):
        row.done = True
        row.status = 'done'
