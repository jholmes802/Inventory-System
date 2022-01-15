#!/usr/bin/python3
from xml.dom import minidom
import os
import datetime
import sqlite3
import db_manager
import pathlib
from logger import logger

global config_file, items_file, fields, verbose
verbose = False
config_file = "../data/config.csv"
items_file = '../data/items.csv'
log_level = 2

def _now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

db_manager.sql_setup()

class ItemError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class FileError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

def mass_import_items(path:str)->None:
    """Not ready for production. It is used to initalize the primary db with data from a csv.

    Args:
        path (str): Path to a csv file. Must contain

    CSV File Requirements:
        Fields, must contain: A "part number" field, that is unique to each part.
            "part Name" field that is the name/desc for the part, does not need to be unique
            "quantity" field that is an integer, and is the quantity of the part.

    Raises:
        FileError: [description]
    """
    db_manager.sql_setup()
    if not path.endswith(".csv"):
        raise FileError("Improper File type, needs to be a csv format.")
    fhand = open(path, 'r', encoding='utf-8-sig')
    fread = fhand.readlines()
    part_num_poss = ["PART_NUM", "PART_NUMBER", "PART NUM", "PART NUMBER"]
    part_name_poss = ["PART_NAME", "PART NAME", "PART_NAM"]
    qty_poss = ["PART_QTY","PART_QUANTITY","PART QTY","PART QUANTITY", "QUANTITY", "QTY"]
    first = True
    for i, line in enumerate(fread):
        line = line.rstrip("\n").split(",")
        print(line)
        if first:
            first = False
            fields:list = [x.upper() for x  in line ]
            for p in part_num_poss:
                if p in fields:
                    p_num_index = fields.index(p)
                    logger(log_level, "Dataio.mass_import_items: Found Part Number field.")
                    break
            for p in part_name_poss:
                if p in fields:
                    logger(log_level, "Dataio.mass_import_items: Found Part Name field.")
                    p_name_index = fields.index(p)
                    break
            for p in qty_poss:
                if p in fields:
                    logger(log_level, "Dataio.mass_import_items: Found Qty field.")
                    qty_index = fields.index(p)
                    break
        else:
            if len(line)< 2:
                logger(log_level, "Dataio.mass_import_items Could not import this line.")
            else:
                try:
                    p_num = line[p_num_index].strip()
                    p_name = line[p_name_index]
                    qty = line[qty_index]
                    parts.new_item(p_num, p_name, qty)
                    print("PartNum:", p_num)
                    logger(log_level, "Dataio.mass_import_items: Created new item! With part number: " + line[p_num_index])
                except: print("Uhoh")
            
