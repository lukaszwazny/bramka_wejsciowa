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
    name_surname = req_body.get('name')
    if name_surname:
        name_surname = split(' ',name_surname, 1)
    name = safe_list_get(name_surname, 0, None)
    surname = safe_list_get(name_surname, 1, None)
    identificator_nr = req_body.get('identificator_nr')
    birthdate = req_body.get('birthdate')
    sex = req_body.get('sex')
    phone = req_body.get('phone')
    PESEL = req_body.get('PESEL')
    street_name = req_body.get('street_name')
    house_nr = req_body.get('house_nr')
    postal_code = req_body.get('postal_code')
    city = req_body.get('city')
    e_mail = req_body.get('e_mail')
    additional_info = req_body.get('additional_info')

    if user_id:
        try:
            if name or surname or identificator_nr or birthdate or sex or phone or PESEL or street_name or house_nr or postal_code or city or e_mail:
                cur = database.connectPostgres()
                query = f"UPDATE public.\"User\" SET"
                if name:
                    query += f" name=\'{name}\',"
                if surname:
                    query += f" surname=\'{surname}\',"
                if identificator_nr:
                    query += f" identificator_nr=\'{identificator_nr}\',"
                if birthdate:
                    query += f" birthdate=\'{birthdate}\',"
                if sex:
                    query += f" sex=\'{sex}\',"
                if phone:
                    query += f" phone=\'{phone}\',"
                if PESEL:
                    query += f" \"PESEL\"=\'{PESEL}\',"
                if street_name:
                    query += f" street_name=\'{street_name}\',"
                if house_nr:
                    query += f" house_nr=\'{house_nr}\',"
                if postal_code:
                    query += f" postal_code=\'{postal_code}\',"
                if city:
                    query += f" city=\'{city}\',"
                if e_mail:
                    query += f" e_mail=\'{e_mail}\',"
                if additional_info:
                    query += f" additional_info=\'{additional_info}\',"

                if query[-1] == ',':
                    query = query[:-1]

                query += f" WHERE user_id={user_id}"
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