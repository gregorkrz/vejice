import os
import mysql.connector
from urllib.parse import urlparse

def connect():
    try:
        db_conn_string = os.environ.get("CLEARDB_DATABASE_URL", "")
        parsed_string = urlparse(db_conn_string)
        mydb = mysql.connector.connect(
        host=parsed_string.hostname,
        user=parsed_string.username,
        passwd=parsed_string.password,
        database=parsed_string.path.split("/")[1]
            )
        return mydb, False
    except mysql.connector.Error as err:
        print(err)
        return mydb, True

def getUserStatistics(userID):
    mydb, error = connect()
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
    mydb.disconnect()
    return 0, 0, False

def updateUserStatistics(userID, correct):
    mydb, error = connect()
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
    mydb.disconnect()
    return False