#!/usr/bin/python3
import dataio
import barcodes
import db_manager
import g_backup
from tools import *


def checkout_post(data: dict)-> bytes:
    dataio.transactions.checkio(data['part_uuid'], data["qty"], 'OUT')
    return "Transaction Logged"

def verify(data: dict)-> bytes:
    dataio.transactions.verify(data['part_number'], data['qty'])
    return "Verified part!"

def checkin(data:dict)->str:
    dataio.transactions.checkio(data['part_uuid'], data["qty"], 'IN')
    return "Transaction Logged"

def new_item(data:dict):
    if data["part_number"] == "":
        return str("Must have a part number!")
    print("Creating new item")
    dataio.items.new(data)
    return str("Created new part: " + data["part_number"])

def print_barcode(data:dict):
    barcodes.print_barcode(data["part_uuid"])
    return str("Printed!")

def backup(data:dict):
    db_manager.db.backup()
    g_backup.g_backup()
    return "Backup was sucessful."

def editpart(data:dict):
    dataio.items.edit(data)
    return "Edited part!"

def newuser(data:dict):
    return "Oops not implemented!"

def itemstatus(data:dict):
    dataio.items.status(data["part_uuid"], data["status"])
    return "Sucess!"