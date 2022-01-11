import re
import dataio
import db_manager
import urllib.parse as u_parse
import os
import html_builder as bob

class DataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def _base()-> bob.body:
    result = bob.header()
    result.head().file_link("stylesheet", 'styles.css').file_link("ico", 'favicon.ico', "type='image/ico' sizes='32x32'").scripts("script.js").title().head()
    result = bob.body(str(result))
    result.body()
    result.div("pageHeader").text("1073 Inventory System", "h1")
    result.div("MainNav").nav([("Home", "/"), ("New Item", "/newitem/"), ("Check-Out", "/checkout/"),("Check In","/checkin/"), ("Verify Qty", "/verify/"), ("Admin","/admin/")]).div("MainNav").div("pageHeader")
    return result

def home(): #Works good
    result = _base()
    result.div("stockSearch")
    result.form("stockSearchBar", "onKeyUp='table_search()'").input("text", parms='id="tableSearchBar" placeholder="Search for Parts.."').form("stockSearchBar", "onKeyUp='table_search()'")
    result.div("stockSearch")
    result.div('stockTable')
    stockTable = bob.table(spacing=result.spacing)
    tab_data, fields = dataio.parts.get_all_items()
    fields = [x.replace("_", " ").title() for x in fields]
    stockTable.table(parms="id = 'stockTableT'").head().row(fields, typ="th").head()
    stockTable.body()
    for data in tab_data:
        dat = []
        for i,d in enumerate(data):
            if i == 0:
                dat.append("<a href='/item/?partNumber=" + d + "'>" + d)
            elif d == None:
                dat.append("")
            else:
                dat.append(d)
        stockTable.row(dat, typ='td')
    stockTable.body().table(parms="id = 'stockTableT'")
    result.returnable += stockTable.__str__()
    result.div("stockTable")
    result.body()
    return str(result).encode()

def new_item(): #Needs Java Script implementation.
    result = _base()
    result.div("newItem")
    result.text("Create New Item", "h1", "checkStat")
    result.form('newItemForm', parms="id='newItemForm'")
    #result.br()
    result.label('NewPartNum', "Part Number").br().input('text',parms="id='NewPartNum'").br()
    result.label("NewPartName", "Part Name").br().input('text',parms="id='NewPartName'").br()
    result.label("NewPartQty", "Quantity").br().input("number",parms= "id='NewPartQty'").br()
    result.label("NewPartSource", "Source").br().input("tex", parms="id='NewPartSource'").br()
    result.label("NewPartLink", "Source Link").br().input("text", parms="id='NewPartLink'").br()
    result.button("button","Save Part", parms="onclick=newItem()").br()
    result.form('newItemForm', parms="id='newItemForm'").div("newItem").br()
    return str(result).encode()

def item(args:str)->str: #NEEDS implementation
    args = {args.split("=")[0]:args.split("=")[1]}
    result = _base()
    fields,item = dataio.parts.find(args['partNumber'])
    fields = [x.replace("_", " ").title() for x in fields]
    result.div("partSpecs")
    partSpecs = bob.table( spacing = result.spacing)
    partSpecs.table().body()
    for i, field in enumerate(fields):
        partSpecs.row([fields[i], item[i]], "td", True)
    partSpecs.body()
    partSpecs.table()
    result.returnable += str(partSpecs)
    result.body()
    return str(result).encode()

def checkout()-> str: #Needs JS implementation and python post side
    result = _base()
    result.div('checkOut').text("Check OUT", "h1", "checkStat").form("checkOutForm", parms="id='checkOutForm'")
    result.label('CheckOutPartNumber', "Part Number").br().input("text", parms="id='CheckOutPartNumber'").br()
    result.label("CheckOutQty", "Quantity Removed").br().input("text", parms="id='CheckOutQty'").br()
    result.label("CheckOutNotes","Notes").br().input("text", parms="id='CheckOutNotes'").br()
    result.button("button", "Submit",parms=' onclick=CheckoutForm()')
    result.form("checkOutForm", parms="id='checkOutForm'").div("checkOut")
    #result.div("checkOutHistory")
    #result.returnable += transactions_table(result)
    #result.div("checkOutHistory")
    return str(result).encode()

