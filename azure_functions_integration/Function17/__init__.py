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
    name_surname = req_body.get('name')
    if name_surname:
        name_surname = split(' ',name_surname, 1)
    name = safe_list_get(name_surname, 0, None)
    surname = safe_list_get(name_surname, 1, None)
    role = req_body.get('role')
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

    if name and surname and identificator_nr and birthdate and sex and phone and PESEL and street_name and house_nr and postal_code and city and e_mail:
        try:

            cur = database.connectPostgres()
            query = f"""
            INSERT INTO public.\"User\"
            (name, surname, identificator_nr, birthdate, sex, phone, "PESEL", street_name, house_nr, postal_code, city, e_mail, additional_info, is_active)
	        VALUES ('{name}', '{surname}', '{identificator_nr}', '{birthdate}', '{sex}', '{phone}', '{PESEL}', '{street_name}', '{house_nr}', '{postal_code}', '{city}', '{e_mail}', '{additional_info if additional_info else ''}', {True});
            """
            cur.execute(query)
            if role:
                query = f"SELECT role_id FROM public.\"Role\" WHERE role_name=\'{role}\' and is_active"
                role = database.getOne(cur, query).get("role_id")
            if role:
                query = f"""
                    INSERT INTO public.\"Role_User\"
                    (\"Role_role_id\", "User_user_id\")
                    VALUES ({role}, (SELECT user_id FROM public.\"User\" WHERE identificator_nr=\'{identificator_nr}\'));
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