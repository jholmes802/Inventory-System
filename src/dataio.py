#!/usr/bin/python3
import datetime
from typing import List, Set, Dict, Tuple, Optional
import db_manager
from logger import logger
from sup_errors import *
import uuid

global config_file, items_file, fields, verbose
verbose = False
config_file = "../data/config.csv"
items_file = '../data/items.csv'
log_level = 2

def _now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
    raise NotReadyError("Not implemented yet, sorry!")
    db = db_manager.db()
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
    def status(part_number, status):
        prt_uuid = items.find(part_number)["part_number"]
        db = db_manager.db()
        conn = db.engine.connect()
        conn.execute(db.table["transactions"].insert({"datetime": _now(), "part_number_uuid":prt_uuid, "typ":status}))
        conn.close()

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

class items:
    def status(part_num:str, status):
        if status not in ["INUSE", "ARCHIVED"]:
            raise dbEntryError("Cannot utilize listed status.")
        transactions.status(part_num, status)
        db = db_manager.db()
        db.engine.connect().execute(db.table["items"].update().where(db.table["items"].c.part_number == part_num).values({"status":status})).close()
    
    def num_check(prt_num)->bool:
        """Checks if a part number already exsists in the items.part_number field.

        Args:
            prt_num (str): Part number to be checked. IS CASE SENSITIVE!
        Return:
            bool: True means it already is in the db.
        """
        db = db_manager.db()
        conn = db.engine.connect()
        res = conn.execute(db.table["items"].select().where(db.table["items"].c.part_number == prt_num)).all()            
        conn.close()
        logger(log_level,"Dataio.part_num_check: Found " + str(len(res)) + " part numbers in db.")
        logger(log_level, "Dataio.part_num_check: Status of part number entered: " + prt_num + " in db")
        return len(res) == 1

    def new(item:dict, verify_part_num:bool = True)-> None:
        """Creates a new item in the items database table.
        Supports logging
        Args:
            item: dict: should be the dictionary matching the table structure.
            This dictionary this should match the user defined columns from the data_struc.json
        Raises:
            ItemError: raised if the part already exsits the in the db.
        """
        if verify_part_num: item["part_number"] = tools.verify_part_num(item["part_number"])
        logger(log_level, "DataIO.new_item: Creating new item with part number: '" + item["part_number"] + "'")
        if items.num_check(item["part_number"]):
            logger(log_level, "dataio.item.new: Already found part number in db.")
            raise ItemError("Item Already Exsists in the db.")
        new_id = tools.new_uuid()
        item["part_uuid"] = new_id
        item["status"] = "INUSE"
        db = db_manager.db()
        db.backup()
        conn = db.engine.connect()
        conn.execute(db.table["items"].insert(values=item))
        conn.execute(db.table["uuids"].insert(values={"uuid":new_id, "typ":"item"}))
        conn.close()
        logger(log_level, "DataIO.new_item: Added new item to db.items.")

    def find(part_num:str)-> Dict[str, str]:
        """Find a part_num in db.items and returns it. 
        Returns all fields in db.items 
        Args:
            part_num (str): Part number to be found.

        Returns:
            dict: column name and data
        """
        db = db_manager.db()
        conn = db.engine.connect()
        res = conn.execute(db.table["items"].select().where(db.table["items"].c.part_number == part_num)).all()[0]
        conn.close()
        fields = [x.name for x in db.table["items"].columns]
        logger(log_level, "Dataio.find: Found " + str(len(res)) + "where items.part_number ='" + part_num + "'.")
        return {fields[i]:res[i] for i in range(0,len(fields))}

    def get_all(status:str="INUSE")->list[list]:
        """Only takes status, which is either "INUSE" or "ARCHIVED"
        Returns:
            tuple(fields, results): Returns the fields and a list and results as list[tuples].
        """
        logger(log_level, "Dataio.get_all_items: Retrieving Primary Stock Table.")
        db = db_manager.db()
        conn = db.engine.connect()
        res = conn.execute(db.table["items"].select()).all()
        conn.close()
        fields = [x.name for x in db.table["items"].columns]
        logger(log_level, "Dataio.get_all_items: Returned " + str(len(res)) + " results.")
        return (fields, res)

class catalog:
    def get_all(num=-1):
        sql = "SELECT * FROM catalog;"
        fields = db_manager.tables["catalog"]
        return(fields, db_manager.run_retrieve(sql, num))
    def new_catalog(part_number="", part_name="", source_name="", source_link="", manufacturer="", man_link="", price="", unit="", unit_qty="", notes=""):
        fields = {"part_number":part_number, "part_name":part_name, "source_name":source_name, "source_link":source_link, "manufacturer":manufacturer, "man_link":man_link, "price":price, "unit":unit, "unit_qty":unit_qty, "notes":notes}
        sql = "INSERT INTO ()"
        
class tools:
    def new_uuid():
        while True:
            ret = str(uuid.uuid4())
            db = db_manager.db()
            conn = db.engine.connect()
            sqlr = conn.execute(db.table["uuids"].select().where(db.table["uuids"].c.uuid == ret)).all() 
            if len(sqlr) < 1:
                return ret
    def verify_part_num(part_num:str):
        return part_num.upper()


if __name__ == "__main__":
    #mass_import_items("../2022 1073 Stock Current (only) - Current Stock.csv")
    dic = {
        "part_number": "1073-test",
        "part_name": "testpart",
        "qty":0,
        "threshold_qty":1,
        "tags":"test, part, 1073"
    }
    #items.new(dic)
    
    pass