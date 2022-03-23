#!/usr/bin/python3

import g_backup,tools, invvars, db_manager, barcodes, dataio


def checkout_post(data: dict)-> bytes:
    try:
        dataio.transactions.checkio(data['part_uuid'], data["qty"], 'OUT')
        return "Transaction Logged"
    except:
        return "Uh-Oh Something went wrong!"

def verify(data: dict)-> bytes:
    try:
        dataio.transactions.verify(data['part_number'], data['qty'])
        return "Verified part!"
    except:
        return "Uh-Oh Something went wrong!"
def checkin(data:dict)->str:
    try:
        dataio.transactions.checkio(data['part_uuid'], data["qty"], 'IN')
        return "Transaction Logged"
    except:
        return "Uh-Oh Something went wrong!"

def new_item(data:dict):
    if data["part_number"] == "":
        return str("Must have a part number!")
    try:
        print("Creating new item")
        dataio.items.new(data)
        return str("Created new part: " + data["part_number"])
    except:
        return str("Could not create new part with part number" + data["part_number"])

def print_barcode(data:dict):
    try:
        if not barcodes.check_barcodes([data["part_uuid"]]):
            f, dbr = dataio.items.find(data["part_uuid"])
            barcodes.barcode_gen(data["part_uuid"], dbr[1])
        barcodes.print_barcode(data["part_uuid"])
        return str("Printed!")
    except:
        return str("Uh oh something went wrong")

def backup(data:dict):
    try:
        db_manager.db.backup(ghseet=True)
        return "Backup was sucessful."
    except:
        return "Backup was not sucessful."

def editpart(data:dict):
    dataio.items.edit(data)
    return "Edited part!"

def newuser(data:dict):
    return "Oops not implemented!"

def itemstatus(data:dict):
    dataio.items.status(data["part_uuid"], data["status"])
    return "Sucess!"
