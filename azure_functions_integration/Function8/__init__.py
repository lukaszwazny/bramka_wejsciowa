import logging
import json
import requests
from datetime import datetime, timedelta, time
import locale
import calendar

from shared_code import database
from shared_code.helpers import safe_list_get, get_key, get_url

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    identificator_nr = req.params.get('identificator_nr')

    if identificator_nr:
        try:

            cur = database.connectPostgres()
            query = f"SELECT * FROM public.\"Entrance\" WHERE mode = \'WYJŚCIE\' AND identificator_nr=\'{identificator_nr}\' ORDER BY e.datetime DESC"  
            last_entr_datetime = database.getOne(cur, query).get('datetime')

            query = f"SELECT * FROM public.\"Parameter\" WHERE name=\'Parametr x\'"
            x = database.getOne(cur, query).get('value')
            if not x:
                return func.HttpResponse(
                    "Nie można odczytać parametru x",
                    status_code=400
                )

            if last_entr_datetime and ((datetime.now().astimezone() - last_entr_datetime).total_seconds()/60) < x:
                query = f"SELECT * FROM public.\"Entrance\" WHERE mode = \'WEJŚCIE\' AND identificator_nr=\'{identificator_nr}\' ORDER BY e.datetime DESC"
                last_entr = database.getOne(cur, query)
                if last_entr and last_entr.get('lesson_type_id'):
                    locale.setlocale(locale.LC_ALL, 'pl_PL')
                    weekday_name_now = calendar.day_name[datetime.now().astimezone().weekday()].upper()
                    query = f"SELECT * FROM public.\"Lesson\" WHERE lesson_type_id={last_entr.get('lesson_type_id')} AND weekday=\'{weekday_name_now}\' AND is_active"
                    lesson = database.getOne(cur, query)
                    if lesson and lesson.get('start_time') < datetime.now().astimezone().timetz() < lesson.get('end_time'):
                        #to do - wyślij wejścia do apki
                        resp = 'siema'
                    else:
                        resp = funtion7(identicator_nr)
                else:
                    #to do - wyślij wejścia do apki
                    resp = 'siema'
            else:
                resp = funtion7(identificator_nr)
            
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

def funtion7(identicator_nr):
    url = get_url() + 'Function7'
    params = dict(
        code=get_key(),
        identificator_nr=identificator_nr
    )
    resp = requests.get(url=url, params=params).json()
    resp = json.dumps(resp, default=str, ensure_ascii=False)
    return resp