import logging

import azure.functions as func

from helpers import send_entrance_to_app


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    send_entrance_to_app(dict(role_name= "MaRiAn"))

    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )
