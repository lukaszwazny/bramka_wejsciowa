import logging
import json
from re import split

from shared_code import database
from shared_code.helpers import safe_list_get

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    req_body = req.get_json()
    value = req_body.get('value')
    name = req_body.get('name')

    if name and value:
        try:
            cur = database.connectPostgres()
            query = f"SELECT name FROM public.\"Parameter\""
            exist_names = database.getMany(cur, query)
            if name in [d['name'] for d in exist_names]:
                query = f"""
                    UPDATE public."Parameter"
                    SET value={value}
                    WHERE name='{name}';
                """
            else:
                query= f"""
                    INSERT INTO public."Parameter"(
                    name, value, unit)
                    VALUES ('{name}', {value}, 'min');
                """
            cur.execute(query)
            cur.execute("COMMIT")

            return func.HttpResponse(
                    "OK",
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
            "Nie podano wszystkich wymaganych danych",
            status_code=400
        )