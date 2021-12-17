import json
import requests

test_data = json.load(open('testing\\CLANOVI_202112171859.json'))
resp = requests.get('https://azurefunctionsintegration.azurewebsites.net/api/Function1?code=tgrN1Qu1U1W5BbCeUT6K7HfKUuG1ZXCnoQUDoNPvad0oQzTXXlWPpg==&identificator_nr=0001614537')
print(resp.text)
for mem_id in test_data['select memberid from clanovi']:
    resp = requests.get('https://azurefunctionsintegration.azurewebsites.net/api/Function1?code=tgrN1Qu1U1W5BbCeUT6K7HfKUuG1ZXCnoQUDoNPvad0oQzTXXlWPpg==&identificator_nr='+mem_id['MEMBERID'])
    print(resp.text)
