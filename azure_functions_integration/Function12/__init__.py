import logging
import json
from datetime import datetime
import requests

from shared_code import database
from shared_code.helpers import safe_list_get, get_url, get_key

import azure.functions as func
import Function4


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        identificator_nr = req_body.get('identificator_nr')
        role = req_body.get('role')
        package = req_body.get('package')
        lesson_type_id = req_body.get('lesson_type_id')
        justification = req_body.get('justification')

        if not (199 < send_opening_command().status_code < 300):
            raise Exception()

        date = datetime.now().astimezone().date()
        hour = datetime.now().astimezone().timetz()

        data = dict(
            identificator_nr=identificator_nr,
            date=date.strftime('%Y-%m-%d'),
            hour=hour.strftime('%H:%M:%S'),
            package_id=package.get('package_id') if package else None,
            lesson=lesson_type_id
        )
        fun4_req = func.HttpRequest('post', '', params={}, body=json.dumps(data, ensure_ascii=False))
        resp = Function4.main(fun4_req)

        cur = database.connectPostgres()
        query = f"INSERT INTO public.\"Entrance\"(datetime, mode, justification, \"package\", identificator_nr, role_name, lesson_type_id) VALUES ('{datetime.combine(date, hour).strftime('%Y-%m-%d %H:%M:%S %z')}', 'WEJŚCIE',  "
        query += f"'{justification}', " if justification else "null, "
        query += f"'{package.get('package_name')}', " if package and package.get('package_name') else "null, "
        query += f"'{identificator_nr}', " if identificator_nr else "null, "
        query += f"'{role}', " if role else "null, "
        query += f"{lesson_type_id})" if lesson_type_id else "null)"
        cur.execute(query)
        cur.execute("COMMIT")

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