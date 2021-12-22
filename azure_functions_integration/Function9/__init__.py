import logging
import json
from datetime import datetime
import requests

from shared_code import database
from shared_code.helpers import safe_list_get, get_url, get_key

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        identificator_nr = req_body.get('identificator_nr')

        if identificator_nr:

            date = datetime.now().astimezone().date()
            hour = datetime.now().astimezone().timetz()

            url = get_url() + 'Function5?code=' + get_key()
            data = dict(
                identificator_nr=identificator_nr,
                date=date.strftime('%Y-%m-%d'),
                hour=hour.strftime('%H:%M:%S')
            )
            resp = requests.request("PATCH", url, headers={'Content-Type': 'application/json'}, data=json.dumps(data, ensure_ascii=False))

            cur = database.connectPostgres()
            query = f"INSERT INTO public.\"Entrance\"(datetime, mode, identificator_nr) VALUES ('{datetime.combine(date, hour).strftime('%Y-%m-%d %H:%M:%S %z')}', 'WYJŚCIE', '{identificator_nr}')"
            cur.execute(query)
            cur.execute("COMMIT")

            resp=json.dumps({'identificator_nr': identificator_nr, 'date': date, 'hour': hour},default=str, ensure_ascii=False)
            return func.HttpResponse(
                resp,
                status_code=200,
                mimetype='application/json'
            )

        else:
            return func.HttpResponse(
                "Nie podano nr identyfikatora!",
                status_code=400
            )
            
    except Exception as ex:
        logging.info('Unknown error')
        logging.info(ex)
        resp=json.dumps(req_body, ensure_ascii=False)
        return func.HttpResponse(
            resp,
            status_code=200
        )