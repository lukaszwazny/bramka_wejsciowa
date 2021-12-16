import rdm6300

reader = rdm6300.Reader('/dev/ttyTHS1')
while True:
    card = reader.read()
    print(card)
    if card:
        print(f"[{card.value}] read card {card}")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# """
# PyRfid
# Copyright (C) 2015 Philipp Meisberger <team@pm-codeworks.de>
# All rights reserved.
# """

# from pyrfid.pyrfid import PyRfid

# rfid = PyRfid('/dev/ttyTHS1', 9600)

# try:
#     print('Waiting for tag...\n')

#     if ( rfid.readTag() != True ):
#         raise Exception('User aborted!')

#     print('RAW:      '+ rfid.rawTag)
#     print('Checksum: '+ rfid.tagChecksum +'\n')

#     print('Decimal-format:')
#     print('ID:       '+ rfid.tagId)
#     print('Type:     '+ rfid.tagType +'\n')

#     print('Float-format:')
#     print('ID:       '+ rfid.tagIdFloat)
#     print('Type:     '+ rfid.tagTypeFloat)

# except Exception as e:
#     print('[Exception] '+ str(e))
#     exit(1)