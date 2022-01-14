import dataio
import os
import barcode
import barcode.writer as writer
import datetime
from PIL import Image
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster


global verbose
verbose = False

if "verbose.dat" in os.listdir(os.getcwd()):
    verbose = True
def now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def check_barcodes(part_nums:list=None)-> bool:
    bpath = "../data/images/barcodes/"
    bdir = [x.rstrip('.png') for x in os.listdir(bpath)]
    if part_nums == None:
        items, fields = dataio.parts.get_all_items()
        for item in items:
            if item[0] not in bdir:
                barcode_gen(item[0])    
    else:
        for item in part_nums:
            if item not in bdir:
                barcode_gen(item)    

def barcode_gen(part_num:str):
    bpath = "../data/images/barcodes/"
    ideal_length = 38.1
    mod_height = ideal_length * .2
    mod_width = ideal_length / _length(part_num)
    if mod_width < 0.08382:
        mod_width = 0.08382
    img_writer = writer.ImageWriter(format='png', mode = "RGB")
    ean = barcode.get('code128', code=part_num,writer=img_writer)
    filename = ean.save(bpath + part_num.replace(".", "-").replace("*", "-"), options = {'module_width':mod_width, 'module_height':mod_height, 'text_distance':1, "font_size":15})
    if verbose: print(now() + ": BARCODES: Created new barcode file for:", part_num)

def print_barcode(path):
    im = Image.open(path)
    im = im.resize((306, 991)) 

    backend = 'pyusb'    # 'pyusb', 'linux_kernal', 'network'
    model = 'QL-800' # your printer model.
    printer = 'usb://0x04F9:0x209B'    # Get these values from the Windows usb driver filter.  Linux/Raspberry Pi uses '/dev/usb/lp0'.

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    instructions = convert(

            qlr=qlr, 
            images=[im],    #  Takes a list of file names or PIL objects.
            label='29x90', 
            rotate='auto',    # 'Auto', '0', '90', '270'
            threshold=70.0,    # Black and white threshold in percent.
            dither=False, 
            compress=False, 
            red=False,    # Only True if using Red/Black 62 mm label tape.
            dpi_600=False, 
            hq=True,    # False for low quality.
            cut=True

    )

    send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)

def _length(part_num:str):
    return ((11 * len(part_num)) + 35)
if __name__ == "__main__":
    print_barcode("../data/images/barcodes/WCP-0200.png")