class header:
    def __init__(self) -> None:
        """ Creates the headers for the html doc runs these commands.
        head, file_linking, scripts, title, head

        Args:
            file_list (list[tuple]): A list of tuples formated as such (href, rel)
            script_path (str): path to .js file.
        """
        self.returnable = "<!DOCTYPE html>\n<html lang='en'>\n"
    def head(self):
        """MUST BE CALLED AT THE BEGINNING AND END OF THE HEADERS SECTION
        """
        if "<head>" in self.returnable:
            self.returnable += "</head>\n"
        else:
            self.returnable += "<head>\n"
        return self
    def file_link(self, rel, href_link, parms=""):
        """Creates the links in the header. Called once per item.


        Args:
            file_list (list[tuple]): A list of tuples formated as such (href, rel)
        """
        self.returnable += "\t<link rel='"+ rel + "' href='" + href_link + "'" + parms + ">\n"
        return self
    def scripts(self,path):
        self.returnable += "\t<script scr='" + path + "'></script>\n"
        return self
    def title(self):
        self.returnable += "\t<title> 1073 Inventory System</title>\n"
        return self
    def __str__(self) -> str:
        return str(self.returnable)

class body:   
    def __init__(self, heading="") -> None:
        self.spacing = 0
        self.returnable = heading
    def div(self, className):
        if "<div class='" + className + "'>" in self.returnable:
            self.spacing -= 1
            self.returnable += (self.spacing * "\t") + "</div>\n"
        else:
            self.returnable += (self.spacing * "\t") + "<div class='" + className + "'>\n"
            self.spacing += 1
        return self
    def body(self):
        if "<body>" in self.returnable:
            self.returnable += "</body>\n"
            self.spacing -= 1
        else:
            self.returnable += "<body>\n"
            self.spacing += 1
        return self
    def nav(self, items:list[tuple]):
        """Creates the navigation section. Only needs to be called once.

        Args:
            spacing ([type]): Dictates the spacing needed.
            items (list[tuple]): A list of tuple formatted as (proper name, link)
        """
        self.returnable += str((self.spacing * "\t") + "<ul>\n")
        self.spacing += 1
        for i in items:
            self.returnable += str(((self.spacing) * "\t") + "<li><a href='" + i[1] + "'>" + i[0] + "</a></li>\n")
        self.spacing -= 1
        self.returnable += str((self.spacing * "\t") + "</ul>\n")
        return self
    def table(self, data:list[list or tuple], fields=True):
        """Being phased out for class table !!!!!!

        """
        self.returnable += (self.spacing * "\t") + "<table>\n"
        self.spacing += 1
        if type(fields) == bool:
            fields = data[0]
            data = data[1:]
        self.returnable += ((self.spacing) * "\t") + "<thead>\n"
        self.spacing += 1
        self.returnable += ((self.spacing) * "\t") + "<tr>\n"
        self.spacing += 1
        for field in fields:
            self.returnable += ((self.spacing) * "\t") + "<th>" + str(field) + "</th>\n"
        self.spacing -= 1
        self.returnable += ((self.spacing) * "\t") + "</tr>\n"
        self.spacing -= 1
        self.returnable += ((self.spacing) * "\t") + "</thead>\n"
        self.returnable += ((self.spacing ) * "\t") + "<tbody>\n"
        self.spacing += 1
        for dat in data:
            self.returnable += ((self.spacing) * "\t") + "<tr>\n"
            self.spacing += 1
            for d in dat:
                self.returnable += ((self.spacing) * "\t") + "<td>" + str(d) + "</td>\n"
            self.spacing -= 1
            self.returnable += ((self.spacing) * "\t") + "</tr>\n"
        self.spacing -= 1
        self.returnable += ((self.spacing) * "\t") + "</tbody>\n"
        self.spacing -= 1
        self.returnable += ((self.spacing) * "\t") + "</table>\n"
        return self
    def form(self, cls:str, parms):
        if "<form class='{cls}'>" in self.returnable:
            self.spacing -= 1
            self.returnable += (self.spacing * "\t") + "</form>\n"
        else:
            self.returnable += (self.spacing * "\t") + "<form class= '" + cls + "' " + parms + ">\n"
            self.spacing += 1
    def input(self, typ, text="", parms=""):
        self.returnable += (self.spacing * "\t") + "<input type='" + typ + "' " + parms + ">" + text + "</input\n"
    def text(self, msg, typ, id=''):
        if id == "":
            self.returnable += (self.spacing * "\t") + "<" + typ + ">" + msg + "</" + typ + ">\n"
        else:
            self.returnable += (self.spacing * "\t") + "<" + typ + "id='" + id + "'>" + msg + "</" + typ + ">\n" 
    def __str__(self) -> str:
        return str(self.returnable)

class table:
    def __init__(self, heading="", spacing =0) -> None:
        self.returnable = heading
        self.spacing = spacing
    def table(self):
        """Takes no arguments. Needs to be called once to itialize and again after data has been entered.
        """
        if ((self.spacing-1) * "\t") + "<table>\n" in self.returnable:
            self.spacing -= 1
            self.returnable += (self.spacing * "\t") + "</table>\n"
        else:
            self.returnable += (self.spacing * "\t") + "<table>\n"
            self.spacing += 1
    def head(self):
        """Takes no arguments. Needs to be called once to itialize and again after data has been entered.
        """
        if ((self.spacing-1) * "\t") + "<thead>\n" in self.returnable:
            self.spacing -= 1
            self.returnable += (self.spacing * "\t") + "</thead>\n"
        else:
            self.returnable += (self.spacing * "\t") + "<thead>\n"
            self.spacing += 1
    def body(self):
        """Takes no arguments. Needs to be called once to itialize and again after data has been entered.
        """
        if ((self.spacing-1) * "\t") + "<tbody>\n" in self.returnable:
            self.spacing -= 1
            self.returnable += (self.spacing * "\t") + "</tbody>\n"
        else:
            self.returnable += (self.spacing * "\t") + "<tbody>\n"
            self.spacing += 1
    def row(self, data, typ="", rotated=False):
        """Creates a row in the table.
        Should be called once for each row.

        --Args--
            - data: list - Must be a list of something that can be converted into a str.
            - typ: str - Either 'th' or 'td' for header or data.
            - rotated:bool - Rotates the table and makes the first entry in the data list the header for the table row.

        """
        if type(data) != list and type(data) != tuple:
            raise DataError("row(data, typ, rotated) data must be list type.")
        if typ not in ["th", "td"]:
            raise DataError("row(data, typ, rotated) typ must be either 'th' or 'td'")
        self.returnable += (self.spacing * "\t") + "<tr>\n"
        self.spacing += 1
        if typ == "":
            typ = "td"
        for d in data: 
            if rotated:
                self.returnable += (self.spacing * "\t") + "<th>" + str(d).strip() + "</th>\n"
                rotated = False    
            self.returnable += (self.spacing * "\t") + "<" + typ + ">" + str(d).strip() + "</" + typ + ">\n"
        self.spacing -= 1
        self.returnable += (self.spacing * "\t") + "</tr>\n"
    def __str__ (self):
        return str(self.returnable)        
