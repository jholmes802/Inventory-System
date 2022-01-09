import dataio
import db_manager
import urllib.parse as u_parse
import os

_head = """
<!DOCTYPE html>
<html land="en">\n
\t<head>\n
\t\t<link rel="stylesheet" href="style.css">\n
\t\t<link rel="icon" type="image/ico" sizes="32x32" href="/favicon.ico">\n
\t\t<script src="script.js"></script>\n
\t\t<title>1073 Inv System</title>\n
\t</head>\n"""

_end = """
</html>\n
        """

_header = """\t\t<div class ="header">\n
\t\t\t<h1>1073 Inventory System</h1>
\t\t\t<ul class="NavBar">
\t\t\t\t<li><a href="/">Home</a></li>
\t\t\t\t<li><a href="/newitem">New Item</a></li>
\t\t\t\t<li><a href="/checkout">Check Out</a></li>
\t\t\t\t<li><a href="/backup/">Backup</a></li>
\t\t\t\t<li><a href="/barcodes/">Barcodes</a></li>
\t\t\t</ul>
\t\t</div>\n"""

def _item_nav(part_num):
    result = "\t\t<div class ='header'>\n"
    result += "\t\t\t<ul class='ItemNavBar'>\n"
    result += "\t\t\t\t<li><a href='/item/" + part_num + "'>Item Home</a></li>\n"
    result += "\t\t\t\t<li><a href='/item/" + part_num + "/delete'>Delete Part</a></li>\n"
    result += "\t\t\t\t<li><a href='/item/" + part_num + "/edit'>Edit Part</a></li>\n"
    result += "\t\t\t\t<li><a href='/item/" + part_num + "/verify'>Verify Qty</a></li>\n"
    result += '\t\t\t</ul>\n'
    result += "\t\t</div>\n"
    return result 

_init = _head + "\t<body>\n" + _header

def home():
    results = _init
    results += "\t\t<div class='stock'>\n"
    results += "\t\t\t<p>Current Stock Table</p>\n"
    results += _tableBuilder("\t\t\t", True)
    results += "\t\t</div>\n"
    results += "\t</body>\n"
    results += _end
    return results.encode()

def new_item(data:bytes):
    results = _init
    #Form Data Processing.
    if data != None:
        data = u_parse.unquote(data)
        data = data.replace("+", " ")
        data = data.split('&')
        data = [x.split("=")[1] for x in data]
        data = [x if x!="" else None for x in data]
        print(data)
        try:
            dataio.new_item(data[0], data[1], data[2], data[3], data[4], None,data[5], check=True)
            print("console: created new item", new_item)
        except dataio.ItemError:
            results += "\t\t<div class='itemError'>\n"
            results += "\t\t\t<p>Uhoh Item already exsits.</p>"
            results += "\t\t\t<table>"
            results += "\t\t</div>"    
        
    else:
        pass
    results += "\t\t<div class='newItem'>\n"
    results += "\t\t\t<p>Create New Item</p>"
    results += '\t\t\t<form action="/newitem/">\n'
    for field in db_manager.columns['items']:
        if field == "verified_date":
            continue
        results += "\t\t\t\t<label for='"+ field +"'>" + field.replace("_", " ").title() + ":</label><br>"
        results += "\t\t\t\t<input type='text' id='"+ field +"' name='"+ field +"'><br>"
    results += "\t\t\t\t<input type='submit' value='Submit'>"
    results += "\t\t\t</form>\n"
    return results.encode()

def _tableBuilder(spacing:str, search: bool = False)-> str:
    results = ''
    if search:
        results += spacing + """<input type="text" id="tableSearchBar" onkeyup="table_search()" placeholder="Search for Parts..">"""
    results += spacing + "<table id='stockTable'>\n"
    items, fields = dataio.get_all_items()
    results += spacing + "\t<tr class='stockTableHeader'>\n"
    for i, f in enumerate(fields):
        if f == "part_number": part_number_i = i
        results += spacing + "\t\t<th>"+ f.replace("_", " ").title() + "</th>\n"
    results += spacing + "\t</tr>\n"
    for item in items:
        results += spacing + "\t<tr>\n"
        for i, ifield in enumerate(item):
            if ifield == None:
                ifield = ""
            if i == part_number_i:
                results += spacing + "\t\t<td><a href='/item/" + ifield + "/'>" + str(ifield) + "</td>\n"
            else:
                results += spacing + "\t\t<td>" + str(ifield) + "</td>\n"
        results += spacing + "\t<tr>\n"
    results += spacing + "</table>\n"
    return results

def item(prt_num:str)->str:
    fields, item = dataio.find(prt_num)
    fields = [x.replace("_", " ").title() for x in fields]
    result = _init + _item_nav(prt_num)
    result += "\t\t<br>\n"
    result += "\t\t<table class='itempage'>\n"
    for i, field in enumerate(fields):
        result += "\t\t\t<tr>\n"
        if "Link" in field:
            result += "\t\t\t\t<th>" + field + "</th>\n"
            result += "\t\t\t\t<td><a href='" + item[i] + "'>" + item[i] + "</a></td>\n" 
        else:
            result += "\t\t\t\t<th>" + field + "</th>\n"
            result += "\t\t\t\t<td>" + str(item[i]) + "</td>\n"
        result += "\t\t\t</tr>\n"
    result += "\t\t</table>\n"
    result += "\t</body>\n"
    return result.encode()

