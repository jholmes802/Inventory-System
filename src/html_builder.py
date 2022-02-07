#!/usr/bin/python3
from tools import *


class DataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

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
        self.returnable += '\t<script src="' + path + '"></script>\n'
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
    def form(self, cls:str, parms=""):
        if "<form class= '" + cls + "' " + parms + ">" in self.returnable:
            self.spacing -= 1
            self.returnable += (self.spacing * "\t") + "</form>\n"
        else:
            self.returnable += (self.spacing * "\t") + "<form class= '" + cls + "' " + parms + ">\n"
            self.spacing += 1
        return self
    def label (self, for1, msg):
        self.returnable += (self.spacing * "\t") + "<label for='"+ for1 +"'>" + msg + "</label>\n"
        return self
    def input(self, typ, text="", parms=""):
        self.returnable += ((self.spacing * "\t") + text +"<input type='" + typ + "' " + parms + ">\n")
        return self
    def br(self):
        self.returnable += ((self.spacing * "\t") + "<br>\n")
        return self
    def button(self, typ, text, parms=""):
        self.returnable += ((self.spacing * "\t") + "<button type='" + typ +  "'" + parms + ">" + text + "</button>\n")
        return self
    def text(self, msg, typ, id=''):
        if id == "":
            self.returnable += (self.spacing * "\t") + "<" + typ + ">" + msg + "</" + typ + ">\n"
        else:
            self.returnable += (self.spacing * "\t") + "<" + typ + " id='" + id + "'>" + msg + "</" + typ + ">\n" 
        return self
    def img(self, src):
        self.returnable += str((self.spacing * "\t") + "<img src=" + src + ">\n")
        return self
    def a(self, href, parms=""):
        self.returnable += str((self.spacing * "\t") + "<a href='" + href + "' " + parms + "></a>\n")
        return self
    def __str__(self) -> str:
        return str(self.returnable)

class table:
    def __init__(self, heading="", spacing =0) -> None:
        self.spacing = spacing            
        self.returnable = heading
    def table(self, parms=""):
        """Takes no arguments. Needs to be called once to itialize and again after data has been entered.
        """
        if ((self.spacing-1) * "\t") + "<table " + parms + ">\n" in self.returnable:
            self.spacing -= 1
            self.returnable += (self.spacing * "\t") + "</table>\n"
        else:
            self.returnable += (self.spacing * "\t") + "<table " + parms + ">\n"
            self.spacing += 1
        return self
    def head(self):
        """Takes no arguments. Needs to be called once to itialize and again after data has been entered.
        """
        if ((self.spacing-1) * "\t") + "<thead>\n" in self.returnable:
            self.spacing -= 1
            self.returnable += (self.spacing * "\t") + "</thead>\n"
        else:
            self.returnable += (self.spacing * "\t") + "<thead>\n"
            self.spacing += 1
        return self
    def body(self):
        """Takes no arguments. Needs to be called once to itialize and again after data has been entered.
        """
        if ((self.spacing-1) * "\t") + "<tbody>\n" in self.returnable:
            self.spacing -= 1
            self.returnable += (self.spacing * "\t") + "</tbody>\n"
        else:
            self.returnable += (self.spacing * "\t") + "<tbody>\n"
            self.spacing += 1
        return self
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
            else: 
                self.returnable += (self.spacing * "\t") + "<" + typ + ">" + str(d).strip() + "</" + typ + ">\n"
        self.spacing -= 1
        self.returnable += (self.spacing * "\t") + "</tr>\n"
        return self
    def __str__ (self):
        return str(self.returnable)        
