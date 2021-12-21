import logging
import os
import fdb
import psycopg2

from shared_code.helpers import safe_list_get

def connect():
    logging.info('Getting env variables')
    host = os.environ['host']
    database = os.environ['database']
    user = os.environ['user']
    password = os.environ['password']
    logging.info('Got env variables')

    logging.info('Connecting to database')
    con = fdb.connect(
        host=host, database=database,
        user=user, password=password, charset='UTF8'
    )
    logging.info('Connected to database succesfully')

    return con.cursor()

def connectPostgres():
    logging.info('Getting env variables')
    host = os.environ['hostPostgres']
    database = os.environ['databasePostgres']
    user = os.environ['userPostgres']
    password = os.environ['passwordPostgres']
    sslmode = 'require'
    logging.info('Got env variables')

    conn_string = f'host={host} user={user} dbname={database} password={password} sslmode={sslmode}'

    logging.info('Connecting to database')
    con = psycopg2.connect(conn_string)
    logging.info('Connected to database succesfully')

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
