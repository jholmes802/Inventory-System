#!/usr/bin/python3
import dataio
import barcodes
import db_manager
import g_backup
from sup_errors import *


def checkout_post(data: dict)-> bytes:
    try:
        dataio.transactions.transaction(data['part_number'], data["qty"], 'OUT', notes=data['notes'])
        return "Transaction Logged"
    except:
        return "Uh-Oh Something went wrong!"

def verify(data: dict)-> bytes:
    try:
        dataio.transactions.transaction(data['part_number'], data["qty"], 'VERIFY')
        return "Verified part!"
    except:
        return "Uh-Oh Something went wrong!"
def checkin(data:dict)->str:
    try:
        dataio.transactions.transaction(data['part_number'], data["qty"], 'IN', notes=data['notes'])
        return "Transaction Logged"
    except:
        return "Uh-Oh Something went wrong!"

def new_item(data:dict):
    if data["part_number"] == "":
        return str("Must have a part number!")
    try:
        print("Creating new item")
        dataio.parts.new_item(data['part_number'], data['part_name'], data["part_qty"])
        return str("Created new part: " + data["part_number"])
    except:
        return str("Could not create new part with part number" + data["part_number"])

def print_barcode(data:dict):
    try:
        if not barcodes.check_barcodes([data["part_number"]]):
            f, dbr = dataio.parts.find(data["part_number"])
            barcodes.barcode_gen(data["part_number"], dbr[1])
        barcodes.print_barcode(data["part_number"])
        return str("Printed!")
    except:
        return str("Uh oh something went wrong")

def backup(data:dict):
    try:
        db_manager.backup()
        g_backup.g_backup()
        return "Backup was sucessful."
    except:
        return "Backup was not sucessful."

def editpart(data:dict):
    return "Uh ohhhh...."
