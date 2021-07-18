# Schema generation utility

SCHEMA_NAME = "vejice"


def schema_exists(db):
    exists_stmt = """SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s"""
    if len(db.exec_stmt(exists_stmt, (SCHEMA_NAME,))) != 0:
        print("Schema already exists")
        return True
    else:
        return False

def create_schema(db):
    if schema_exists(db):
        return
    script = open("scripts/storage/schema_create.sql").read().split(";")
    db.exec_stmt(script, tuple(), commit=True, fetch=False)
