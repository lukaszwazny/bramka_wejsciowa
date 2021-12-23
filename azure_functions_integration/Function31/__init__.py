import logging
import json

from shared_code import database

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    req_body = req.get_json()
    lesson_id = req_body.get('lesson_id')

    if lesson_id:
        try:
            cur = database.connectPostgres()
            query = f"""
                UPDATE public."Lesson"
                SET is_active={False}
                WHERE lesson_id={lesson_id};
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