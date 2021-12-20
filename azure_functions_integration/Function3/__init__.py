import logging
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info('Getting parameters')
    identificator_nr = req.params.get('identificator_nr')
    date = req.params.get('date')
    lesson = req.params.get('lesson')

    resp=json.dumps({'entrance_allowed': True}, ensure_ascii=False)
    return func.HttpResponse(
        resp,
        status_code=200,
        mimetype='application/json'
    )
