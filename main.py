import requests, statistics
from bs4 import BeautifulSoup

class ProductNotFound(Exception):
    pass

class BlockedRequest(Exception):
    pass


class SearchSites:
    def __init__(self, item):
        self.item = item

    def search_olx(self):
        query = []

        for i in self.item:
            if i == ' ':
                query.append('+')
            else:
                query.append(str(i))

        site_olx = requests.get('https://www.olx.ba/pretraga?trazilica={}'.format(''.join(query)))

        if site_olx.status_code == 200:
            try:

                bs4_result = BeautifulSoup(site_olx.content, 'html.parser')
                result = bs4_result.find(id="rezultatipretrage")
                m = []

                for i in result.findAll(class_='datum'):
                    num = i.span.text.split('KM')
                    if str(num[0]).strip().isdigit():
                        m.append(int(num[0]))

                return round(statistics.mean(m))

            except statistics.StatisticsError:
                raise ProductNotFound("Product not found, have you typed it correctly?")
        else:
            raise BlockedRequest("One of the sites has blocked the request.")

if __name__ == '__main__':
    print(SearchSites("usb stick").search_olx())
    # this would search for an usb stick ^^
