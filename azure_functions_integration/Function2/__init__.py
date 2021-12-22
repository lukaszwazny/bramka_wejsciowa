import logging
import fdb
import json
import random

from shared_code import database
from shared_code.helpers import safe_list_get

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    identificator_nr = req.params.get('identificator_nr')
    date = req.params.get('date')

    if identificator_nr and date:
        try:

            cur = database.connect()
            query = f"SELECT u.ID as ID, p.NAZIV, u.BROJTRENINGA, u.BROJDOLAZAKA FROM UPLATE u LEFT OUTER JOIN PROGRAMI p ON u.PROGRAMID = p.ID RIGHT OUTER JOIN CLANOVI c ON c.ID = u.KORISNIKID WHERE c.MEMBERID='{identificator_nr}' AND '{date}' BETWEEN u.DATUMOD AND u.DATUMDO"

            resp = database.getMany(cur, query)
            if not resp:
                resp=json.dumps({'entrance_allowed': False, 'message': 'Brak aktywnego karnetu!'}, ensure_ascii=False)
                return func.HttpResponse(
                    resp,
                    status_code=400,
                    mimetype='application/json'
                )

            active_packages = [{'ID':package['ID'], 'NAME':package['NAZIV']} for package in resp if package['BROJTRENINGA'] - package['BROJDOLAZAKA'] != 0]
            if not active_packages:
                resp=json.dumps({'entrance_allowed': False, 'message': 'Wykorzystano wszystkie wejścia!'}, ensure_ascii=False)
                return func.HttpResponse(
                    resp,
                    status_code=400,
                    mimetype='application/json'
                )  
            
            package = random.choice(active_packages)
            resp=json.dumps({'entrance_allowed': True, 'package_ID': package['ID'], 'package_name': package['NAME']}, ensure_ascii=False)
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
                status_code=401
            )
    else:
        return func.HttpResponse(
             "Nie podano nr identyfikatora lub daty wejścia!",
             status_code=401
        )