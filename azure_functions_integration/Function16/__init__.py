import logging
import json
import requests
from datetime import datetime, timedelta, time
import locale
import calendar

from shared_code import database
from shared_code.helpers import safe_list_get, get_key, get_url
from shared_code.getters import get_active_users

import azure.functions as func
import Function6

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')

    try:

        fun6_req = func.HttpRequest('get', '', params={}, body='')
        resp = json.loads(Function6.main(fun6_req).get_body())
        logging.info('Got outer users')

        cur = database.connectPostgres()
        query = f'SELECT u.user_id, u.identificator_nr, u.name, u.surname, ARRAY_AGG(DISTINCT r.role_name) AS roles FROM public."User" u LEFT OUTER JOIN public.\"Role_User\" ru ON ru.\"User_user_id\"=u.user_id JOIN public.\"Role\" r ON r.role_id=ru.\"Role_role_id\" WHERE u.is_active AND r.is_active GROUP BY u.user_id'
        resp_new = database.getMany(cur, query)
        logging.info('Got inner users')

        for idx, r in enumerate(resp):
            for d in resp_new:
                if d['identificator_nr']==r['identificator_nr']:
                    d['roles'] = d['roles'] + r['roles']
                    resp.pop(idx)
        logging.info('Concatenated roles of users')
        
        users = resp + resp_new
        logging.info('Concatenated users')
        
        users = json.dumps(users, default=str, ensure_ascii=False)
        return func.HttpResponse(
                users,
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