class transactions:
    def transaction(part_num:str, qty:int, typ:str, dest:str = "cabinet", source:str = "", notes:str = "")-> bool:
        """Creates a new transactional record and updates appropriate item.

        Args:
            part_num (str): Part number to be updated.
            qty (int): Qty of change, does not support negatives.
            typ (str): "OUT": removing item from source and into destination, "IN" pulls items from source and into dest. USED ONLY IN BACKEND.
            dest (str, optional): Destination of where item is going. Should be from a list of destinations. Defaults to "cabinet".

        Raises:
            ItemError: Raised if part number does not exsist.

        Returns:
            bool: Used as a it worked.

        -- Change Log --
            - 1/1/22 -- Currently works, does not need major changes.
                - Would benefit from additional checks.
        """
        if typ == "OUT":
            equ = "qty = qty - "
        elif typ == "IN":
            equ = "qty = qty + "
        if parts.part_num_check(part_num):
            logger(log_level, "Dataio.transaction: Part num exsists in the db.")
            tstamp = _now()
            sql_transaction = "INSERT INTO transactions ('part_number', 'type', 'qty', 'destination','source', 'notes', 'datetime') VALUES ('" + part_num + "', '" + typ + "', " + qty + ",'" + dest + "','"+ source + "','"+ notes + "','" + tstamp + "');"
            if typ=="VERIFY":
                sql_update = "UPDATE items SET qty = " + qty + ", verified_date = '" + tstamp + "' WHERE part_number = '" + part_num + "';"
            else:    
                sql_update = "UPDATE items SET " + equ + qty + " WHERE part_number = '" + part_num + "';"
            db_manager.run(sql_transaction)
            logger(log_level, "Dataio.transaction: Adding transactional record.")
            db_manager.run(sql_update)
            logger(log_level, "Dataio.transaction: Updated items db record for part_number: '" + part_num + "'.")
        else:
            print("ERROR! Could not find part number")
            raise ItemError("Part Number could not be found.")
        return True

    def get_transactions(starttime:str or datetime=None, endtime: str or datetime=None,types:str or list=None, cnt:int = -1) -> list[list]:
        """Setup to return a list of transactions.

        Args:
            starttime (str or datetime, optional): str of startime for the filter. Defaults to None.
            endtime (str or datetime, optional): endtime filter.. Defaults to None.
            types (str or list, optional): can be used to filter by types. Defaults to None.

        Returns:
            list[list]: Records from transactions.
        """
        if starttime == None and endtime == None and types == None:
            return db_manager.run_retrieve("SELECT * FROM transactions;", cnt)
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
            return db_manager.run_retrieve(sql, cnt)

class locations:
    def getAll():
        sql = "SELECT * FROM locations;"
        results = db_manager.run_retrieve(sql)
        fields = [x.split(" ")[0] for x in db_manager.tables['locations']]
        return (fields, results)
        
    def new(self, loc_name, typ, desc):
        sql = "INSERT INTO locations (name, type, desc) VALUES (" + ", ".join([loc_name, typ, desc]).rstrip(",").lstrip(",") + ");"

