import datetime
import sqlite3

global verbose, _sql_conn, _sql_cur
verbose = True
_sql_conn=sqlite3.connect("../data/inv_data.db")
_sql_cur = _sql_conn.cursor()

# Tables is a dict{table name : list["fieldname dtype primary key etc"]}
tables:dict = {
    "items": [
        "part_number TEXT PRIMARY KEY",
        "part_name TEXT NOT NULL",
        "qty INT DEFAULT 0",
        "threshold_qty INT DEFAULT NULL",
        "dependencies TEXT DEFAULT NULL",
        "verified_date TEXT DEFAULT NULL",
        "alt_part_nums TEXT DEFAULT NULL"
        ],
    "transactions": [
        "part_number TEXT NULL",
        "type TEXT NULL",
        "qty REAL NULL",
        "datetime TEXT NULL"
        ],
    "catalog": [
        "part_number TEXT",
        "part_name TEXT",
        "source_name TEXT",
        "source_link TEXT",
        "price REAL",
        "unit TEXT",
        "unit_qty INT"
        ]
}

columns = dict()
for table in tables:
    columns[table] = [x.split(" ")[0] for x in tables[table]]

def now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def sql_setup():
    """Runs functions to check current status of the SQL db.
    Ensures all things are setup and with correct schema.
    """
    table_check()
    fields_check()
    return 0

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
    tables_sql = [x[0] for x in _sql_cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()]
    if verbose: print(now() + ": Table Check: found", len(tables_sql), "tables.")
    if verbose: print(now() + ": Table Check: tables present:", tables_sql)
    ran = False
    for table in tables.keys():
        if table not in tables_sql:
            if verbose: print(now() + ": Table Check: '" + table + "' table not found...")
            if verbose: print(now() + ": Table Check: building '" + table + "' table...")
            _sql_cur.execute("CREATE TABLE " + table + " (" + "".join([x + "," for x in tables[table]]).rstrip(",") + ");")
            _sql_conn.commit()
            if verbose: print(now() + ": Table Check: succesfully built '" + table + "' table.")
            ran = True
    if ran:
        tables_sql = [x[0] for x in _sql_cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()]
        if verbose: print(now() + ": Table Check: found", len(tables_sql), "tables.")
        if verbose: print(now() + ": Table Check: tables present:", tables_sql)
    if verbose: print(now() + ": Table Check: All Tables found. Ready.")
    return 0

def fields_check():
    if verbose: print(now() + ": Fields Check: Beginng...")
    for table in tables.keys():
        if verbose: print(now() + ": Fields Check: Checking table:", table)
        fields:str = [x[0] for x in _sql_cur.execute("SELECT sql FROM sqlite_schema WHERE name = '"+table+"';")]
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
                _sql_cur.execute("ALTER TABLE " + table + "ADD COLUMN " + field)
                _sql_conn.commit()
                if verbose: print(now() + ": Fields Check: Sucessfully altered table.")
        if verbose: print(now() + ": Fields Check: Completed checking table '" + table + "'.")
        if verbose and good: print(now() + ": Fields Check: Succesful validation for the above table.")
        if verbose and not good: print(now() + ": Fields Check: Found atleast one missing field.")
