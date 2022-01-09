import os
import datetime
import sqlite3

global config_file, items_file, fields, sql_conn, sql_cur, verbose
verbose = True
sql_conn=sqlite3.connect("../data/inv_data.db")
sql_cur = sql_conn.cursor()
config_file = "../data/config.csv"
items_file = '../data/items.csv'

def now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class FileError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
class ItemError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ConfigError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class configOpts():
    def __init__(self,fieldname:str, required:str, unique:str, default:str):
        self.fieldname = fieldname
        self.name = fieldname.lower().replace(" ", '_')
        self.required = required
        self.unique = unique
        self.default = default
        if "#" in self.default:
            self.default_inc = True
        else:
            self.default_inc = False

items = list[dict]

def getFields()-> list[configOpts]:
    fhand = open(config_file, "r")
    configDat = list()
    fieldnames = []
    for i,line in enumerate(fhand.readlines()[1:]):
        line = line.rstrip().split(",")
        #if len(line) != 4:
            #raise ConfigError("Incorrect number of entries on line " + str(i))
        if line[0] == "":
            raise ConfigError("Cannot have blank FIELDNAME on line", i)
        newCFig = configOpts(line[0], line[1], line[2], line[3])
        if line[1] == 'n':
            newCFig.required = False
        elif line[1] == 'y':
            newCFig.required = True
        if line[2] == 'n':
            newCFig.unique = False
        elif line[2] == 'y':
            newCFig.unique = True
        if newCFig.fieldname in fieldnames:
            raise ConfigError("Setup Console: '" + newCFig.fieldname + "' already in csv config file. Please rename or remove.")
        else:
            fieldnames.append(line[0])
            configDat.append(newCFig)
    fhand.close()
    return configDat


fields = getFields()

fields_names = [x.name for x in fields]

def sql_setup():
    """Checks sqlite db file to ensure it has the appropriate tables and structure.
    Supports verbose.
    
    ---CHANGE LOG---
    - 12/23/2021 - Added checks if tables exists for [items, transactions, catalog].
        - Needs field checking for all tables.
        - May need additional Table for kits out, something to look at where stuff is?
    """
    tables_sql = [x[0] for x in sql_cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()]
    if verbose: print(now() + ": SQL Setup: found", len(tables_sql), "tables.")
    if verbose: print(now() + ": SQL Setup: tables present:", tables_sql)
    ran = False
    if "items" not in tables_sql:
        if verbose: print(now() + ": SQL Setup: items table not found...")
        if verbose: print(now() + ": SQL Setup: building items table...")
        sql_cur.execute("CREATE TABLE items (part_number TEXT PRIMARY KEY, part_name TEXT, qty INT, unit TEXT, unit_qty TEXT, price REAL, pri_source TEXT, pri_link TEXT, second_source TEXT, second_link TEXT, second_price REAL, threshold_qty INT, dependencies TEXT, verified_date TEXT, alt_part_nums TEXT);")
        sql_conn.commit()
        if verbose: print(now() + ": SQL Setup: succesfully built items table.")
        ran = True
    if "transactions" not in tables_sql:
        if verbose: print(now() + ": SQL Setup: transactions table not found...")
        if verbose: print(now() + ": SQL Setup: building transactions table...")
        sql_cur.execute("CREATE TABLE transactions (part_number TEXT, type TEXT, qty REAL, datetime TEXT);")
        sql_conn.commit()
        if verbose: print(now() + ": SQL Setup: succesfully built transaction table.")
        ran = True
    if "catalog" not in tables_sql:
        if verbose: print(now() + ": SQL Setup: catalog table not found...")
        if verbose: print(now() + ": SQL Setup: building catalog table...")
        sql_cur.execute("CREATE TABLE catalog (part_number TEXT, part_name TEXT, source_name TEXT, source_link TEXT, price REAL, unit TEXT, unit_qty INT);")
        if verbose: print(now() + ": SQL Setup: succesfully built catalog table.")
        ran=True
    else:
        if ran:
            tables_sql = [x[0] for x in sql_cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()]
            if verbose: print(now() + ": SQL Setup: found", len(tables_sql), "tables.")
            if verbose: print(now() + ": SQL Setup: tables present:", tables_sql)
        if verbose: print(now() + ": SQL Setup: All Tables found. Ready.")
        return 0

def extractall()-> items:
    """DEPRICATED

    Raises:
        FileError: [description]
        FileError: [description]

    Returns:
        items: [description]
    """
    items_file = '../data/items.csv'
    if not items_file.endswith('.csv'):
        print("Invalid File Path")
        raise FileError("Provided file: '"+items_file+"' is not a '.csv' file type")
    if not os.path.exists(items_file):
        print("File not found")
        raise FileError("Listed file could not be found at:", items_file)
    fhand = open(items_file, 'r')
    fread = fhand.readlines()
    results = []
    for line in fread:
        line = line.rstrip("\n").split(',')
        print(line)
        if len(line) != len(fields):
            print(len(line))
            print(len(fields))
        new_item = dict()
        for i,field in enumerate(fields):
            if line[i] == "NA":
                line[i] = " "
            if line[i] == '':
                continue
            new_item[field.fieldname] =line[i]
        results.append(new_item)
    fhand.close()
    return results

def part_num_check(its:items)->bool:
    if len(its) <= 1:
        print("Passes rule 1")
        return True
    keys:list[str] = []
    for i in its:
        print(i)
        part_num = i["Part Number"]
        if part_num in keys:
            print("failed rule 2")
            return False
        else:
            keys.append(part_num)
    print("Passes rule 3")
    return True
        
def new_item(new_item:list[dict], check:bool = True)-> None:
    if check:
        its:items = extractall()
        its.append(new_item)
        if not part_num_check(its):
            raise ItemError("Item Already Exsits")
        else:
            nline = str()
            for field in fields:
                nline += new_item[field.fieldname]+ ","
            nline += ("\n")
            fhand = open(items_file,'a')
            fhand.write(nline)
            fhand.close()
    else:
        nline = str()
        for field in fields:
            nline += new_item[field]+ ","
        nline = nline.rstrip(",")
        nline += ("\n")
        fhand = open(items_file,'a')
        fhand.write(nline)
        fhand.close()

def filter(part_nums:list[str])->items:
    its = extractall()
    results = []
    for i in its:
        if i["Part Number"] in part_nums:
            results.append(i)
    return results

def find(part_nums:str)->items:
    its = extractall()
    for i in its:
        if i["Part Number"] == part_nums:
            return i
    raise ItemError("Item not found for part number: '" + part_nums + "'")

def item_gen(line:str)->dict:
    new_item = dict()
    for i,field in enumerate(fields):
        if line[i] == "":
            line[i] == "NA"
        if field == "Verified Date":
            new_item[field.fieldname] = str(datetime.datetime.now())
        new_item[field.fieldname] =line[i]
    return new_item

sql_setup()

sql_conn.commit()