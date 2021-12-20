import logging
import fdb
import json

from shared_code import database
from shared_code.helpers import safe_list_get

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        identificator_nr = req_body.get('identificator_nr')
        date = req_body.get('date')
        hour = req_body.get('hour')

        if identificator_nr and date and hour:

            cur = database.connect()

            cur.execute(f"SELECT ID FROM CLANOVI WHERE MEMBERID='{identificator_nr}'")
            names = [item[0] for item in cur.description]
            resp = cur.fetchone()
            resp = {names[i]:safe_list_get(resp, i, None) for i in range(len(names))}
            if not resp:
                return func.HttpResponse(
                    "Nie ma użytkownika o podanym ID!",
                    status_code=400
                )
            member_id = resp['ID']

            cur.execute(f"SELECT * FROM DOLASCI WHERE DATUM='{date}' AND KORISNIKID = {member_id} ORDER BY CAST(VREMEDOLASKA AS TIME) DESC")
            names = [item[0] for item in cur.description]
            resp = cur.fetchone()
            resp = {names[i]:safe_list_get(resp, i, None) for i in range(len(names))}

            cur.execute(f"UPDATE DOLASCI SET VREMEODLASKA = '{hour}' WHERE ID={resp['ID']}")
            cur.execute(f"COMMIT")

            resp=json.dumps({'identificator_nr': identificator_nr, 'date': date, 'hour': hour}, ensure_ascii=False)
            return func.HttpResponse(
                resp,
                status_code=200,
                mimetype='application/json'
            )

        else:
            return func.HttpResponse(
                "Nie podano nr identyfikatora lub daty lub godziny wejścia!",
                status_code=400
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