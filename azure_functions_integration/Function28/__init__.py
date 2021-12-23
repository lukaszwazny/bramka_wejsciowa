import logging
import json

from shared_code import database
from shared_code.helpers import safe_list_get

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    lesson_type_id = req.params.get('lesson_type_id')

    try:

        if lesson_type_id:
            cur = database.connectPostgres()
            query = f'SELECT lesson_id, weekday, start_time, end_time FROM public."Lesson" WHERE is_active AND lesson_type_id={lesson_type_id};'
            lessons = json.dumps(database.getMany(cur, query), default=str, ensure_ascii=False)
            
            return func.HttpResponse(
                    lessons,
                    status_code=200,
                    mimetype='application/json'
                )
        else:
            return func.HttpResponse(
                "Nie podano wszystkich wymaganych danych",
                status_code=400
            )
    
    except Exception as ex:
        logging.info('Unknown error')
        logging.info(ex)
        return func.HttpResponse(
            "Unknown error",
            status_code=400
        )