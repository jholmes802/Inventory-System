import dataio
import db_manager
import urllib.parse as u_parse
import os
import html_builder as bob

class DataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

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

def home1():
    results = _init
    results += """\t\t<div class='stock'>
    \t\t\t<p>Current Stock Table</p>
    """
    results += _tableBuilder("\t\t\t", True)
    results += """\t\t</div>
    \t</body>"""
    results += _end
    return results.encode()

def home():
    result = header()
    result.head()
    result.file_link("stylesheet", './style.css')
    result.file_link("ico", './favicon.ico', "type='image/ico' sizes='32x32'" )
    result.title
    result.scripts("./script.js")
    result.head()
    result = body(str(result))
    result.body()
    result.div("pageHeader")
    result.text("1073 Inventory System", "h1")
    result.div("pageHeader")
    result.div("MainNav")
    result.nav([("Home", "/"), ("New Item", "/newitem/"), ("Check-Out", "/checkout/"), ("Backup", "/backup/")])
    result.div("MainNav")
    result.div("stockTable")
    tab_data, fields = dataio.parts.get_all_items()
    table1 = table(spacing=result.spacing)
    table1.table()
    table1.head()
    table1.row(fields, typ='th')
    table1.head()
    table1.body()
    for data in tab_data:
        table1.row(data, typ='td')
    table1.body()
    table1.table()
    result.returnable += table1.__str__()
    result.div("stockTable")
    result.body()
    return result.__str__().encode()

print(home().decode())
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
            dataio.parts.new_item(data[0], data[1], data[2], data[3], data[4], None,data[5], check=True)
            print("console: created new item", new_item)
        except dataio.ItemError:
            results += """\t\t<div class='itemError'>
            \t\t\t<p>Uhoh Item already exsits.</p>
            \t\t\t<table>
            \t\t</div>
            """    
        
    else:
        pass
    results += """\t\t<div class='newItem'>
    \t\t\t<p>Create New Item</p>
    \t\t\t<form action="/newitem/">
    """
    for field in db_manager.columns['items']:
        if field == "verified_date":
            continue
        results += "\t\t\t\t<label for='"+ field +"'>" + field.replace("_", " ").title() + ":</label><br>"
        results += "\t\t\t\t<input type='text' id='"+ field +"' name='"+ field +"'><br>"
    results += """\t\t\t\t<input type='submit' value='Submit'>
    \t\t\t</form>\n"""
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
    fields, item = dataio.parts.find(prt_num)
    fields = [x.replace("_", " ").title() for x in fields]
    result = _init + _item_nav(prt_num)
    result += """\t\t<br>
    \t\t<table class='itempage'>\n"""
    for i, field in enumerate(fields):
        result += "\t\t\t<tr>\n"
        if "Link" in field:
            result += "\t\t\t\t<th>" + field + "</th>\n"
            result += "\t\t\t\t<td><a href='" + item[i] + "'>" + item[i] + "</a></td>\n" 
        else:
            result += "\t\t\t\t<th>" + field + "</th>\n"
            result += "\t\t\t\t<td>" + str(item[i]) + "</td>\n"
        result += "\t\t\t</tr>\n"
    result += """\t\t</table>
    \t</body>\n"""
    return result.encode()

def checkout_x(data)-> str:
    try:
        data = [x.split("=")[1] for x in u_parse.unquote(data).lstrip("?").split("&")]
        dataio.transactions.checkout(data)
    except:
        pass
    result = _init
    result += """\t\t<br>
    \t\t<dev class='checkout'>
    \t\t\t<form action='/checkout/' onsubmit='checkout()' id='checkout_form'>
    \t\t\t\tPart Number: <input type='text' name='part_number'>
    \t\t\t\tRemoved Qty: <input type='number' name='change_qty'>
    \t\t\t\t<input type='submit' value='Submit'>
    \t\t\t</table>
    \t\t</dev>
    \t</body>
    """
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
    \t</body>
    """
    return result.encode()

def barcodes_page():
    result = _init
    result += """\t<input type='button' value='print' onclick="printDiv('bcodesTable')"/>
    \t<dev class="bcodesTable">
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
            dataio.parts.delete_part(prt_num,tf[1])
            return (_init + "\t\t<script> alert('Part Has Been Deleted')</script>\n" + """\t\t<meta http-equiv='refresh' content="0; url='/'"/>\n""").encode()
        else:
            return  (_init + "\t\t<script> alert('Part Has Not Been Deleted')</script>\n" + """\t\t<meta http-equiv='refresh' content="0; url='/'"/>\n""").encode()
    else:
        fields, item = dataio.parts.find(prt_num)
        fields = [x.replace("_", " ").title() for x in fields]
        result = _init + _item_nav(prt_num)
        result += """\t\t<br>\n
        \t\t<h1>Are you Sure you would like to delete this part?</h1>
        \t\t<form action='/item/""" + prt_num + """/delete' onsubmit='checkout()'>
        \t\t<input type='radio' name=yes_no value='yes' checked>Yes</input>
        \t\t<input type='radio' name=yes_no value='no' checked>No</input>
        \t\t<p>Do you want to remove all transactions with this part number?</p>
        \t\t<input type='radio' name=transactions_yn value='yes' checked>Yes</input>
        \t\t<input type='radio' name=transactions_yn value='no' checked>No</input>
        \t\t<input type='submit' value='Submit'>
        \t\t</form>
        \t\t<table class='itempage'>
        """
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
    if db_manager.backup():
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