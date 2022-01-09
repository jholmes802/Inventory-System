import dataio

_head = """
<html land="en">\r
\t<head>\r
\t\t<link rel="stylesheet" href="style.css">\r
\t\t<link rel="icon" type="image/ico" sizes="32x32" href="/favicon.ico">\r
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
\t\t\t</ul>
\t\t</div>\r"""
def home():
    results = "" + _head
    results += "\t<body>\r"
    results += _header
    results += "\t\t<div class='stock'>\r"
    results += "\t\t\t<p>Current Stock Table</p>\r"
    results += _tableBuilder("\t\t\t")
    results += "\t\t</div>\r"
    results += "\t</body>\r"
    results += _end
    return results.encode()

def new_item(data:str):
    results = "" + _head
    results += "\t<body>\r"
    results += _header
    #Form Data Processing.
    if data != None:
        data = data.replace("+", " ")
        data = data.split('&')
        part_name = data[0].split("=")[1]
        part_num = data[1].split("=")[1]
        qty = data[2].split("=")[1]
        new_item = dataio.item(part_name, part_num, qty)
        try:
            dataio.DataIO.new_item('../data/items.csv', new_item, check=True)
        except dataio.FileError:
            pass
        except dataio.ItemError:
            results += "\t\t<div class='itemError'>\r"
            results += "\t\t\t<p>Uhoh Item already exsits.</p>"
            results += "\t\t\t<table>"
            results += "\t\t</div>"    
        print("console: created new item", new_item)
        
    else:
        pass
    results += "\t\t<div class='newItem'>\r"
    results += "\t\t\t<p>Create New Item</p>"
    results += '\t\t\t<form action="/newitem/">\r'
    results += "\t\t\t\t<label for='prtnum'>Part Number:</label><br>"
    results += "\t\t\t\t<input type='text' id='prtnum' name='prtnum'><br>"
    results += "\t\t\t\t<label for='prtname'>Part Name:</label><br>"
    results += "\t\t\t\t<input type='text' id='prtname' name='prtname'><br>"
    results += "\t\t\t\t<label for='qty'>Quantity:</label><br>"
    results += "\t\t\t\t<input type='text' id='qty' name='qty'><br>"
    results += "\t\t\t\t<input type='submit' value='Submit'>"
    results += "\t\t\t</form>\r"
    return results.encode()

def _tableBuilder(spacing:str, partNums:list=None)-> str:
    results = spacing + "<table class='stockTable'>\r"
    items = dataio.DataIO.extractall('../data/items.csv')
    results += spacing + "\t<tr>\n"
    results += spacing + "\t\t<th>Part Name</th>\r"
    results += spacing + "\t\t<th>Part Number</th>\r"
    results += spacing + "\t\t<th>Quantity</th>\r"
    results += spacing + "\t</tr>\r"
    if partNums == None:
        for item in items:
            results += spacing + "\t<tr>\n"
            results += spacing + "\t\t<td>" + item.name + "</td>\r"
            results += spacing + "\t\t<td>" + item.part_num + "</td>\r"
            results += spacing + "\t\t<td>" + item.qty + "</td>\r"
            results += spacing + "\t</tr>\r"
    elif type(partNums) == list:
        for item in items:
            if item.part_num in partNums:
                results += spacing + "\t<tr>\n"
                results += spacing + "\t\t<td>" + item.name + "</td>\r"
                results += spacing + "\t\t<td>" + item.part_num + "</td>\r"
                results += spacing + "\t\t<td>" + item.qty + "</td>\r"
                results += spacing + "\t</tr>\r"
    results += spacing + "</table>\r"
    return results
