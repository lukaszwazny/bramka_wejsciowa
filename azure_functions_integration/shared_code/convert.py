import re
from shared_code.helpers import safe_list_get

def convertClanoviToUser(clanovi):
    clanovi['name'] = clanovi.pop('IME', None)
    clanovi['surname'] = clanovi.pop('PREZIME', None)
    clanovi['identificator_nr'] = clanovi.pop('MEMBERID', None)
    clanovi['birthdate'] = clanovi.pop('DATUMRODJENJA', None)
    clanovi['sex'] = clanovi.pop('POL', None)
    clanovi['phone'] = clanovi.pop('TELEFON', None)
    street = clanovi.pop('ULICA', None)
    if street:
        street = re.split(r'(\d+.+)',street, 1)
    clanovi['street_name'] = safe_list_get(street, 0, None)
    clanovi['house_nr'] = safe_list_get(street, 1, None)
    clanovi['postal_code'] = clanovi.pop('ZIP', None)
    clanovi['city'] = clanovi.pop('NAZIV', None)
    clanovi['e_mail'] = clanovi.pop('EMAIL', None)
    clanovi['aditional_info'] = clanovi.pop('INFO', None)
    clanovi['PESEL'] = None
    clanovi['is_active'] = True
    clanovi.pop('JMBG', None)
    clanovi.pop('MESTOID', None)
    clanovi.pop('BROJ', None)
    clanovi.pop('GRUPAID', None)
    clanovi.pop('VARIJANTA', None)
    clanovi.pop('UPLATAID', None)
    clanovi.pop('ZELITRENERA', None)
    clanovi.pop('TRENERID', None)
    clanovi.pop('DEBT', None)
    clanovi.pop('PIN', None)
    clanovi.pop('COUNTRY', None)
    clanovi.pop('REWARDPOINTS', None)
    clanovi.pop('JOINDATE', None)
    clanovi.pop('MEDICALISSUES', None)
    clanovi.pop('RFID', None)
    clanovi.pop('DAC_STATUS', None)
    return clanovi