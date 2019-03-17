import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.1.117",
  user="vejice",
  passwd="vejice",
  database="vejice"
)


def insert(id, original):
    mycursor = mydb.cursor()
    sql = "INSERT INTO vejica13 (id, original) VALUES (%s, %s)"
    mycursor.execute(sql, (id, original))


with open('vejica13.txt',encoding='utf-8-sig') as fp:  
    line = fp.readline()
    while line:
        x = line.strip().split('\t')
        insert(x[0], x[1])
        line = fp.readline()

print('Committing changes')

mydb.commit()

print('Import done')