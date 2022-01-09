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
\t\t\t\t<li><a href="/newitem/">New Item</a></li>
\t\t\t\t<li><a href="/checkout/">Check Out</a></li>
\t\t\t\t<li><a href="/backup/">Backup</a></li>
\t\t\t\t<li><a href="/barcodes/">Barcodes</a></li>
\t\t\t\t<li><a href="/admin/">Admin</a></li>
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
        results += spacing + """<input type="text" id="tableSearchBar" onkeyup="table_search()" placeholder="Search for Parts..">\n"""
    results += spacing + "<table id='stockTable'>\n"
    items, fields = dataio.parts.get_all_items()
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
    result += """\t\t<br>
    \t\t<dev class='checkout'>
    \t\t\tPart Number:<input type='text' id='part_number'>
    \t\t\tQuantity Removed:<input type='number' id='qty'>
    \t\t\tDestination:<input type='text' id='dest'>
    \t\t\tSource:<input type='text' id='source'>
    \t\t\t<button type=button onclick='checkout()'>Submit</button>
    \t\t\t</table>
    \t\t</dev>
    \t\t<dev id='checkoutHistory'>
    \t\t</dev>
    \t</body>\n"""
    return result.encode()

def barcodes_page():
    result = _init
    result += """\t<input type='button' value='print' onclick="printDiv('bcodesTable')"/>\n"""
    result += """\t<dev class="bcodesTable">
    \t\t<table>\n"""
    bcodes = os.listdir("../data/images/barcodes/")
    cols = 4
    rows = int(len(bcodes)/cols)
    if rows < 1: rows=1
    i = 0
    for r in range(0, rows):
        result += "\t\t\t<tr>\n"
        for c in range(0, cols):
            if i >= len(bcodes):
                result += "\t\t\t\t<td><img src='../data/images/barcodes/blank.png'></td>\n"
            else:
                print(bcodes[i])    
                result += "\t\t\t\t<td><img src='../data/images/barcodes/" + bcodes[i] + "'></td>\n"
                i += 1
        result += "\t\t\t</tr>\n"
    result += "\t\t</table>\n"
    result += """\t\t</dev>
    \t</form>
    </body>"""
    return result.encode()

def transactions_table(data:list[list]=None):
    results = """<div class='tranactionTable'>
    \t<table>
    \t\t<tr>
    """
    fields:list[str] = [x.split(" ")[0] for x in db_manager.tables["transactions"]]
    for field in fields:
        field = field.replace("_", " ").title()
        results += "\t\t\t<th>" + field +"</th>\n"
    results += "\t\t</tr>\n"
    if data != None:
        for dat in data:
            print(dat)
            results += "\t\t<tr>\n"
            for d in dat:
                results += "\t\t\t<td>" + str(d) + "</td>\n"
            results += "\t\t</tr>\n"
    results += """\t</table>
    </dev>
    """
    print(results)
    return results.encode()

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

def verify()-> str:
    result = _init
    result += """\t\t<br>\n
    \t\t<dev class='verify'>\n
    \t\t\t<form action='" + path + "' onsubmit='checkout()' id='checkout_form'>\n
    \t\t\t\tQuantity: <input type='number' name='change_qty'>\n
    \t\t\t\t<input type='submit' value='Submit'>
    \t\t\t</table>\n
    \t\t</dev>\n
    \t</body>\n"""
    return result.encode()

def admin():
    result = _init
    result += """\t\t<dev class='adminHeader'>
    \t\t\t<ul class='adminNavBar'>
    \t\t\t\t<li><a href='/admin/locations/'>Locations</a></li>
    \t\t\t\t<li><a href='/admin/items/'>Items Management</a></li>
    \t\t\t</ul>
    \t\t</dev>
    \t</body>
    """
    return result.encode()

def admin_locations():
    result = admin().decode("utf-8")
    result += """\t\t<dev class='adminLocations'>
    \t\t\t<table>
    \t\t\t\t<thead>
    \t\t\t\t\t<tr>
    """      
    fields, sqlres = dataio.locations.getAll()
    
    for field in fields:
        result += "\t\t\t\t\t<th>" + field.replace("_", " ").title() + "</th>\n"
    result += """\t\t\t\t\t<th>Options</th>
    \t\t\t\t</thead>
    \t\t\t\t</tr>
    """
    
    for res in sqlres:
        result += "\t\t\t\t\t<form class='locData'>\n"
        for f in range(fields):
            result += "\t\t\t\t\t\t<td>" + res + "</td>\n"
        result += "\t\t\t\t\t\t<td><input type='submit' value='Save'>\n"
        result += "\t\t\t\t\t</form>\n"
    result += """\t\t\t\t</tr>
    \t\t\t</table>
    \t\t</dev>
    """    
    return result.encode()
if __name__ == "__main__":
    pass