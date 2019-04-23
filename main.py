from CommaDatabase import *
from tkt import *

print('Connecting...')

mydb = CommaDatabase()



StartMainWindow(mydb)

if mydb.action == 1:
    # practice 100
    StartPracticeWindow(mydb)
elif mydb.action == 2:
    print("TODO")
