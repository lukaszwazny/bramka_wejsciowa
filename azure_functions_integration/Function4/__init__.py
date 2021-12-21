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
        lesson = req_body.get('lesson')
        package = req_body.get('package_id')

        if identificator_nr and date and hour and package:

            cur = database.connect()
            query = f"SELECT ID FROM CLANOVI WHERE MEMBERID='{identificator_nr}'"

            resp = database.getOne(cur, query)
            if not resp:
                return func.HttpResponse(
                    "Nie ma użytkownika o podanym ID!",
                    status_code=400
                )
            member_id = resp['ID']

            query = f"SELECT * FROM DOLASCI WHERE DATUM='{date}' AND KORISNIKID = {member_id} AND DATEDIFF(MINUTE FROM CAST(VREMEDOLASKA AS TIME) TO CAST('{hour}' AS TIME)) < 60"
            resp = database.getMany(cur, query)
            if resp:
                return func.HttpResponse(
                    json.dumps(resp, default=str, ensure_ascii=False),
                    status_code=200
                )

            cur.execute(f"INSERT INTO DOLASCI (DATUM, KORISNIKID, VREMEDOLASKA, UPLATAID) VALUES('{date}',{member_id}, '{hour}', {package})")
            cur.execute(f"UPDATE UPLATE SET BROJDOLAZAKA = BROJDOLAZAKA + 1 WHERE ID={package}")
            cur.execute(f"COMMIT")

            resp=json.dumps({'identificator_nr': identificator_nr, 'date': date, 'hour': hour, 'lesson': lesson, 'package_id': package }, ensure_ascii=False)
            return func.HttpResponse(
                resp,
                status_code=200,
                mimetype='application/json'
            )

        else:
            return func.HttpResponse(
                "Nie podano nr identyfikatora lub daty lub godziny wejścia lub karnetu!",
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