def checkout_x(data)-> str:
    try:
        data = [x.split("=")[1] for x in u_parse.unquote(data).lstrip("?").split("&")]
        dataio.checkout(data)
    except:
        pass
    result = _init
    result += "\t\t<br>\n"
    result += "\t\t<dev class='checkout'>\n"
    result += "\t\t\t<form action='/checkout/' onsubmit='checkout()' id='checkout_form'>\n"
    result += "\t\t\t\tPart Number: <input type='text' name='part_number'>\n"
    result += "\t\t\t\tRemoved Qty: <input type='number' name='change_qty'>\n"
    result += "\t\t\t\t<input type='submit' value='Submit'>"
    result += "\t\t\t</table>\n"
    result += "\t\t</dev>\n"
    result += "\t</body>\n"
    return result.encode()

def checkout()-> str:
    
    result = _init
    result += "\t\t<br>\n"
    result += "\t\t<dev class='checkout'>\n"
    result += "\t\t\tPart Number:<input type='text' id='part_number'>\n"
    result += "\t\t\tQuantity Removed:<input type='number' id='qty'>\n"
    result += "\t\t\t<button type=button onclick='checkout()'>Submit</button>\n"
    result += "\t\t\t</table>\n"
    result += "\t\t</dev>\n"
    result += "\t</body>\n"
    return result.encode()

def barcodes_page():
    result = _init
    result += """\t<dev class="bcodes">
    \t\t<dev class="bcodesTable">
    \t\t\t<table style='>\n"""
    bcodes = os.listdir("../data/images/barcodes/")
    cols = 4
    coli = 1
    for bcode in bcodes:
        if coli >= cols:
            result += "\t\t\t\t</tr>\n"
            coli = 0
        elif coli == 0:
            result += "\t\t\t\t<tr>\n"
            coli += 1
        else:
            coli += 1
            result += "\t\t\t\t\t<td><img src='../data/images/barcodes/" + bcode + "'></td>\n"
    result += "\t\t\t</table>\n"
    result += """\t\t</dev>
    \t</dev>
    </body>"""
    return result.encode()

def delete_part(prt_num:str,choices:list):
    if choices != None:
        tf = []
        for c in choices:
            tf.append(c == 'yes')
        if tf[0]:
            dataio.delete_part(prt_num,tf[1])
            return (_init + "\t\t<script> alert('Part Has Been Deleted')</script>\n" + """\t\t<meta http-equiv='refresh' content="0; url='/'"/>\n""").encode()
        else:
            return  (_init + "\t\t<script> alert('Part Has Not Been Deleted')</script>\n" + """\t\t<meta http-equiv='refresh' content="0; url='/'"/>\n""").encode()
    else:
        fields, item = dataio.find(prt_num)
        fields = [x.replace("_", " ").title() for x in fields]
        result = _init + _item_nav(prt_num)
        result += "\t\t<br>\n"
        result += "\t\t<h1>Are you Sure you would like to delete this part?</h1>\n"
        result += "\t\t<form action='/item/" + prt_num + "/delete' onsubmit='checkout()'>\n"
        result += "\t\t<input type='radio' name=yes_no value='yes' checked>Yes</input>\n"
        result += "\t\t<input type='radio' name=yes_no value='no' checked>No</input>\n"
        result += "\t\t<p>Do you want to remove all transactions with this part number?</p>\n"
        result += "\t\t<input type='radio' name=transactions_yn value='yes' checked>Yes</input>\n"
        result += "\t\t<input type='radio' name=transactions_yn value='no' checked>No</input>\n"
        result += "\t\t<input type='submit' value='Submit'>"
        result += "\t\t</form>"
        result += "\t\t<table class='itempage'>\n"
        for i, field in enumerate(fields):
            result += "\t\t\t<tr>\n"
            if "Link" in field:
                result += "\t\t\t\t<th>" + field + "</th>\n"
                result += "\t\t\t\t<td><a href='" + item[i] + "'>" + item[i] + "</a></td>\n" 
            else:
                result += "\t\t\t\t<th>" + field + "</th>\n"
                result += "\t\t\t\t<td>" + str(item[i]) + "</td>\n"
            result += "\t\t\t</tr>\n"
        result += "\t\t</table>\n"
        result += "\t</body>\n"
        return result.encode()

def backup():
    if dataio.backup():
        return  (_init + "\t\t<script> alert('Server Side Backup Created!')</script>\n" + """\t\t<meta http-equiv='refresh' content="0; url='/'"/>\n""").encode()

def verify(qty, path)-> str:
    part_num = path.split("/")[2]
    result = _init
    try:
        data = u_parse.unquote(qty).lstrip("?").split("=")[1]
        dataio.verify([part_num,data])
        result += """\t\t<meta http-equiv='refresh' content="0; url='/'"/>\n"""
        return result.encode()
    except: pass
    result = _init
    result += "\t\t<br>\n"
    result += "\t\t<dev class='verify'>\n"
    result += "\t\t<p>" + part_num + "</p>\n"
    result += "\t\t\t<form action='" + path + "' onsubmit='checkout()' id='checkout_form'>\n"
    result += "\t\t\t\tQuantity: <input type='number' name='change_qty'>\n"
    result += "\t\t\t\t<input type='submit' value='Submit'>"
    result += "\t\t\t</table>\n"
    result += "\t\t</dev>\n"
    result += "\t</body>\n"
    return result.encode()

def admin():
    result = _init
    pass

if __name__ == "__main__":
    pass