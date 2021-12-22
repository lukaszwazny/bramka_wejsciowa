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
        justification = req_body.get('justification')
        if justification:
            #to do rozkaz otwarcia do urządzenia

            date = datetime.now().astimezone().date()
            hour = datetime.now().astimezone().timetz()

            cur = database.connectPostgres()
            query = f"INSERT INTO public.\"Entrance\"(datetime, mode, justification) VALUES ('{datetime.combine(date, hour).strftime('%Y-%m-%d %H:%M:%S %z')}', 'WEJŚCIE', '{justification}')"
            cur.execute(query)
            cur.execute("COMMIT")
        else:
            return func.HttpResponse(
                "Nie podano uzasadnienia!",
                status_code=400
            )

        return func.HttpResponse(
            "OK",
            status_code=200
        )
            
    except Exception as ex:
        logging.info('Unknown error')
        logging.info(ex)
        resp=json.dumps(req_body, ensure_ascii=False)
        return func.HttpResponse(
            resp,
            status_code=400
        )