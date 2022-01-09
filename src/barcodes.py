import dataio
import os
import barcode
import barcode.writer as writer
import datetime

global verbose
verbose = False

if "verbose.dat" in os.listdir(os.getcwd()):
    verbose = True
def now(): return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def check_barcodes(part_nums:list=None)-> bool:
    bpath = "../data/images/barcodes/"
    bdir = [x.rstrip('.png') for x in os.listdir(bpath)]
    if part_nums == None:
        items, fields = dataio.get_all_items()
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
    filename = ean.save(bpath + part_num, options = {'module_width':mod_width, 'module_height':mod_height, 'text_distance':1, "font_size":15})
    if verbose: print(now() + ": BARCODES: Created new barcode file for:", part_num)


def _length(part_num:str):
    return ((11 * len(part_num)) + 35)
if __name__ == "__main__":
    check_barcodes()
    barcode_gen("1073-1")