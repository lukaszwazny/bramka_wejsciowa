import logging
import json
import requests

from shared_code import database
from shared_code.helpers import safe_list_get, get_key, get_url

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    identificator_nr = req.params.get('identificator_nr')

    if identificator_nr:
        try:
            url = get_url() + 'Function1'
            params = dict(
                code=get_key(),
                identificator_nr=identificator_nr
            )
            resp = requests.get(url=url, params=params).json()

            cur = database.connectPostgres()
            cur.execute(f'SELECT * FROM public."User" WHERE identificator_nr = \'{identificator_nr}\' AND is_active')
            names = [item[0] for item in cur.description]
            resp_new = cur.fetchone()
            for i in range(len(names)):
                if safe_list_get(resp_new, i, None):
                    resp[names[i]] = safe_list_get(resp_new, i, None)

            if resp.get('user_id'):
                query = f"SELECT * FROM public.\"Role_User\" RIGHT OUTER JOIN public.\"Role\" ON role_id = \"Role_role_id\"  WHERE \"User_user_id\" = {resp['user_id']} AND is_active"
                resp_new = database.getMany(cur, query)
                resp_new = [item['role_name'] for item in resp_new]
                resp['roles'] = resp['roles'] + list(set(resp_new))

            #to do - rozkaz do apki webowej i urządzenia

            resp = json.dumps(resp, default=str, ensure_ascii=False)
            return func.HttpResponse(
                resp,
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
    else:
        return func.HttpResponse(
             "Nie podano nr identyfikatora!",
             status_code=400
        )