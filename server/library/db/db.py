import os
import psycopg2
import psycopg2.pool
from urllib.parse import urlparse

class ConnPoolInterface:
    def __init__(self, db):
        self.db = db
    def getconn(self):
        return self.db.get_connection()
    def putconn(self, conn):
        conn.close()


class Database:
    def __init__(self):
        db_conn_string = os.environ.get("DATABASE_URL", "")
        parsed_string = urlparse(db_conn_string)
        db_config = {
            "host": parsed_string.hostname,
            "user": parsed_string.username,
            "password": parsed_string.password,
            "database": parsed_string.path.split("/")[1],
            "port": os.environ.get("DB_PORT", 5432)
        }
        self.pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1, maxconn=10, **db_config
        )
    
    def exec_stmt(self, stmt, args: tuple, commit=False, fetch=True):
        con = self.pool.getconn()
        try:
            cur = con.cursor()
            if not type(stmt) == list:
                stmt = [stmt]
            for s in stmt:
                if len(s.strip()):
                    cur.execute(s, args)
            if commit:
                con.commit()
            if fetch:
                result = cur.fetchall()
                return result
        except:
            con.rollback()
            raise
        finally:
            cur.close()
            self.pool.putconn(con)

def db_init():
    global db
    db = Database()

def db_get():
    global db
    return db
