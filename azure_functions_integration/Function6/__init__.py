import logging
import fdb
import json

from shared_code import database, convert
from shared_code.helpers import safe_list_get

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:

        cur = database.connect()

        logging.info('Getting data')
        cur.execute(f"select * from clanovi")
        logging.info('Got data succesfully')

        logging.info('Converting data')
        names = [item[0] for item in cur.description]
        resp = cur.fetchall()
        resp = [{names[i]:safe_list_get(item, i, None) for i in range(len(names))} for item in resp]
        resp = [convert.convertClanoviToUser(item) for item in resp]
        resp = [{'identicator_nr':item['identificator_nr'], 'name': item['name'], 'surname':item['surname'], 'roles': ['KLIENT']} for item in resp]
        resp = json.dumps(resp, default=str, ensure_ascii=False)
        logging.info('Converted data succesfully')

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