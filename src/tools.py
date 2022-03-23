#!/usr/bin/python3
from io import FileIO
import pathlib, datetime, json, invvars, os

class DataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ConfigError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class dbError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class BackUpError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NotReadyError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ItemError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class FileError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class dbEntryError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

def read_file(path):
    fhand = open(pathlib.Path(path), "rb")
    fread = fhand.read()
    fhand.close()
    return fread

def now(path_fiendly=False): 
    if path_fiendly:
        return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace("-", "_").replace(" ", "_").replace(":", "")
    else:
        return str(datetime.datetime.now())


def logger(lvl,msg):
    """Prints logging statements based on logging level, and message.

    Args:
        lvl (int): 0: Lowest Detail, 1: Moderate Detail, 2: Highest Detail logged into a file.
        msg (str): str message.
    """    
    lmsg = now() + ": " +  str(msg)
    if lvl == 0 and lvl == invvars.verboselvl:
        print(now() + ": " + str(msg))
    elif lvl == 1 and lvl == invvars.verboselvl:
        fhand = open('./logs/log-' + now().split(" ")[0] + ".txt", 'a')
        fhand.write(lmsg + "\n")
        fhand.close()
    if invvars.verbose:
        print(lmsg)

def post_dic_cleaner(item:dict)->dict:
    result = {}
    for k in item.keys():
        if item[k] == "None":
            result[k] = None
        else:    
            result[k] = item[k]
    return result

def load_config():
    cwdlst = os.listdir(os.getcwd())
    for i in cwdlst:
        if i.startswith("config") and i.endswith(".json"):
            invvars.config_path = i
            fhand:FileIO = open(i, "r")
            fread = fhand.read()
            result = json.loads(fread)
            invvars.config = result
            invvars.config_ran = True
            logger(1,"tools.load_config: Loaded '" + i + "' in.")
            return None
    logger(1,"tools.load_config: Unable to find a config file.")

if __name__ == "__main__":
    invvars.init()
    load_config()