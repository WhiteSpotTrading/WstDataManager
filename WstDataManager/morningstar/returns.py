from WstDataManager.morningstar import Fund_Base
from lxml import html
import requests


class Returns(Fund_Base):

    def __init__(self, morningstar_id):
        self.page = requests.get('http://www.morningstar.se/Funds/Quicktake/History.aspx?perfid=' + morningstar_id)
        self.tree = html.fromstring(self.page.content)
        self.annual_returns = self.get_annual_returns()
        self.quarterly_returns = self.get_quarterly_returns()
        self.average_annual_return = self.get_average_annual_return()
        self.average_quarterly_return = self.get_average_quarterly_return()
        self.returns_data = self.make_returns_object()

    def get_annual_returns(self):
        table = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_AnnualReturnsTopListItem1_ctl04"]/table')

        table_dict_raw = {}
        for i in range(1, 6):
            table_dict_raw[i] = [table[0][i][0].text_content(), self.format_float(table[0][i][1].text_content())]

        table_dict = {}
        for idx, key in enumerate(table_dict_raw):
            try:
                table_dict[int(table_dict_raw[key][0])] = table_dict_raw[key][1]
            except ValueError:
                try:
                    table_dict[int(table_dict_raw[key + 1][0]) + 1] = table_dict_raw[key][1]
                except IndexError:
                    table_dict[int(table_dict_raw[key - 1][0]) - 1] = table_dict_raw[key][1]
        return table_dict

    def get_quarterly_returns(self):
        table = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_ctl01_ctl01_ctl04"]/table')
        quarterly_returns = {}

        for i in range(1, len(table[0])):
            q_list = [self.format_float(table[0][i][1].text_content()),
                      self.format_float(table[0][i][2].text_content()),
                      self.format_float(table[0][i][3].text_content()),
                      self.format_float(table[0][i][4].text_content())]

            q_list = self.format_quarterly_returns(q_list)
            row = {}
            for idx, item in enumerate(q_list):
                if item:
                    label = 'Q'+str(idx + 1)
                    row[label] = item
            quarterly_returns[table[0][i][0].text_content()] = row
        return quarterly_returns



    def get_average_annual_return(self):
        sum, count = self.sum_count_dict(self.annual_returns)
        return float(sum / count)

    def get_average_quarterly_return(self):
        sum = 0
        count = 0
        for key in self.quarterly_returns:
            part_sum, part_count = self.sum_count_dict(self.quarterly_returns[key])
            sum += part_sum
            count += part_count
        return float(sum / count)

    def make_returns_object(self):
        returns_object = {}
        returns_object['annual_returns'] = self.annual_returns
        returns_object['quarterly_returns'] = self.quarterly_returns
        returns_object['average_annual_return'] = self.average_annual_return
        returns_object['average_quarterly_return'] = self.average_quarterly_return
        return returns_object

    def sum_count_dict(self, dict):
        sum = 0
        count = 0
        for key in dict:
            sum += dict[key]
            count += 1
        return sum, count

    def format_quarterly_returns(self, q_list):
        formatted_list = []
        for item in q_list:
            try:
                formatted_item = float(item)
            except ValueError:
                formatted_item = None
            formatted_list.append(formatted_item)
        return formatted_list
