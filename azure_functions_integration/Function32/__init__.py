import logging
import json

from shared_code import database

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    req_body = req.get_json()
    weekday = req_body.get('weekday')
    start_time = req_body.get('start_time')
    end_time = req_body.get('end_time')
    lesson_type_id = req_body.get('lesson_type_id')

    if weekday and start_time and end_time and lesson_type_id:
        try:
            cur = database.connectPostgres()
            query = f"""
                INSERT INTO public."Lesson"(
                weekday, start_time, end_time, is_active, lesson_type_id)
                VALUES ('{weekday}', '{start_time}', '{end_time}', {True}, {lesson_type_id});
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