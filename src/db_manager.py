#!/usr/bin/python3
from typing import List, Set, Dict, Tuple, Optional
from logger import logger
import datetime
import os
import pathlib
import sqlalchemy
import g_backup
import json
from sup_errors import *
import shutil

if sqlalchemy.__version__ != "1.4.29":
    print(sqlalchemy.__version__, "not correct version. Please use 1.4.29")

def _now(path_fiendly=False): 
    if path_fiendly:
        return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace("-", "_").replace(" ", "_").replace(":", "")
    else:
        return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

logl = 2

class db:
    def __init__(self, dbSetupPath="dat_struc.json") -> None:
        self.dbSetupPath:str = dbSetupPath
        self.dbSetupConfig:dict = json.loads(open(self.dbSetupPath).read())
        self.type:str = self.dbSetupConfig["db_type"]
        self.db_path:str = self.dbSetupConfig["db_path"]
        self.setupTables:List[Dict[str, str]] = self.dbSetupConfig["tables"]
        self._engine()
        self._tables()

    def _engine(self) -> None:
        self.engine: sqlalchemy.engine = sqlalchemy.create_engine("sqlite+pysqlite:///../data/inv_data2.db")
        self.meta: sqlalchemy.MetaData = sqlalchemy.MetaData(self.engine)
        self.inspector: sqlalchemy.inspection = sqlalchemy.inspect(self.engine)
    
    def _tables(self) -> sqlalchemy.Table:
        self.table:Dict[str, sqlalchemy.Table] = dict()
        for itable, table in enumerate(self.setupTables):
            for i, col in enumerate(table["table_cols"]):
                dtype = col["data_type"].upper()
                if dtype == "STRING": self.setupTables[itable]["table_cols"][i]["data_type"] = sqlalchemy.String
                elif dtype == "INTEGER": self.setupTables[itable]["table_cols"][i]["data_type"] = sqlalchemy.Integer
                elif dtype == "REAL": self.setupTables[itable]["table_cols"][i]["data_type"] = sqlalchemy.Float
                else: raise ConfigError(dtype + " : is not a recognized data type. Please refer to SQLAlchemy supported types.")
            self.table[table["table_name"]] = sqlalchemy.Table(
                table["table_name"],
                self.meta,
                *[sqlalchemy.Column(col["col_name"], col["data_type"], primary_key=bool(col["primary_key"]), nullable=bool(col["nullable"])) for col in table["table_cols"]]
            )
        self.meta.create_all()
    def run(self, sql_str)-> bool:
        try:
            cur = self.engine.connect()
            cur.execute(sqlalchemy.sql.text(sql_str))
            cur.close()
            return True
        except:
            return False
    def run_retrieve(self, sql_str):
        try:
            cur = self.engine.connect()
            res = cur.execute(sqlalchemy.sql.text(sql_str)).all()
            cur.close()
            return res
        except:
            raise dbError("There was an error running the sql code.")

    def backup(self, gsheet:bool=False, backup_path:str or pathlib = "../backup/", clean_up:bool=True):
        datetimestamp = _now(True)
        logger(logl, "db.Backup: Starting backup at: " + datetimestamp)
        
        if backup_path.endswith("/"):
            bpath = backup_path + datetimestamp + "/"
        else:
            bpath = backup_path + "/" + datetimestamp + "/"
        
        if not os.path.exists(backup_path):
            logger(logl, "db.backup: Could not find the listed base backup directory: " + backup_path)
            raise BackUpError("Listed backup path does not exsit.")
       
        if clean_up:
            dirlist = os.listdir(backup_path)
            if len(dirlist) < 30:
                pass
            else:
                _kill_list = dirlist[:-30]
                i = 0
                for k in _kill_list:
                    for item in os.listdir(backup_path + k):
                        os.remove(backup_path + k + "/" + item)
                    os.removedirs(backup_path + k)
                    logger(logl, "db.backup: Removed backup for " + k)
                    i += 1
                logger(logl, "db.backup: Removed " + str(i) + " old backups.")
        
        if not os.path.exists(bpath):
            os.mkdir(bpath)
            logger(logl, "db.backup: Created new backup folder at: " + bpath)
        
        try:
            shutil.copy(self.db_path, bpath)
            logger(logl, "db.backup: Copied primary db file into backup path.")
        except:
            logger(logl, "db.backup: Could NOT copy primary db file to backup path.")
            raise BackUpError("Could not copy primary db file to specified path")
        
        for table in self.table.keys():
            sql = "SELECT * FROM " + self.table[table].name
            sql_res = self.run_retrieve(sql)
            fields = [x.name for x in self.table[table].columns]
            tablepath = bpath + table + ".csv"
            tablehand = open(tablepath,"x")
            tablehand.write(",".join(fields).lstrip(",").rstrip(",") + "\n")
            rowi = 0
            for res in sql_res:
                tablehand.write(",".join([str(r) for r in res]).lstrip(",").rstrip(",") + "\n")
                rowi += 1
            logger(logl, "db.backup: Created csv for " + table + " table, with " + str(rowi) + " rows.")
        
        if gsheet:
            g_backup.g_backup()
            logger(logl, "db.backup: Updated Google Sheet.")


if __name__ == "__main__":
    d = db()
    print(d.inspector.get_table_names())
    d.backup(clean_up=True)