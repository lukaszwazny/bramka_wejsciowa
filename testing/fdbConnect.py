import fdb

con = fdb.connect(
        host='20.61.35.191', database='/firebird/data/Fitnes.fdb',
        user='sysdba', password='masterkey', charset='UTF8'
    )
print