#!/usr/bin/python3
from typing import List, Dict
import os
import pathlib
import sqlalchemy
import g_backup
import json
from tools import *
import shutil

logl = 2

class db:
    def __init__(self, dbSetupPath="dat_struc.json"):
        """This creates a db access obj. This contains the engine, and meta data.
        It creates the tables, and is able to manipulate the db.
        Primarily used for its db.engine which .connect() and .execute run sqlalchemy code.
        Args:
            dbSetupPath (str, optional): It is an optional path to the db config file. More info later... Defaults to "dat_struc.json".
        """
        self.dbSetupPath:str = dbSetupPath
        self.dbSetupConfig:dict = json.loads(open(self.dbSetupPath).read())
        self.type:str = self.dbSetupConfig["db_type"]
        self.db_path:str = self.dbSetupConfig["db_path"]
        self.setupTables:List[Dict[str, str]] = self.dbSetupConfig["tables"]

        ### Creates self.engine, meta, and inspector which are objects that provide information about what is in the db.
        
        #Use the line below for a sqlite db
        #self.engine: sqlalchemy.engine = sqlalchemy.create_engine("sqlite+pysqlite:///../data/inv_data2.db")
        
        #Use the line below for mysql db.
        self.engine: sqlalchemy.engine = sqlalchemy.create_engine("mysql+mysqlconnector://invsys:InvSysDB85@localhost/invdb")
        self.meta: sqlalchemy.MetaData = sqlalchemy.MetaData(self.engine)
        self.inspector: sqlalchemy.inspection = sqlalchemy.inspect(self.engine)
        
        ### Beginning creating the tables from the config doc. ###
        self.table:Dict[str, sqlalchemy.Table] = dict()
        
        for itable, table in enumerate(self.setupTables): #This iterates through the config file and creates SQLAlchemy.Table objects under a dictionary.
            for i, col in enumerate(table["table_cols"]):
                dtype = col["data_type"].upper()
                if col["primary_key"] == "True":
                    col["primary_key"] = True
                else:
                    col["primary_key"] = False

                if col["primary_key"] and dtype == "STRING":
                    self.setupTables[itable]["table_cols"][i]["primary_key"] = True
                    self.setupTables[itable]["table_cols"][i]["data_type"] = sqlalchemy.Text(30)
                elif dtype == "STRING":
                    self.setupTables[itable]["table_cols"][i]["data_type"] = sqlalchemy.Text
                elif dtype == "INTEGER":
                    self.setupTables[itable]["table_cols"][i]["data_type"] = sqlalchemy.Integer
                elif dtype == "REAL":
                    self.setupTables[itable]["table_cols"][i]["data_type"] = sqlalchemy.Float
                else:
                    raise ConfigError(dtype + " : is not a recognized data type. Please refer to SQLAlchemy supported types.")
            
            self.table[table["table_name"]] = sqlalchemy.Table(
                table["table_name"],
                self.meta,
                *[sqlalchemy.Column(
                    col["col_name"],
                    col["data_type"],
                    primary_key=col["primary_key"],
                    nullable=bool(col["nullable"])
                    )
                    for col in self.setupTables[itable]["table_cols"]
                ]
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
        datetimestamp = now(True)
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
        try:
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
        except:
            pass
        
        if gsheet:
            g_backup.g_backup()
            logger(logl, "db.backup: Updated Google Sheet.")


if __name__ == "__main__":
    d = db()
    print(d.inspector.get_table_names())
    #d.backup(clean_up=True)