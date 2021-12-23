import logging
import json

from shared_code import database
from shared_code.helpers import safe_list_get

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')

    try:

        cur = database.connectPostgres()
        query = f'SELECT lesson_type_id, name FROM public."Lesson_type" WHERE is_active;'
        lesson_types = json.dumps(database.getMany(cur, query), default=str, ensure_ascii=False)
        
        return func.HttpResponse(
                lesson_types,
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