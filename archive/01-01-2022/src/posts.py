import dataio
import db_manager
import barcodes
import json

def checkout_post(data: dict)-> bytes:
    dataio.transaction(data['part_number'], data["qty"], 'OUT')


j = ('{"part_number":"1073-1","qty":"1"}')
print(json.loads(j)['part_number'])
