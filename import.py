# import repository of examples into mysql database with this script (repository: https://www.clarin.si/repository/xmlui/handle/11356/1185)

from db-funcs import *

mydb = CommaDatabase()

with open('vejica13.txt', encoding='utf-8-sig') as fp:  
    line = fp.readline()
    while line:
        x = line.strip().split('\t')
        mydb.insert(mydb, x[0], x[1])
        line = fp.readline()

print('Committing changes')

mydb.commit()

print('Import done')