#!/usr/bin/python3
import dataio
import db_manager
import os
import html_builder as bob


def header()-> bob.body:
    result = bob.header()
    result.head().file_link("stylesheet", 'styles.css').file_link("ico", 'favicon.ico', "type='image/ico' sizes='32x32'").scripts("script.js").title().head()
    result = bob.body(str(result))
    result.body()
    result.div("pageHeader").text("1073 Inventory System", "h1")
    result.div("MainNav").nav([("Home", "/"), ("New Item", "/newitem/"), ("Check-Out", "/checkout/"),("Check In","/checkin/"), ("Verify Qty", "/verify/"), ("Admin","/admin/")]).div("MainNav").div("pageHeader")
    return result

class home:
    def home() -> bytes:
        result = header()
        result.div("stockSearch")
        result.form("stockSearchBar", "onKeyUp='table_search()'").input("text", parms='id="tableSearchBar" placeholder="Search for Parts.."').form("stockSearchBar", "onKeyUp='table_search()'")
        result.div("stockSearch")
        result.div('stockTable')
        stockTable = bob.table(spacing=result.spacing)
        fields,tab_data  = dataio.items.get_all()
        u_index = fields.index("part_uuid")
        num_index = fields.index("part_number")
        fields = [x.replace("_", " ").title() for x in fields]
        stockTable.table(parms="id = 'stockTableT'").head().row(fields, typ="th").head()
        stockTable.body()
        for data in tab_data:
            data = list(data)
            data[num_index] = "<a href='/item/?partUUID=" + data[u_index] + "'>" + data[num_index]
            stockTable.row(data, typ='td')
        stockTable.body().table(parms="id = 'stockTableT'")
        result.returnable += stockTable.__str__()
        result.div("stockTable")
        result.body()
        return str(result).encode()

    def new_item()-> bytes:
        result = header()
        result.div("newItem")
        result.text("Create New Item", "h1", "checkStat")
        result.form('newItemForm', parms="id='newItemForm'")
        for x in [x.name for x in db_manager.db().table["items"].columns]:
            if x == "part_uuid": continue
            elif x == "status": continue
            else:
                result.label(x, x.replace("_", " ").title()).br().input('text',parms="id='"+ x +"'").br()
        result.button("button","Save Part", parms="onclick=newItem()").br()
        result.form('newItemForm', parms="id='newItemForm'").div("newItem").br()
        return str(result).encode()

    def checkout()-> bytes:
        result = header()
        result.div('checkOut').text("Check OUT", "h1", "checkStat").form("checkOutForm", parms="id='checkOutForm'")
        result.label('CheckOutPartNumber', "Part Number").br().input("text", parms="id='CheckOutPartNumber'").br()
        result.label("CheckOutQty", "Quantity Removed").br().input("text", parms="id='CheckOutQty'").br()
        result.label("CheckOutNotes","Notes").br().input("text", parms="id='CheckOutNotes'").br()
        result.button("button", "Submit",parms=' onclick=CheckoutForm()')
        result.form("checkOutForm", parms="id='checkOutForm'").div("checkOut")
        return str(result).encode()

    def checkin()-> bytes:
        result = header()
        result.div('checkIn').text("Check IN", "h1", "checkStat").form("checkInForm", parms="id='checkInID'")
        result.label('CheckInPartNumber', "Part Number").br().input("text", parms="id='CheckInPartNumber'").br()
        result.label("CheckInQty", "Quantity").br().input("text", parms="id='CheckInQty'").br()
        result.label("CheckInNotes","Notes").br().input("text", parms="id='CheckInNotes'").br()
        result.button("button", "Submit",parms=' onclick=CheckInForm()')
        result.form("checkInForm", parms="id='checkInID'").div("checkIn")
        return str(result).encode()
    
    def verify()-> str:
        result = header()
        result.div('verify').text("Verify Qty", "h1", "checkStat")
        result.form("verifyForm", parms=" id='verifyFormID'")
        result.br().label("VerificationPartNumber", "Part Number").br().input("text", parms="id='VerificationPartNumber'").br()
        result.label("VerificationPartQty", "Qty").br().input("text", parms="id='VerificationPartQty'").br()
        result.button("button", "Save", "onclick=VerifyForm()").form("verifyForm", parms=" id='verifyFormID'")
        result.div("verify").body()
        return str(result).encode()


class item:
    def item_home(args)->bytes:
        args = {args.split("=")[0]:args.split("=")[1]}
        result = header()
        item = dataio.items.find(part_uuid = args['partUUID'])
        result.div("itemButtons").\
            button("button", "Print Barcode", "onclick=printBarcode()").\
            button("button", "Edit Item", "onclick=editPartForm() id='editButton'").\
            div("itemButtons")
        result.div("partSpecs")
        partSpecs = bob.table( spacing = result.spacing)
        partSpecs.table().body()
        for field in item.keys():
            partSpecs.row([field.replace("_", " ").title(), item[field]], "td", True)
        partSpecs.body()
        partSpecs.table()
        result.returnable += str(partSpecs)
        result.div("partSpecs")
        result.body()
        return str(result).encode()

class admin:    
    def _admin_base()-> bob.body:
        result = header()
        result.div("adminNav")
        result.nav([("Import Parts", "/admin/import/"), ("Users", "/admin/users/")])
        result.div("itemNav")
        return result

    def admin()-> bytes:
        result = admin._admin_base()
        result.div("baseOps")
        result.button("button", "Full Backup", "id='adminBackup' onclick=adminBackupfunc()")
        result.div("baseOps").body()
        return str(result).encode()

    def admin_import()-> bytes:
        result = admin._admin_base()
        result.div("importParts")
        result.form("importForm")
        result.label('importfile', "Choose File").br().input("file", parms="id='importFile' name='filename'").br()
        result.input("submit", parms="value='Submit'")
        result.form("importForm")
        result.div("importParts")
        result.body()
        return str(result).encode()
    def users()->bytes:
        result = admin._admin_base()
        result.div("users")
        utable = bob.table(spacing=result.spacing)
        utable.table()
        fields, data = dataio.users.get_all()
        utable.head().row(fields, "th")
        utable.head().body()
        for d in data:
            utable.row(d, "td")
        utable.body().table()
        result.returnable += utable.returnable
        result.spacing = utable.spacing
        result.div("users")
        result.body()
        return str(result).encode()

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

if __name__ == "__main__":
    pass