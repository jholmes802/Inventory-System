#!/usr/bin/python3
from logger import logger
import datetime
import os
import pathlib
import sqlalchemy

if sqlalchemy.__version__ != "1.4.29":
    print(sqlalchemy.__version__, "not correct version. Please use 1.4.29")

global verbose, _sql_conn, _sql_cur
verbose = False
if "verbose.dat" in os.listdir(os.getcwd()):
    verbose = True

def _now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Tables is a dict{table name : list["fieldname dtype primary key etc"]}
tables:dict = {
    "items": [
        "part_number TEXT PRIMARY KEY",
        "part_name TEXT NOT NULL",
        "qty INT DEFAULT 0",
        "threshold_qty INT DEFAULT NULL",
        "dependencies TEXT DEFAULT NULL",
        "verified_date TEXT DEFAULT NULL",
        "alt_part_nums TEXT DEFAULT NULL",
        "search_parms TEXT DEFUALT NULL",
        "notes TEXT"
        ],
    "transactions": [
        "part_number TEXT NULL",
        "type TEXT NULL",
        "qty REAL NULL",
        "datetime TEXT NULL",
        "destination TEXT",
        "source TEXT",
        "notes TEXT"
        ],
    "catalog": [
        "part_number TEXT",
        "part_name TEXT",
        "source_name TEXT",
        "source_link TEXT",
        "manufacturer TEXT",
        "manufacturer_link TEXT",
        "price REAL",
        "unit TEXT",
        "unit_qty INT",
        "notes TEXT"
        ],
    "locations":[
        "name TEXT NOT NULL",
        "type TEXT NOT NULL",
        "desc TEXT NOT NULL"
    ],
    "cabinetLoc":[
        "location TEXT",
        "part_number TEXT NOT NULL",
        "qty REAL",
        "notes TEXT"
    ]
}
dbpath = pathlib.Path("../data/inv_data.db")
columns = dict()
for table in tables:
    columns[table] = [x.split(" ")[0] for x in tables[table]]

engine = sqlalchemy.create_engine("sqlite+pysqlite:///../data/inv_data.db", )

def now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def sql_setup():
    """Runs functions to check current status of the SQL db.
    Ensures all things are setup and with correct schema.
    """
    table_check()
    fields_check()
    return 0

def run_retrieve(sql, num=-1):
    _sql_conn=engine.connect()
    result = _sql_conn.execute(sql).all()
    _sql_conn.close()
    return result

def run(sql):
    _sql_conn=engine.connect()
    result = _sql_conn.execute(sql)
    _sql_conn.close()
    return True

def table_check():
    """Checks sqlite db file to ensure it has the appropriate tables and structure.
    Supports verbose.
    
    ---CHANGE LOG---
    - 12/23/2021 - Added checks if tables exists for [items, transactions, catalog].
        - Needs field checking for all tables.
        - May need additional Table for kits out, something to look at where stuff is?
    -12/23/2021 - Modified to utilize the tables dictionary so adding tables is easier and makes constant variable across the whole file.
        -Moving field checking to field_checks(). May remerge later.
        -Should add error checking...?
    """
    if verbose: print(now() + ": Table Check: Beginning Check for tables.")
    tables_sql = [x[0] for x in run_retrieve("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';")]
    if verbose: print(now() + ": Table Check: found", len(tables_sql), "tables.")
    if verbose: print(now() + ": Table Check: tables present:", tables_sql)
    ran = False
    for table in tables.keys():
        if table not in tables_sql:
            if verbose: print(now() + ": Table Check: '" + table + "' table not found...")
            if verbose: print(now() + ": Table Check: building '" + table + "' table...")
            run("CREATE TABLE " + table + " (" + "".join([x + "," for x in tables[table]]).rstrip(",") + ");")
            if verbose: print(now() + ": Table Check: succesfully built '" + table + "' table.")
            ran = True
    if ran:
        tables_sql = [x[0] for x in run_retrieve("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';")]
        if verbose: print(now() + ": Table Check: found", len(tables_sql), "tables.")
        if verbose: print(now() + ": Table Check: tables present:", tables_sql)
    if verbose: print(now() + ": Table Check: All Tables found. Ready.")
    return 0

def fields_check():
    """Checks fields for the tables in the tables dictionary. 
    Returns nothing, and support verbose logging. 
    """
    if verbose: print(now() + ": Fields Check: Beginng...")
    for table in tables.keys():
        if verbose: print(now() + ": Fields Check: Checking table:", table)
        fields:str = [x[0] for x in run_retrieve("SELECT sql FROM sqlite_schema WHERE name = '"+table+"';")]
        if verbose: print(now() + ": Fields Check: Found", len(fields), "results from sqlite_shcema.")
        fields = fields[0]
        fields_start = fields.find("(")
        fields_end = fields.find(")")
        extracted = fields[fields_start + 1:fields_end].split(',')
        if verbose: print(now() + ": Fields Check: Found", len(extracted),"fields.")
        if verbose: print(now() + ": Fields Check: Found", len(tables[table]), "expected fields.")
        good = True
        for field in tables[table]:
            if field not in extracted:
                good = False
                if verbose: print(now() + ": Fields Check: Could not find '" + field + "' in sqlite_schema. Altering table...")
                run("ALTER TABLE " + table + "ADD COLUMN " + field)
                if verbose: print(now() + ": Fields Check: Sucessfully altered table.")
        if verbose: print(now() + ": Fields Check: Completed checking table '" + table + "'.")
        if verbose and good: print(now() + ": Fields Check: Succesful validation for the above table.")
        if verbose and not good: print(now() + ": Fields Check: Found atleast one missing field.")

def backup():
    """Creates a new backup folder in "../backup/" for the current date and time.
    Creates a csv file from each db table into there.

    """
    stamp = _now().replace(" ","_").replace(":","_")
    backup_path = '../backup/'+ stamp + "/"
    if stamp not in os.listdir('../backup/'):
        os.mkdir(backup_path)
    for t in tables.keys():
        file_path = pathlib.Path(backup_path + t + ".csv")
        fhand = open(file_path, "w")
        fhand.write(", ".join([x.split()[0] for x in tables[t]]).lstrip(',').rstrip(",")+"\n")
        sql = run_retrieve("SELECT * FROM " + t + ";")
        for r in sql:
            fhand.write(", ".join([str(x) for x in r]).rstrip(",").lstrip(",") + "\n")
        fhand.close()
    return True

def clean_backups():
    """Cleans up the backups to be the latest 30 backups made.
    """
    dirlist = os.listdir("../backup/")
    if len(dirlist) < 30:
        pass
    else:
        _kill_list = dirlist[:-30]
        i = 0
        for k in _kill_list:
            for item in os.listdir("../backup/" + k):
                os.remove("../backup/" + k + "/" + item)
            os.removedirs("../backup/" + k)
            logger(2, "db_manger.clean_backups: Removed backup for " + k)
            i += 1
        logger(2, "db_manager.clean_backups: Removed " + str(i) + " old backups.")

if __name__ == "__main__":
    sql_setup()
