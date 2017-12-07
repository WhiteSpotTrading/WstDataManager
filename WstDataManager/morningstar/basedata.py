from morningstar import Fund_Base
from lxml import html
import requests
from datetime import datetime


class BaseData(Fund_Base):

    def __init__(self, morningstar_id):
        self.morningstar_id = morningstar_id
        self.page = requests.get('http://www.morningstar.se/Funds/Quicktake/Overview.aspx?perfid='+morningstar_id)
        self.tree = html.fromstring(self.page.content)
        self.nav = self.get_nav()
        self.fund_basics = self.make_fund_object()

    def get_nav(self):
        table = self.tree.xpath('//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col333_OverviewGeneralItem1_ctl04"]/table')
        raw_str = table[0][0][1].text_content().replace(' ', '')
        currency = raw_str[-3:]
        raw_nav = raw_str[:-3]
        raw_nav_date = table[0][0][2].text_content()
        nav = self.format_float(raw_nav)
        nav_date = datetime.strptime(raw_nav_date, '%Y-%m-%d')
        return {'nav':nav, 'nav_date':nav_date, 'currency':currency}


    def make_fund_object(self):
        fund_name = self.tree.xpath('//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_FlowColumn4_FundNameHeaderItem1_ctl04"]/h2')
        cat = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col333_OverviewGeneralItem1_ctl04"]/div[2]/div[1]/span[2]/a')

        return {
            'morningstar_id':self.morningstar_id,
            'name': fund_name[0].text_content(),
            'morningstar_category': cat[0].text_content(),
            'nav': self.nav['nav'],
            'nav_date': self.nav['nav_date'],
            'currency': self.nav['currency']
        }





