import logging
import json
import requests
from datetime import datetime, timedelta, time
import locale
import calendar

from shared_code import database
from shared_code.helpers import safe_list_get, get_key, get_url

import azure.functions as func
import Function2


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    identificator_nr = req.params.get('identificator_nr')
    role = req.params.get('role')

    if identificator_nr and role:
        try:
            response = dict(
                identificator_nr= identificator_nr,
                role= role,
                package= None,
                justification= None,
                reason_of_disallowance= None
            )

            if role == 'KLIENT':
                date = datetime.now().astimezone().date()
                params = dict(
                    code=get_key(),
                    identificator_nr=identificator_nr,
                    date=date
                )
                fun2_req = func.HttpRequest('get', '', params=params, body='')
                resp = Function2.main(fun2_req)
                if resp.status_code != 200:
                    #to do wyślij rozkaz nieotwarcia
                    if resp.status_code == 400:
                        response['reason_of_disallowance'] = json.loads(resp.get_body()).get('message', 'Nieznany powód :(')
                    else:
                        response['reason_of_disallowance'] = 'Nieznany powód :('
                else:
                    response['package'] = dict(
                        package_ID= json.loads(resp.get_body()).get('package_ID'), 
                        package_name= json.loads(resp.get_body()).get('package_name')
                    )
            elif role == 'TRENER' or role == 'PRACOWNIK RECEPCJI' or role ==  'ADMINISTRATOR':
                response = response
            elif role == 'WIDZ':
                cur = database.connectPostgres()
                query = f"SELECT * FROM public.\"Justification\" WHERE is_active AND user_id = (SELECT user_id FROM public.\"User\" WHERE identificator_nr='{identificator_nr}' AND is_active) AND '{datetime.now().astimezone().date().strftime('%Y-%m-%d')}' BETWEEN \"from\" AND \"to\""
                justification = database.getOne(cur, query)
                if justification.get('justification_id'):
                    response['justification'] = dict(
                        id= justification.get('justification_id'),
                        name= justification.get('name'),
                        description = justification.get('description')
                    )
                else:
                    #to do wyślij rozkaz nieotwarcia
                    response['reason_of_disallowance'] = 'Brak uprawnień do wejścia'
            else:
                response['reason_of_disallowance'] = 'Nieznany powód :('
            
            response = json.dumps(response, default=str, ensure_ascii=False)
            return func.HttpResponse(
                    response,
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
             "Nie podano nr identyfikatora lub roli!",
             status_code=400
        )