import logging
import azure.functions as func
import fdb
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        logging.info('Connecting to database')
        con = fdb.connect(
            host='51.105.135.4', database='/firebird/data/Fitnes.fdb',
            user='sysdba', password='masterkey', charset='UTF8'
        )
        logging.info('Connected to database succesfully')

        logging.info('Getting data')
        cur = con.cursor()
        cur.execute("select * from clanovi")
        names = [item[0] for item in cur.description]
        resp = cur.fetchall()
        resp = json.dumps([{names[i]:item[i] for i in range(len(names))} for item in resp], default=str, ensure_ascii=False)
        logging.info('Got data succesfully')

        return func.HttpResponse(
                resp,
                status_code=200,
                mimetype='application/json'
            )

    except fdb.DatabaseError as err:
        logging.info('Database error :(')
        return func.HttpResponse(
             err.args[0],
             status_code=500
        )
    
    except Exception as ex:
        logging.info('Unknown error')
        logging.info(ex)
        return func.HttpResponse(
             "Unknown error",
             status_code=400
        )
