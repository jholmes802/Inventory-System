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
from logger import logger

global verbose
verbose = False

if "verbose.dat" in os.listdir(os.getcwd()):
    verbose = True
def now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def fname(pn:str):
    return pn.replace(" ", "_").replace("/","_").replace(".", "_")

def check_barcodes(part_nums:list=None)-> bool:
    bpath = "../data/images/barcodes/"
    if not os.path.exists(bpath):
        os.mkdir(bpath)
    bdir = [x.rstrip('.png') for x in os.listdir(bpath)]
    logger(2, "barcodes.check_barcodes: Checking...")
    if part_nums == None:
        items, fields = dataio.parts.get_all_items()
        for item in items:
            logger(2, "barcodes.check_barcodes: Checking" + item[0])
            if item[0] not in bdir:
                barcode_gen(item[0], item[1])    
    else:
        for item in part_nums:
            f, dbr = dataio.parts.find(item)
            if item not in bdir:
                barcode_gen(item, dbr[1])    
def barcode_gen(part_num:str, part_name:str):
    logger(2, "barcodes.barcode_gen: Creating barcode for " + part_num)
    bpath = "../data/images/barcodes/" + fname(part_num) + ".png"
    ideal_length = 38.1
    mod_height = ideal_length * .2
    mod_width = ideal_length / _length(part_num)
    if mod_width < 0.08382:
        mod_width = 0.08382
    img_writer = writer.ImageWriter(format='png', mode = "RGB")
    ean = barcode.codex.Code128(code=part_num,writer=img_writer)
    opts ={
        'module_width':mod_width,
        'module_height':mod_height,
        "font_size":15,
        'text_distance':1
    }
    txt = part_num + "\n" + part_name
    ean = ean.render(opts, txt)
    ean.save(bpath)
    #filename = ean.save(bpath + part_num.replace(".", "-").replace("*", "-"), options = {'modul\e_width':mod_width, 'module_height':mod_height, 'text_distance':1})
    if verbose: print(now() + ": BARCODES: Created new barcode file for:", part_num)

def print_barcode(path1):
    logger(2, "barcodes.print_barcode: Printing" + path1)
    if "/" in path1:
        pass
    else:
        path = "../data/images/barcodes/" + fname(path1) + ".png"

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
         blocking=True)

def _length(part_num:str):
    return ((11 * len(part_num)) + 35)


if __name__ == "__main__":
    #barcode_gen("test")
    #print_barcode("../data/images/barcodes/test.png")
    check_barcodes()
