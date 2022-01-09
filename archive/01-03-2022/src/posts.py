import dataio
import db_manager
import barcodes
import json

def checkout_post(data: dict)-> bytes:
    dataio.transactions.transaction(data['part_number'], data["qty"], 'OUT')

def new_item(data:dict):
    pass