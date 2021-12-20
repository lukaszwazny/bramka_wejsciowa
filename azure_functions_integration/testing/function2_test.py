import json
import requests

test_data = json.load(open('testing\\CLANOVI_202112171859.json'))
for mem_id in test_data['select memberid from clanovi']:
    resp = requests.get('https://azurefunctionsintegration.azurewebsites.net/api/Function2?code=UiF8iy6Kc9n6rocbthkvgjxfEedtSvv4u6iQaiIPlgmQlWiKJfsCtQ==&identificator_nr='+mem_id['MEMBERID']+'&date=2021-10-15')
    print(mem_id, resp.text)