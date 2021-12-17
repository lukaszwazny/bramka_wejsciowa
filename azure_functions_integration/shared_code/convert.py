import re
from shared_code.helpers import safe_list_get

def convertClanoviToUser(clanovi):
    clanovi['name'] = clanovi.pop('IME')
    clanovi['surname'] = clanovi.pop('PREZIME')
    clanovi['identificator_nr'] = clanovi.pop('MEMBERID')
    clanovi['birthdate'] = clanovi.pop('DATUMRODJENJA')
    clanovi['sex'] = clanovi.pop('POL')
    clanovi['phone'] = clanovi.pop('TELEFON')
    street = clanovi.pop('ULICA')
    if street:
        street = re.split(r'(\d+.+)',street, 1)
    clanovi['street_name'] = safe_list_get(street, 0, None)
    clanovi['house_nr'] = safe_list_get(street, 1, None)
    clanovi['postal_code'] = clanovi.pop('ZIP')
    clanovi['city'] = clanovi.pop('NAZIV')
    clanovi['e_mail'] = clanovi.pop('EMAIL')
    clanovi['aditional_info'] = clanovi.pop('INFO')
    clanovi['PESEL'] = None
    clanovi['is_active'] = True
    clanovi.pop('JMBG')
    clanovi.pop('MESTOID')
    clanovi.pop('BROJ')
    clanovi.pop('GRUPAID')
    clanovi.pop('VARIJANTA')
    clanovi.pop('UPLATAID')
    clanovi.pop('ZELITRENERA')
    clanovi.pop('TRENERID')
    clanovi.pop('DEBT')
    clanovi.pop('PIN')
    clanovi.pop('COUNTRY')
    clanovi.pop('REWARDPOINTS')
    clanovi.pop('JOINDATE')
    clanovi.pop('MEDICALISSUES')
    clanovi.pop('RFID')
    clanovi.pop('DAC_STATUS')
    return clanovi