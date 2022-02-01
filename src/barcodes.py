#!/usr/bin/python3
import dataio
import os
import barcode
import barcode.writer as writer
import datetime
from PIL import Image
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
from tools import *

logl = 2

def fname(pn:str):
    return pn.replace(" ", "_").replace("/","_").replace(".", "_")

def check_barcodes(part_nums:list=None)-> bool:
    bpath = "../data/images/barcodes/"
    if not os.path.exists(bpath):
        os.mkdir(bpath)
    bdir = [x.rstrip('.png') for x in os.listdir(bpath)]
    logger(2, "barcodes.check_barcodes: Checking...")
    log_count_i = 0
    if part_nums == None:
        fields, items = dataio.items.get_all()
        for item in items:
            logger(logl, "barcodes.check_barcodes: Checking" + item[0])
            if item[0] not in bdir:
                log_count_i += 1
                barcode_gen(item[0], item[1])
    else:
        logger(logl, "barcodes.check_barcodes: No list specified...processing from db.items table.")
        for item in part_nums:
            f, dbr = dataio.items.find(item)
            if item not in bdir:
                log_count_i += 1
                barcode_gen(item, dbr[1])
    logger(logl, "barcodes.check_barcodes: Created " + str(log_count_i) + " new barcodes.")

def barcode_gen(part_uuid:str, part_name:str=""):
    logger(logl, "barcodes.barcode_gen: Creating barcode for " + part_uuid)
    item = dataio.items.find(part_uuid=part_uuid)
    part_number = item["part_number"]
    part_name = item["part_name"]
    bpath = "../data/images/barcodes/" + fname(part_number) + ".png"
    ideal_length = 38.1
    mod_height = ideal_length * .2
    mod_width = ideal_length / _length(part_number)
    if mod_width < 0.08382:
        mod_width = 0.08382
    img_writer = writer.ImageWriter(format='png', mode = "RGB")
    ean = barcode.codex.Code128(code=part_number,writer=img_writer)
    opts ={
        'module_width':mod_width,
        'module_height':mod_height,
        "font_size":15,
        'text_distance':1
    }
    txt = part_number + "\n" + part_name
    ean = ean.render(opts, txt)
    ean.save(bpath)
    #filename = ean.save(bpath + part_num.replace(".", "-").replace("*", "-"), options = {'modul\e_width':mod_width, 'module_height':mod_height, 'text_distance':1})
    logger(logl,"barcodes.barcode_gen: Created new barcode file for: " + part_number)

def print_barcode(path1):
    logger(logl, "barcodes.print_barcode: Printing" + path1)
    part_number = dataio.items.find(part_uuid=path1)["part_number"]
    path = "../data/images/barcodes/" + fname(part_number) + ".png"

    if os.path.exists(path):
        pass
    else:
        barcode_gen(path1)
    os.system("sudo chown pi /dev/usb/lp0")
    im = Image.open(path)
    im = im.resize((696, 225))

    backend = 'linux_kernel'    # 'pyusb', 'linux_kernal', 'network'
    model = 'QL-800' # your printer model.
    printer = '/dev/usb/lp0'    # Get these values from the Windows usb driver filter.  Linux/Raspberry Pi uses '/dev/usb/lp0'.

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    instructions = convert(
            qlr=qlr,
            images=[im],    #  Takes a list of file names or PIL objects.
            label='62',
            rotate='0',    # 'Auto', '0', '90', '270'
            threshold=70.0,    # Black and white threshold in percent.
            dither=False,
            compress=False,
            red=True,    # Only True if using Red/Black 62 mm label tape.
            dpi_600=False,
            hq=True,    # False for low quality.
            cut=True
    )

    send(instructions=instructions,
         printer_identifier=printer,
         backend_identifier=backend,
         blocking=True
         )

def _length(part_num:str):
    return ((11 * len(part_num)) + 35)


if __name__ == "__main__":
    #barcode_gen("test")
    #print_barcode("../data/images/barcodes/test.png")
    #check_barcodes()
    pass