import os
import mysql.connector
from urllib.parse import urlparse

error = False
try:
    db_conn_string = os.environ.get("CLEARDB_DATABASE_URL", "")
    parsed_string = urlparse(db_conn_string)
    mydb = mysql.connector.connect(
    host=parsed_string.hostname,
    user=parsed_string.username,
    passwd=parsed_string.password,
    database=parsed_string.path.split("/")[1]
        )
except mysql.connector.Error as err:
    print(err)
    error = True

def getUserStatistics(userID):
    if error: return 0, 0, True
    query = """SELECT total, correct 
    FROM userstatistics 
    WHERE userid = %s"""
    cur = mydb.cursor()
    cur.execute(query, (userID,))
    for (total, correct) in cur:
        cur.close()
        return total, correct, False
    cur.close()
    return 0, 0, False

def updateUserStatistics(userID, correct):
    if(correct != 0 and correct != 1): return True
    query = """ insert into userstatistics(userid,total,correct)
                                    values(%s, 1, %s)
                on duplicate key update 
                    total  = total+1,
                    correct=correct+%s;
            """

    cur = mydb.cursor()
    cur.execute(query, (userID, correct, correct,))
    mydb.commit()
    cur.close()
    return False