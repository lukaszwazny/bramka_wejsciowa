import logging
import json
import requests

from shared_code import database
from shared_code.helpers import safe_list_get, get_key, get_url, send_user_to_app, send_not_opening_command
from shared_code.getters import get_active_user

import azure.functions as func
import Function1


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    identificator_nr = req.params.get('identificator_nr')

    if identificator_nr:
        try:
            resp = get_active_user(identificator_nr)

            if send_user_to_app(resp).status_code != 200:
                raise Exception()

            if (resp.get('user_id') == None) and (resp.get('ID') == None):
                if send_not_opening_command().status_code != 200:
                    raise Exception()

            if type(resp) is Exception:
                raise resp
            else:
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