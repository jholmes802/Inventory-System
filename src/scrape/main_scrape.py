import requests
import re

class scrape():
    def __init__(self, url) -> None:
        self.url = url
        self.text = requests.get(self.url).text.split("\n")
    def parse_body(self):
            for line in self.text:
                if re.search("^<body", line) != None:
                    print(line)



a = scrape("https://www.vexrobotics.com/")
open("text.txt", "w").writelines(a.text)
a.parse_body()