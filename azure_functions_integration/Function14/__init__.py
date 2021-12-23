import logging
import json
import requests
from datetime import datetime, timedelta, time
import locale
import calendar

from shared_code import database
from shared_code.helpers import safe_list_get, get_key, get_url

import azure.functions as func
import Function7

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')

    try:

        cur = database.connectPostgres()
        query = f"SELECT * FROM public.\"Entrance\" e LEFT OUTER JOIN public.\"Lesson_type\" l ON e.lesson_type_id = l.lesson_type_id ORDER BY datetime DESC"
        entrances = database.getMany(cur, query)
        for idx, entr in enumerate(entrances):
            params = dict(
                code=get_key(),
                identificator_nr=entr.get('identificator_nr')
            )
            fun7_req = func.HttpRequest('get', '', params=params, body='')
            resp = json.dumps(Function7.main(fun7_req).get_body())
            entrances[idx] = dict(
                id=entr.get('entrance_id'),
                date=entr.get('datetime').date(),
                hour=entr.get('datetime').time(),
                name=resp.get('name') + ' ' + resp.get('surname'),
                lesson_type=entr.get('name'),
                role=entr.get('role_name'),
                mode=entr.get('mode')
            )
        
        entrances = json.dumps(entrances, default=str, ensure_ascii=False)
        return func.HttpResponse(
                entrances,
                status_code=200,
                mimetype='application/json'
            )
    
    except Exception as ex:
        logging.info('Unknown error')
        logging.info(ex)
        return func.HttpResponse(
            "Unknown error",
            status_code=400
        )