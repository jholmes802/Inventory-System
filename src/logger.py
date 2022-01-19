#!/usr/bin/python3
import datetime

def _now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
def logger(lvl,msg):
    """Prints logging statements based on logging level, and message.

    Args:
        lvl (int): 0: Lowest Detail, 1: Moderate Detail, 2: Highest Detail logged into a file.
        msg (str): str message.
    """
    
    if lvl == 0:
        print(_now() + ": " + str(msg))
    elif lvl == 1:
        print(_now() + ": " + str(msg))
    elif lvl == 2:
        fhand = open('./logs/log-' + _now().split(" ")[0] + ".txt", 'a')
        fhand.write(_now() + str(msg) + "\n")
        fhand.close()