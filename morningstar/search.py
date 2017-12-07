from morningstar.fund import Fund
from lxml import html
import requests

class Search(Fund):

    def __init__(self, search_string=None, fivestar_only=None):
        self.url = 'http://www.morningstar.se/Funds/Quickrank.aspx?'
        if search_string:
            self.url = self.url + 'search=' + search_string + '&'
        if fivestar_only:
            self.url = self.url + 'fiverating=on&rtng=5'
        self.page = requests.get(self.url)
        self.tree = html.fromstring(self.page.content)
        self.results = self.get_results()
        self.funds_data = {}

    def get_results(self):
        table = self.tree.xpath('//*[@id="ctl01_cphContent_Quickrank1_ctl00"]/tbody')
        results = {}
        for i in range(0, len(table[0])):
            fund_name = table[0][i][2][0].text_content().strip()
            morningstar_id = table[0][i][2][0].values()[0].split('?')[1].split('&')[0].split('=')[1].strip()
            results[i] = {'fund_name':fund_name, 'morningstar_id':morningstar_id}
        return results

    def get_funds_data(self):
        funds_data = {}
        for key in self.results:
            funds_data[key] = Fund(self.results[key]['morningstar_id'])
        self.funds_data = funds_data
        return self


