""" base repository module """
import os

QUERY_CREATE_LOG_TABLE = 'create_log_table'

def get_query(query):
    """ gets a query by file name """
    file_name = os.path.dirname(__file__) +  '/queries/' + query + '.sql'
    with open(file_name, 'r') as query_file:
        sql = query_file.read()

    return sql

def execute_multi_commands(cursor, sql):
    """ executes a script with multiple commands """
    sql = sql.replace(';', ' GO ')
    commands = sql.split('GO')

    for command in commands:
        cursor.execute(command)

    cursor.commit()
