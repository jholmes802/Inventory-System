import dataio
import db_manager
import barcodes
import json
import html_builder as bob

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
        dataio.parts.new_item(data['part_number'], data['part_name'], data["part_qty"])
        return str("Created new part: " + data["part_number"])
    except:
        return str("Could not create new part with part number" + data["part_number"])