class parts:
    def delete_part(part_num:str, transactions=False):
        db_manager.backup()
        db_manager.run("DELETE FROM items WHERE part_number='"+ part_num + "';")
        if transactions: db_manager.run("DELETE FROM transactions WHERE part_number='"+ part_num + "';")
    
    def part_num_check(prt_num)->bool:
        """Checks if a part number already exsists in the items.part_number field.

        Args:
            prt_num (str): Part number to be checked.
        Return:
            bool: True means it already is in the db.
        """
        in_db = [x[0] for x in db_manager.run_retrieve("SELECT part_number FROM items;")]
        logger(log_level,"Dataio.part_num_check: Found " + str(len(in_db)) + " part numbers in db.")
        logger(log_level, "Dataio.part_num_check: Status of part number entered: " + prt_num + " in db")
        return prt_num in in_db

    def new_item(part_num, part_name, qty=""  ,threshold = 0, depend = None, verified=None, alt_part_num = None ,notes:str="", check:bool = True)-> None:
        """Creates a new item in the items database table.
        Supports logging.

        Args:
            part_num (str): part number of the new item.
            part_name (str): part name of the new item.
            qty (str, optional): The quantity of the part if known. Defaults to "".
            threshold (int, optional): Sets a low limit threshold of the part. Defaults to 0.
            depend (str, optional): Any part_number dependencies, if other parts are required to make it run. Defaults to None.
            verified (datetime, optional): If applicable, its the date the qty was verified. Defaults to None.
            alt_part_num (str, optional): Alternate part numbers for this item, ie VexPro and WCP part numbers. Defaults to None.
            check (bool, optional): bool to check if the part already exsits. Defaults to True.

        Raises:
            ItemError: raised if the part already exsits the in the db.

        --Change Log--
        1/1/22 - Works at base level. Supports logging.
            - Should add support for checking bool.
            - Should add handeling for if the part number already exsists.
        """
        db_manager.backup()
        if qty == "" or qty==None: qty=0
        logger(log_level, "DataIO.new_item: Creating new item with part number: '" + part_num + "'")
        if parts.part_num_check(part_num):
            raise ItemError("Item Already Exsists in the db.")
        else:
            values = [part_num, part_name, qty, threshold, depend, verified, alt_part_num, "search_parms", notes]
            for i, val in enumerate(values):
                if val == None:
                    values[i] = "NULL"
                else:
                    values[i] = "'" + str(val) + "'"
                if val == 'search_parms':
                    values[i] = "'"
                    if part_num != None:
                        values[i] += str(part_num) + " "
                    if part_name != None:
                        values[i] += str(part_name) + " "
                    if alt_part_num != None:
                        values[i] += str(alt_part_num) + " "
                    values[i] += "'"
            
            values = ",".join(values).lstrip(",").rstrip(',')
            sql = "INSERT INTO items (" + ",".join(db_manager.columns['items']).lstrip(",").rstrip(',') + ") VALUES (" + values + ")"
            db_manager.run(sql)
            logger(log_level, "DataIO.new_item: Added new item to db.items. ")
    def find(part_num:str):
        """Find a part_num in db.items and returns it. 
        Returns all fields in db.items 
        Args:
            part_num (str): Part number to be found.

        Returns:
            tuple(fields, results): fields are the fields from db.items, and results for that record. Only returns the FIRST record.

        --Change Log--
            - 1/1/22 -- Works and needs no current changes.
                -Could probably benefit from checking if there is more than one record.
                -Current does not support if part number has types ie 217-6515 has 217-6515 and 217-6515A etc...
                    -Also no current plan to do such implementation.
        """
        sql = "SELECT * from items where part_number = '" + part_num + "';"
        sql_results = db_manager.run_retrieve(sql)
        logger(log_level, "Dataio.find: Found " + str(len(sql_results)) + "where items.part_number ='" + part_num + "'.")
        fields = [x.split(" ")[0] for x in db_manager.tables['items']]
        results = [x for x in sql_results[0]] 
        return (fields, results)
    def get_all_items(ints=-1)->list[list]:
        """Takes no parameters, returns a set list of fields. 
        Returns the following fields...
        -items.part_number
        -items.part_name
        -items.qty
        -items.verified_date
        -catalog.source_name
        -catalog._source_link
        -catalog.price
        -catalog.unit
        -catalog.unit_qty
        -items.search_parms

        Returns:
            tuple(results, fields): Returns the results as list[tuples] and fields and a list.
        """
        logger(log_level, "Dataio.get_all_items: Retrieving Primary Stock Table.")
        sql = "SELECT items.part_number, items.part_name, items.qty, items.verified_date, catalog.source_name, catalog.source_link, catalog.price, catalog.unit, catalog.unit_qty, items.search_parms FROM items LEFT JOIN catalog ON items.part_number = catalog.part_number;"
        sql_results = db_manager.run_retrieve(sql,ints)
        fields = ('part_number', 'part_name', 'qty', 'verified_date', 'source_namne', 'source_link', "price", 'unit', 'unit_qty', 'search_parms')
        logger(log_level, "Dataio.get_all_items: Returned " + str(len(sql_results)) + " results.")
        return (sql_results, fields)

class catalog:
    def get_all(num=-1):
        sql = "SELECT * FROM catalog;"
        fields = db_manager.tables["catalog"]
        return(fields, db_manager.run_retrieve(sql, num))
    def new_catalog(part_number="", part_name="", source_name="", source_link="", manufacturer="", man_link="", price="", unit="", unit_qty="", notes=""):
        fields = {"part_number":part_number, "part_name":part_name, "source_name":source_name, "source_link":source_link, "manufacturer":manufacturer, "man_link":man_link, "price":price, "unit":unit, "unit_qty":unit_qty, "notes":notes}
        sql = "INSERT INTO ()"
if __name__ == "__main__":
    mass_import_items("../2022 1073 Stock Current (only) - Current Stock.csv")
    pass