import mysql.connector

print('Connecting...')

mydb = mysql.connector.connect(
  host="192.168.1.117",
  user="vejice",
  passwd="vejice",
  database="vejice"
)

mycursor = mydb.cursor()

sql = "SELECT * FROM vejica13 WHERE ID LIKE 'Lektor%' ORDER BY RAND() LIMIT 100"
mycursor.execute(sql)

result_set = mycursor.fetchall()

def star(i):
    c = mydb.cursor()
    sql = "UPDATE vejica13 SET starred = 1 WHERE ID = '"+i+"'"
    print(sql)
    c.execute(sql)
    mydb.commit()
    print('Starred')
    

for row in result_set:
    print(row[1].replace('÷', '').replace('¤', '').replace(',',''))
    input(end='\r')
    print(row[1].replace('÷', '').replace('¤', ','))
    s = input()
    if s.strip() == 's': star(row[0])
    print('')

