import requests


class scrape():
    def __init__(self, url) -> None:
        self.url = url
        self.text = requests.get(self.url).text.split("\n")
    def parse_body(self):
            for line in self.text:
                if line:
                    print(line)


a = scrape("https://www.vexrobotics.com/pro/all?q=")
a.parse_body()