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
    user_id = req_body.get('user_id')
    name = req_body.get('name')
    from_ = req_body.get('from')
    to_ = req_body.get('to')
    description = req_body.get('description')

    if user_id and name and from_ and to_ and description:
        try:
            cur = database.connectPostgres()
            query = f"""
                INSERT INTO public."Justification"(
                name, "from", "to", description, is_active, user_id)
                VALUES ('{name}', '{from_}', '{to_}', '{description}', {True}, {user_id});
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