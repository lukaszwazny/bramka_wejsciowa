import azure.functions as func
import json
from shared_code import database
from shared_code.helpers import get_key, safe_list_get
import Function1
import Function6
from itertools import zip_longest
from collections import defaultdict

def get_user(identificator_nr):
    try:
        params = dict(
            code=get_key(),
            identificator_nr=identificator_nr
        )
        fun1_req = func.HttpRequest('get', '', params=params, body='')
        resp = json.loads(Function1.main(fun1_req).get_body())

        cur = database.connectPostgres()
        cur.execute(f'SELECT * FROM public."User" WHERE identificator_nr = \'{identificator_nr}\'')
        names = [item[0] for item in cur.description]
        resp_new = cur.fetchone()
        for i in range(len(names)):
            if safe_list_get(resp_new, i, None):
                resp[names[i]] = safe_list_get(resp_new, i, None)

        if resp.get('user_id'):
            query = f"SELECT * FROM public.\"Role_User\" RIGHT OUTER JOIN public.\"Role\" ON role_id = \"Role_role_id\"  WHERE \"User_user_id\" = {resp['user_id']} AND is_active"
            resp_new = database.getMany(cur, query)
            resp_new = [item['role_name'] for item in resp_new]
            resp['roles'] = resp['roles'] + list(set(resp_new))

        return resp
    
    except Exception as ex:
        return ex

def get_active_user(identificator_nr):
    try:
        params = dict(
            code=get_key(),
            identificator_nr=identificator_nr
        )
        fun1_req = func.HttpRequest('get', '', params=params, body='')
        resp = json.loads(Function1.main(fun1_req).get_body())

        cur = database.connectPostgres()
        cur.execute(f'SELECT * FROM public."User" WHERE identificator_nr = \'{identificator_nr}\' AND is_active')
        names = [item[0] for item in cur.description]
        resp_new = cur.fetchone()
        for i in range(len(names)):
            if safe_list_get(resp_new, i, None):
                resp[names[i]] = safe_list_get(resp_new, i, None)

        if resp.get('user_id'):
            query = f"SELECT * FROM public.\"Role_User\" RIGHT OUTER JOIN public.\"Role\" ON role_id = \"Role_role_id\"  WHERE \"User_user_id\" = {resp['user_id']} AND is_active"
            resp_new = database.getMany(cur, query)
            resp_new = [item['role_name'] for item in resp_new]
            resp['roles'] = resp['roles'] + list(set(resp_new))

        return resp
    
    except Exception as ex:
        return ex

def get_users(identificator_nrs):
    try:
        if identificator_nrs:
            identificator_nrs = ', '.join(["\'" + str(id_nr) + "\'" for id_nr in identificator_nrs])
            params = dict(
                identificator_nrs=identificator_nrs
            )
        else:
            params = {}
        fun6_req = func.HttpRequest('get', '', params=params, body='')
        resp = json.loads(Function6.main(fun6_req).get_body())

        cur = database.connectPostgres()
        if identificator_nrs:
            query = f'SELECT * FROM public."User" WHERE identificator_nr IN ({identificator_nrs})'
        else:
            query = f'SELECT * FROM public."User"'
        resp_new = list(map(lambda r: dict(identificator_nr=r.get('identificator_nr'), name=r.get('name'), surname=r.get('surname')), database.getMany(cur, query)))

        for idx, r in enumerate(resp):
            for d in resp_new: 
                if d['identificator_nr']==r['identificator_nr']:
                    resp.pop(idx)
        
        resp = resp + resp_new

        return resp
    
    except Exception as ex:
        return ex


def get_active_users():
    try:
        fun6_req = func.HttpRequest('get', '', params={}, body='')
        resp = json.loads(Function6.main(fun6_req).get_body())

        cur = database.connectPostgres()
        query = f'SELECT * FROM public."User" WHERE is_active'
        resp_new = list(map(lambda r: dict(user_id=r.get('user_id'), identificator_nr=r.get('identificator_nr'), name=r.get('name'), surname=r.get('surname')), database.getMany(cur, query)))

        for r in resp_new:
            query = f"SELECT * FROM public.\"Role_User\" RIGHT OUTER JOIN public.\"Role\" ON role_id = \"Role_role_id\"  WHERE \"User_user_id\" = {r['user_id']} AND is_active"
            roles = database.getMany(cur, query)
            roles = [item['role_name'] for item in roles]
            r['roles'] = list(set(roles))

        for idx, r in enumerate(resp):
            for d in resp_new:
                if d['identificator_nr']==r['identificator_nr']:
                    d['roles'] = d['roles'] + r['roles']
                    resp.pop(idx)
        
        resp = resp + resp_new

        return resp
    
    except Exception as ex:
        return ex