import logging
import fdb
import json

from shared_code import database, convert
from shared_code.helpers import safe_list_get

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    identificator_nr = req.params.get('identificator_nr')

    if identificator_nr:
        try:

            cur = database.connect()
            query = f"select * from clanovi right outer join mesta on clanovi.mestoid = mesta.id where memberid='{identificator_nr}'"

            resp = database.getOne(cur, query)
            resp = convert.convertClanoviToUser(resp)
            resp['roles'] = []
            if resp['ID']:
                resp['roles'].append('KLIENT')     
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
    else:
        return func.HttpResponse(
             "Nie podano nr identyfikatora!",
             status_code=400
        )