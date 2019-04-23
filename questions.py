import mysql.connector
import tkinter

print('Connecting...')

mydb = mysql.connector.connect(
  host="192.168.1.117",
  user="vejice",
  passwd="vejice",
  database="vejice"
)

mycursor = mydb.cursor()

sql = "SELECT * FROM vejica13 WHERE ID LIKE 'Lektor%' ORDER BY RAND() LIMIT 100" # select only grammatically correct sentences (from corpus Lektor)
mycursor.execute(sql)

result_set = mycursor.fetchall()

def star(i):
    c = mydb.cursor()
    sql = "UPDATE vejica13 SET starred = 1 WHERE ID = '%s'"
    c.execute(sql, i)
    mydb.commit()
    print('Starred')
    

for row in result_set:
    print(row[1].replace('÷', '').replace('¤', '').replace(',',''))
    input()
    print(row[1].replace('÷', '').replace('¤', ','))
    s = input()
    if s.strip() == 's': star(row[0])
    print('')

