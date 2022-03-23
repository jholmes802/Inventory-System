""" This doc has a series of variables that will be used globally."""
def init():
    global DBSetup, hostname, serverport, verboselvl, config, config_ran, config_path, verbose
    DBSetup = False # type: bool
    hostname = None # type: str
    serverport = None # type: str
    verboselvl = 1 # type: int
    config = dict() # type: dict[str,str]
    config_ran = False #type: bool
    config_path = None # type: str
    verbose = True # type: bool