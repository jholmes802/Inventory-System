import re

string1 = "/item/217-6515/"
string2 = string1 + "edit"

test = re.search("^/item/.*/$", string1)
print(test == True)
test = re.search("^/item/.*/$", string2)
print(test)