import logging
import json
import requests
from datetime import datetime, timedelta, time
import locale
import calendar

from shared_code import database
from shared_code.helpers import safe_list_get, get_key, get_url
from shared_code.getters import get_user

import azure.functions as func
import Function7

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    entrance_id = req.params.get('entrance_id')

    try:

        cur = database.connectPostgres()
        query = f"SELECT * FROM public.\"Entrance\" e LEFT OUTER JOIN public.\"Lesson_type\" l ON e.lesson_type_id = l.lesson_type_id WHERE e.entrance_id={entrance_id}"
        entrance = database.getOne(cur, query)
        if not entrance.get('entrance_id'):
            entrance = dict(
                id=None,
                date=None,
                hour=None,
                name=None,
                lesson_type=None,
                role=None,
                mode=None,
                package=None,
                justification=None
            )
        else:
            resp = get_user(entrance.get('identificator_nr'))
            if not resp or type(resp) is Exception():
                resp = dict(
                    name=' ',surname=' '
                )
            else:
                if not resp.get('name'): resp['name'] = ' '
                if not resp.get('surname'): resp['surname'] = ' '
            entrance = dict(
                id=entrance.get('entrance_id'),
                date=entrance.get('datetime').date(),
                hour=entrance.get('datetime').time(),
                name=resp.get('name', ' ') + ' ' + resp.get('surname',' '),
                lesson_type=entrance.get('name'),
                role=entrance.get('role_name'),
                mode=entrance.get('mode'),
                package=entrance.get('package'),
                justification=entrance.get('justification')
            )
            
        entrance = json.dumps(entrance, default=str, ensure_ascii=False)
        return func.HttpResponse(
                entrance,
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