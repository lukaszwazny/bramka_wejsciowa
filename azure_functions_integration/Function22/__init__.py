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
    justification_id = req_body.get('justification_id')

    if justification_id:
        try:
            cur = database.connectPostgres()
            query = f"""
                UPDATE public."Justification"
                SET is_active={False}
                WHERE justification_id=\'{justification_id}\'; 
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