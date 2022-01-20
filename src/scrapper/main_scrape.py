import requests


class scrape():
    def __init__(self, url) -> None:
        self.url = url
        self.text:list = [x for x in requests.get(self.url).text]
    def parse_body(self):
            for line in self.text:
                if line.

a = scrape("https://www.vexrobotics.com/pro/all?q=")
a.parse_body()