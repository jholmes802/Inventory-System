#!/usr/bin/python3
from typing import List, Dict
import os,pathlib, sqlalchemy, g_backup, json, tools, shutil, invvars

class db:
    def __init__(self, dbSetupPath="dat_struc.json"):
        """This creates a db access obj. This contains the engine, metadata and inspector from SQLAlchemy.
        It creates the tables, and is able to manipulate the db.
        This is built from the config.json and dat_struc.json
        Args:
            dbSetupPath (str, optional): It is an optional path to the db config file. More info later... Defaults to "dat_struc.json".
        """
        if invvars.config_ran:
            try:
                self.dbSetupPath:str = invvars.config["dbSettings"]["dbSetupPath"]
                self._dbUserName:str = invvars.config["dbSettings"]["dbUserName"]
                self._dbPass:str = invvars.config["dbSettings"]["dbPass"]
                self._dbAddr:str = invvars.config["dbSettings"]["dbHostName"] + ":" +  invvars.config["dbSettings"]["dbPort"]
                self._dbconnector:str = invvars.config["dbSettings"]["dbConnector"]
                self._dbType:str = invvars.config["dbSettings"]["dbType"]
                self._sqlalchemyPath:str = invvars.config["dbSettings"]["sqlalchemyPath"]
                self._dbName:str = invvars.config["dbSettings"]["dbName"]
                if self._sqlalchemyPath.startswith("EXAMPLE"):
                    self._sqlalchemyPath = self._dbType + "+" + self._dbconnector + "://" + self._dbUserName + ":" + self._dbPass + "@" + self._dbAddr + "/" + self._dbName
                if self._sqlalchemyPath == "" or self._sqlalchemyPath == None:
                    self._sqlalchemyPath = self._dbType + "+" + self._dbconnector + "://" + self._dbUserName + ":" + self._dbPass + "@" + self._dbAddr + "/" + self._dbName
            except:
                raise tools.ConfigError("Errory utilizing the config file at: " + invvars.config_path)    
        else:
            self.dbSetupPath:str = dbSetupPath
            tools.logger(1, "db.__init__: Warning inializing without a config file.")
        
        #Loads the database config file.
        try:
            self.dbSetupConfig:dict = json.loads(open(self.dbSetupPath).read())
        except:
            tools.ConfigError("db.__init__: Error reading the Database Structure at: " + self.dbSetupPath)
        self.setupTables:List[Dict[str, str]] = self.dbSetupConfig["tables"]
        self.engine: sqlalchemy.engine.Engine = sqlalchemy.create_engine(self._sqlalchemyPath)
        self.meta: sqlalchemy.MetaData = sqlalchemy.MetaData(self.engine)
        self.inspector: sqlalchemy.engine._reflection.Inspector = sqlalchemy.inspect(self.engine)
        
        #Builds tables normally.
        self.build_tables()
        if not invvars.DBSetup:
            self.build()

    def build_tables(self):
        self.table = dict() # type: dict[str, sqlalchemy.Table]
        
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
                    raise tools.ConfigError(dtype + " : is not a recognized data type. Please refer to SQLAlchemy supported types.")
            
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

    def build(self):
        self.meta.create_all()
        invvars.DBSetup = True

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
            raise tools.dbError("There was an error running the sql code.")

    def backup(self, gsheet:bool=False, backup_path:str or pathlib = "../backup/", clean_up:bool=True):
        datetimestamp = tools.now(True)
        tools.logger(1, "db.Backup: Starting backup at: " + datetimestamp)
        
        if backup_path.endswith("/"):
            bpath = backup_path + datetimestamp + "/"
        else:
            bpath = backup_path + "/" + datetimestamp + "/"
        
        if not os.path.exists(backup_path):
            tools.logger(1, "db.backup: Could not find the listed base backup directory: " + backup_path)
            raise tools.BackUpError("Listed backup path does not exsit.")
       
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
                    tools.logger(1, "db.backup: Removed backup for " + k)
                    i += 1
                tools.logger(1, "db.backup: Removed " + str(i) + " old backups.")
        
        if not os.path.exists(bpath):
            os.mkdir(bpath)
            tools.logger(1, "db.backup: Created new backup folder at: " + bpath)
        
        try:
            shutil.copy(self.db_path, bpath)
            tools.logger(1, "db.backup: Copied primary db file into backup path.")
        except:
            tools.logger(1, "db.backup: Could NOT copy primary db file to backup path.")
            raise tools.BackUpError("Could not copy primary db file to specified path")
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
                tools.logger(1, "db.backup: Created csv for " + table + " table, with " + str(rowi) + " rows.")
        except:
            pass
        
        if gsheet:
            tools.logger(1, "db.backup: Attempting to update the listed google sheet.")
            g_backup.g_backup()
            tools.logger(1, "db.backup: Updated Google Sheet.")


if __name__ == "__main__":
    invvars.init()
    tools.load_config()
    d = db()
    print(d.inspector.get_table_names())
    #d.backup(clean_up=True)