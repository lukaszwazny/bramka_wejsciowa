from logging import info
from os import environ
from fdb import connect as fdbConnect
from psycopg2 import connect as postgresConnect

from shared_code.helpers import safe_list_get

def connect():
    info('Getting env variables')
    host = environ['host']
    database = environ['database']
    user = environ['user']
    password = environ['password']
    info('Got env variables')

    info('Connecting to database')
    con = fdbConnect(
        host=host, database=database,
        user=user, password=password, charset='UTF8'
    )
    info('Connected to database succesfully')

    return con.cursor()

def connectPostgres():
    info('Getting env variables')
    host = environ['hostPostgres']
    database = environ['databasePostgres']
    user = environ['userPostgres']
    password = environ['passwordPostgres']
    sslmode = 'require'
    info('Got env variables')

    conn_string = f'host={host} user={user} dbname={database} password={password} sslmode={sslmode}'

    info('Connecting to database')
    con = postgresConnect(conn_string)
    info('Connected to database succesfully')

    return con.cursor()

def getMany(cur, query):
    cur.execute(query)
    names = [item[0] for item in cur.description]
    resp = cur.fetchall()
    resp = [{names[i]:safe_list_get(item, i, None) for i in range(len(names))} for item in resp]
    return resp

def getOne(cur, query):
    cur.execute(query)
    names = [item[0] for item in cur.description]
    resp = cur.fetchone()
    resp = {names[i]:safe_list_get(resp, i, None) for i in range(len(names))}
    return resp
