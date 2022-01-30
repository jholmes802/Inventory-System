#!/usr/bin/python3
import pathlib
import datetime

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
    #path = "/app/"  + path.lstrip("../")
    fhand = open(pathlib.Path(path), "rb")
    fread = fhand.read()
    fhand.close()
    return fread

def now(path_fiendly=False): 
    if path_fiendly:
        return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace("-", "_").replace(" ", "_").replace(":", "")
    else:
        return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def logger(lvl,msg):
    """Prints logging statements based on logging level, and message.

    Args:
        lvl (int): 0: Lowest Detail, 1: Moderate Detail, 2: Highest Detail logged into a file.
        msg (str): str message.
    """
    
    if lvl == 0:
        print(now() + ": " + str(msg))
    elif lvl == 1:
        print(now() + ": " + str(msg))
    elif lvl == 2:
        fhand = open('./logs/log-' + now().split(" ")[0] + ".txt", 'a')
        fhand.write(now() + str(msg) + "\n")
        fhand.close()