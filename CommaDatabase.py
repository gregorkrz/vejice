import mysql.connector

class CommaDatabase:
    def __init__(self):
        self.db = mysql.connector.connect(
        host="192.168.1.117",
        user="vejice",
        passwd="vejice",
        database="vejice"
        )
        self.result_set = None
        self.action = 0
    
    def fetch100(self):
        mycursor = self.db.cursor()
        sql = "SELECT * FROM vejica13 WHERE ID LIKE 'Lektor%' ORDER BY RAND() LIMIT 100" # select sentences from corpuses that seem to contain gramatically correct sentences
        mycursor.execute(sql)
        self.result_set = mycursor.fetchall()

    def insert(self, id, original):
        mycursor = self.db.cursor()
        sql = "INSERT INTO vejica13 (id, original) VALUES (%s, %s)"
        mycursor.execute(sql, (id, original))

    def star(self, id):
        c = self.db.cursor()
        sql = "UPDATE vejica13 SET starred = 1 WHERE ID = '"+id+"'"
        c.execute(sql)
        self.commit()

    def commit(self):
        self.db.commit()
