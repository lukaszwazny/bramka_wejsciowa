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
    date = datetime.now().astimezone().date()
    hour = datetime.now().astimezone().timetz()

    try:

        cur = database.connectPostgres()
        query = f"SELECT * FROM public.\"Parameter\" WHERE name=\'Parametr y\'"
        y = database.getOne(cur, query).get('value')
        query = f"SELECT * FROM public.\"Parameter\" WHERE name=\'Parametr z\'"
        z = database.getOne(cur, query).get('value')
        if not y or not z:
            return func.HttpResponse(
                "Nie można odczytać parametrów",
                status_code=400
            )

        locale.setlocale(locale.LC_ALL, 'pl_PL')
        weekday_name_now = calendar.day_name[date.weekday()].upper()
        query = f"SELECT * FROM public.\"Lesson\" l JOIN public.\"Lesson_type\" lt ON lt.lesson_type_id = l.lesson_type_id  WHERE l.is_active AND lt.is_active AND l.weekday='{weekday_name_now}' AND (lt.name = 'WOLNE WEJŚCIE' OR ('{hour.strftime('%H:%M:%S %z')}' BETWEEN l.start_time - ({y} * interval '1 minute') AND l.start_time + ({z} * interval '1 minute')))"
        lessons = database.getMany(cur, query)
        
        lessons = json.dumps(lessons, default=str, ensure_ascii=False)
        return func.HttpResponse(
                lessons,
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