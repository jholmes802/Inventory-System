from xml.dom import minidom
import os
import datetime
import sqlite3
import db_manager
import pathlib

global config_file, items_file, fields, verbose
verbose = False
_sql_conn=sqlite3.connect("../data/inv_data.db")
_sql_cur = _sql_conn.cursor()
config_file = "../data/config.csv"
items_file = '../data/items.csv'
if "verbose.dat" in os.listdir(os.getcwd()):
    verbose = True

def now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def cursor_gen(conn): return (conn.cursor())

def conn_gen(): return (sqlite3.connect('../data/inv_data.db'))

db_manager.sql_setup()

class ItemError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

def get_all_items()->list[list]:
    sql = "SELECT items.part_number, items.part_name, items.qty, items.verified_date, catalog.source_name, catalog.source_link, catalog.price, catalog.unit, catalog.unit_qty FROM items LEFT JOIN catalog ON items.part_number = catalog.part_number;"
    _sql_conn = conn_gen()
    _sql_cur = cursor_gen(_sql_conn)
    sql_results = _sql_cur.execute(sql).fetchall()
    fields = ('part_number', 'part_name', 'qty', 'verified_date', 'source_namne', 'source_link', "price", 'unit', 'unit_qty')
    _sql_conn.close()
    return (sql_results, fields)

def part_num_check(prt_num)->bool:
    """Checks if a part number already exsists in the items.part_number field.

    Args:
        prt_num (str): Part number to be checked.
    Return:
        bool: True means it already is in the db.
    """
    _sql_conn = conn_gen()
    _sql_cur = cursor_gen(_sql_conn)
    in_db = [x[0] for x in _sql_cur.execute("SELECT part_number FROM items;").fetchall()]
    if verbose: print(now() + ":Dataio.part_num_check: Found", len(in_db), "part numbers in db.")
    if verbose: print(now() + ":Dataio.part_num_check: Status of part number entered:", prt_num in in_db)
    _sql_conn.close()
    return prt_num in in_db

def new_item(part_num, part_name, qty=""  ,threshold = 0, depend = None, verified=None, alt_part_num = None , check:bool = True)-> None:
    backup()
    _sql_conn = conn_gen()
    _sql_cur = cursor_gen(_sql_conn)
    if qty == "" or qty==None: qty=0
    if verbose: print(now() + ": DataIO.new_item: Creating new item with part number: '" + part_num + "'")
    if part_num_check(part_num):
        raise ItemError("Item Already Exsists in the db.")
    else:
        values = [part_num, part_name, qty, threshold, depend, verified, alt_part_num]
        for i, val in enumerate(values):
            if val == None:
                values[i] = "NULL"
            else:
                values[i] = "'" + str(val) + "'"
        values = ",".join(values).lstrip(",").rstrip(',')
        if verbose: print(now() + ": DataIO.new_item: Adding item to db. ")
        _sql_cur.execute("INSERT INTO items (" + ",".join(db_manager.columns['items']).lstrip(",").rstrip(',') + ") VALUES (" + values + ")")
        print(_sql_cur.fetchall())
        _sql_conn.commit()
        if verbose: print(now() + ": DataIO.new_item: Item added to db.")
    _sql_conn.commit()
    _sql_conn.close()

def find(part_num:str):
    _sql_conn = conn_gen()
    _sql_cur = cursor_gen(_sql_conn)
    sql = "SELECT items.part_number, items.part_name, items.qty, items.threshold_qty, items.verified_date from items where part_number = '" + part_num + "';"
    sql_results = _sql_cur.execute(sql).fetchall()
    fields = [x.split(".")[1].rstrip(",") for x in sql.split(" ")[1:-6]]
    results = [x for x in sql_results[0]] 
    return (fields, results )

def transaction(part_num:str, qty:int, typ:str, dest:str = "cabinet")-> bool:
    _sql_conn = conn_gen()
    _sql_cur = cursor_gen(_sql_conn)
    if part_num_check(part_num):
        tstamp = now()
        sql_transaction = "INSERT INTO transactions ('part_number', 'type', 'qty', 'destination', 'datetime') VALUES ('" + part_num + "', '" + typ + "', " + qty + ",'" + dest + "','" + tstamp + "');"
        print(sql_transaction)
        sql_update = "UPDATE items SET qty = qty - " + qty + " WHERE part_number = '" + part_num + "';"
        _sql_cur.execute(sql_transaction)
        _sql_cur.execute(sql_update)
        _sql_conn.commit()
    else:
        raise ItemError("Part Number could not be found.")
    _sql_conn.close()
    return True

def get_transactions(starttime:str or datetime=None, endtime: str or datetime=None,types:str or list=None) -> list[list]:
    _sql_conn = conn_gen()
    _sql_cur = cursor_gen(_sql_conn)
    if starttime == None and endtime == None and types == None:
        return _sql_cur.execute("SELECT * FROM transactions;").fetchall()
    elif types != None:
        
        sql = "SELECT * FROM transactions WHERE type in (" 
        if type(types) == list:
            for t in types:
                sql += "'" + t + "',"
            sql = sql.rstrip(",") + ")"
        elif type(types) == str:
            sql = "SELECT * FROM transactions where type = '" + types + "'"
        else:
            return 0
        sql = sql + "ORDER BY datetime desc;"
        _sql_cur.execute(sql)
        return _sql_cur.fetchmany(10)         

def to_xml1(format: str, data:list[list])-> any:
    fields = [x.split(" ")[0] for x in db_manager.tables[format]]
    xmlpath = '../data/xml/' + now().replace(":", '_').replace(" ", "_") +"_" + format + ".xml"
    fhand = open(xmlpath, 'w')
    fhand.write("<?xml version='1.0'?>\n")
    fhand.write("<transactions>\n")
    if format == 'transactions':
        for d in data:
            fhand.write("\t<transaction>\n")
            for i in range(0, len(fields)):
                fhand.write("\t\t<" + str(fields[i]) + ">" + str(d[i]) + "</" + str(fields[i]) + ">\n")
            fhand.write("\t</transaction>\n")
    fhand.write("</transactions>")
    return xmlpath
        
def delete_part(part_num:str, transactions=False):
    backup()
    _sql_conn = conn_gen()
    _sql_cur = cursor_gen(_sql_conn)
    _sql_cur.execute("DELETE FROM items WHERE part_number='"+ part_num + "';")
    if transactions: _sql_cur.execute("DELETE FROM transactions WHERE part_number='"+ part_num + "';")
    _sql_conn.commit()
    return 0

def backup():
    """Creates a new backup folder in "../backup/" for the current date and time.
    Creates a csv file from each db table into there.

    """
    _sql_conn = conn_gen()
    _sql_cur = cursor_gen(_sql_conn)
    backup_path = '../backup/'+ now().replace(" ","_").replace(":","_") + "/"
    os.mkdir(backup_path)
    for t in db_manager.tables.keys():
        file_path = pathlib.Path(backup_path + t + ".csv")
        fhand = open(file_path, "w")
        fhand.write(", ".join([x.split()[0] for x in db_manager.tables[t]]).lstrip(',').rstrip(",")+"\n")
        sql = _sql_cur.execute("SELECT * FROM " + t + ";").fetchall()
        for r in sql:
            fhand.write(", ".join([str(x) for x in r]).rstrip(",").lstrip(",") + "\n")
        fhand.close()

_sql_conn.commit()
_sql_conn.close()

if __name__ == "__main__":
    to_xml('transactions', get_transactions(types=['OUT', "IN"]))
    pass