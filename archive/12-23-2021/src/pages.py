import dataio

_head = """
<html land="en">\r
\t<head>\r
\t\t<link rel="stylesheet" href="style.css">\r
\t\t<link rel="icon" type="image/ico" sizes="32x32" href="/favicon.ico">\r
\t\t<script src="script.js"></script>\r
\t\t<title>1073 Inv System</title>\r
\t</head>\r"""

_end = """
</html>\n
        """

_header = """\t\t<div class ="header">\r
\t\t\t<h1>1073 Inventory System</h1>
\t\t\t<ul class="NavBar">
\t\t\t\t<li><a href="/">Home</a></li>
\t\t\t\t<li><a href="/newitem">New Item</a></li>
\t\t\t\t<li><a href="/checkout-in">Check Out/In</a></li>
\t\t\t</ul>
\t\t</div>\r"""

_init = _head + "\t<body>\r" + _header

def home():
    results = _init
    results += "\t\t<div class='stock'>\r"
    results += "\t\t\t<p>Current Stock Table</p>\r"
    results += _tableBuilder("\t\t\t")
    results += "\t\t</div>\r"
    results += "\t</body>\r"
    results += _end
    return results.encode()

def new_item(data:str):
    results = _init
    #Form Data Processing.
    if data != None:
        data = data.replace("+", " ")
        data = data.split('&')
        line = []
        for dat in data:
            line.append(dat.split("=")[1])
        new_item = dataio.item_gen(line)
        try:
            dataio.new_item(new_item, check=True)
            print("console: created new item", new_item)
        except dataio.FileError:
            pass
        except dataio.ItemError:
            results += "\t\t<div class='itemError'>\r"
            results += "\t\t\t<p>Uhoh Item already exsits.</p>"
            results += "\t\t\t<table>"
            results += "\t\t</div>"    
        
    else:
        pass
    results += "\t\t<div class='newItem'>\r"
    results += "\t\t\t<p>Create New Item</p>"
    results += '\t\t\t<form action="/newitem/">\r'
    for fi in dataio.fields:
        if fi.fieldname == "Verified Date":
            continue
        results += "\t\t\t\t<label for='"+ fi.name +"'>" + fi.fieldname + ":</label><br>"
        results += "\t\t\t\t<input type='text' id='"+ fi.name +"' name='"+ fi.name +"'><br>"
    results += "\t\t\t\t<input type='submit' value='Submit'>"
    results += "\t\t\t</form>\r"
    return results.encode()

def _tableBuilder(spacing:str, partNums:list=None)-> str:
    results = spacing + "<table class='stockTable'>\r"
    items = dataio.extractall()
    fields = dataio.fields
    results += spacing + "\t<tr>\n"
    for f in fields:
        results += spacing + "\t\t<th>"+ f.fieldname + "</th>\r"
    results += spacing + "\t</tr>\r"
    for item in items:
        print(item)
        results += spacing + "\t<tr>\r"
        for field in fields:
            if "Part Number" == field.fieldname:
                results += spacing + "\t\t<td><a href='/item/" + item[field.fieldname] + "'>" + item[field.fieldname] + "</a></td>\r"
            elif "Link" in field.fieldname:
                results += spacing + "\t\t<td><a href='" + item[field.fieldname] + "'>" + item[field.fieldname] + "</a></td>\r"
            else:
                results += spacing + "\t\t<td>" + item[field.fieldname] + "</td>\r"
        results += spacing + "\t<tr>\r"
    results += spacing + "</table>\r"
    return results

def item(prt_num:str)->str:
    item = dataio.find(prt_num)
    result = _init
    result += "\t\t<br>\r"
    result += "\t\t<table class='itempage'>\r"
    for field in dataio.fields:
        result += "\t\t\t<tr>\r"
        if "Quantity" == field.fieldname:
            result += "\t\t\t\t<th>" + field.fieldname + "</th>\r"
            result += "\t\t\t\t<td>\r"
            result += "\t\t\t\t\t<form action='/item/" + item["Part Number"] + "/'>\r"
            result += "\t\t\t\t\t\t<input type='number' step='1' min='0' max='' name='quantity' value='" + item["Quantity"] + "' title='Qty' class='input-text qty text' size='4' pattern='' inputmode''><input type='submit' value='Submit'>\r"
            result += "\t\t\t\t\t</form>\r"
            result += "\t\t\t\t</td>"
        elif "Link" in field.fieldname:
            result += "\t\t\t\t<th>" + field.fieldname + "</th>\r"
            result += "\t\t\t\t<td><a href='" + item[field.fieldname] + "'>" + item[field.fieldname] + "</a></td>\r" 
        else:
            result += "\t\t\t\t<th>" + field.fieldname + "</th>\r"
            result += "\t\t\t\t<td>" + item[field.fieldname] + "</td>\r"
        result += "\t\t\t</tr>\r"
    result += "\t\t</table>\r"
    result += "\t</body>\r"
    return result.encode()

def checkout(prt_num:str)-> str:
    item = dataio.find(prt_num)
    result = _init
    result += "\t\t<br>\r"
    result += "\t\t<dev class='checkout'>\r"
    result += "\t\t\t<table>\r"
    result += "\t\t\t\t<tr>\r"
    result += "\t\t\t\t\t<th>"
    return result.encode()

def admin():
    pass