def checkin()-> str: #Needs JS implementation and python post side
    result = _base()
    result.div('checkIn').text("Check IN", "h1", "checkStat").form("checkInForm", parms="id='checkInID'")
    result.label('CheckInPartNumber', "Part Number").br().input("text", parms="id='CheckInPartNumber'").br()
    result.label("CheckInQty", "Quantity").br().input("text", parms="id='CheckInQty'").br()
    result.label("CheckInNotes","Notes").br().input("text", parms="id='CheckInNotes'").br()
    result.button("button", "Submit",parms=' onclick=CheckInForm()')
    result.form("checkInForm", parms="id='checkInID'").div("checkIn")
    #result.div("checkOutHistory")
    #result.returnable += transactions_table(result)
    #result.div("checkOutHistory")
    return str(result).encode()

def barcodes_page(): #Currently not being used, ideally will be later...
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

def transactions_table(cur:bob.body):
    histTable = bob.table(spacing = cur.spacing)
    histTable.table()
    histTable.head()
    histTable.row([x.split(" ")[0] for x in db_manager.tables["transactions"]], "th")
    histTable.head()
    histTable.body()
    records = dataio.transactions.get_transactions(cnt = 20)
    for record in records:
        histTable.row(record, 'td')
    histTable.body()
    histTable.table()
    return histTable.returnable

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
        return  (_base().returnable + "\t\t<script> alert('Server Side Backup Created!')</script>\n" + """\t\t<meta http-equiv='refresh' content="0; url='/'"/>\n""").encode()

def verify()-> str:
    result = _base()
    result.div('verify').text("Verify Qty", "h1", "checkStat")
    result.form("verifyForm", parms=" id='verifyFormID'")
    result.br().label("VerificationPartNumber", "Part Number").br().input("text", parms="id='VerificationPartNumber'").br()
    result.label("VerificationPartQty", "Qty").br().input("text", parms="id='VerificationPartQty'").br()
    result.button("button", "Save", "onclick=VerifyForm()").form("verifyForm", parms=" id='verifyFormID'")
    result.div("verify").body()
    return str(result).encode()

def _admin_base():
    result = _base()
    result.div("adminNav")
    result.nav([("Import Parts", "/admin/import/"), ("Barcodes", "/admin/barcodes/")])
    result.div("itemNav")
    return result

def admin():
    result = _admin_base().body()
    return str(result).encode()

def admin_barcodes():
    result = _admin_base()
    result.div("bcodeOPTS")
    result.button("button", "Print Barcodes", "id ='printBCodes' onclick=printDiv('bcodesPrintable')").br()
    result.div("bcodeOPTS")
    result.div("bcodesPrintable")
    printable = bob.table(spacing=result.spacing)
    printable.table().body()
    bcodes_list = os.listdir("../data/images/barcodes/")
    i = 0
    while i <= len(bcodes_list):
        if (len(bcodes_list) - i) < 6:
            pass
        else:
            data = []
            for ri in range(0,6):
                data.append("<img src='../data/images/barcodes/" + bcodes_list[i] + "'></img>")
                i += 1
            printable.row(data, 'td')
    printable.body().table()
    result.returnable += printable.returnable
    result.div("bcodesPrintable")
    result.body()
    return str(result).encode()

def admin_import():
    result = _admin_base()
    result.div("importParts")
    result.form("importForm")
    result.label('importfile', "Choose File").br().input("file", parms="id='importFile' name='filename'").br()
    result.input("submit", parms="value='Submit'")
    result.form("importForm")
    result.div("importParts")
    result.body()
    return str(result).encode()

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