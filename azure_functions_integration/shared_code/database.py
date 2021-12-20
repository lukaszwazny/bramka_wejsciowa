import logging
import os
import fdb

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