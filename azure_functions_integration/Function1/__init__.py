from logging import info
from fdb import DatabaseError
from json import dumps

from shared_code import database, convert
from shared_code.helpers import safe_list_get

from azure.functions import HttpRequest, HttpResponse


def main(req: HttpRequest) -> HttpResponse:
    info('Python HTTP trigger function processed a request.')

    info('Getting parameters')
    identificator_nr = req.params.get('identificator_nr')

    if identificator_nr:
        try:

            cur = database.connect()
            query = f"select * from clanovi right outer join mesta on clanovi.mestoid = mesta.id where memberid='{identificator_nr}'"

            resp = database.getOne(cur, query)
            resp = convert.convertClanoviToUser(resp)
            resp['roles'] = []
            if resp['ID']:
                resp['roles'].append('KLIENT')     
            resp = dumps(resp, default=str, ensure_ascii=False)
            info('Converted data succesfully')
            info('Responded with' + resp)
            return HttpResponse(
                resp,
                status_code=200,
                mimetype='application/json'
            )

        except DatabaseError as err:
            info('Database error :(')
            return HttpResponse(
                err.args[0],
                status_code=500
            )
        
        except Exception as ex:
            info('Unknown error')
            info(ex)
            return HttpResponse(
                "Unknown error",
                status_code=400
            )
    else:
        return HttpResponse(
             "Nie podano nr identyfikatora!",
             status_code=400
        )