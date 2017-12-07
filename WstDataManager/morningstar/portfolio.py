# This Python file uses the following encoding: utf-8
from . import Fund_Base
from lxml import html
import re
from datetime import datetime
import requests
import pprint



class EquityPortfolio(Fund_Base):

    def __init__(self, morningstar_id):
        self.page = requests.get('http://www.morningstar.se/Funds/Quicktake/Portfolio.aspx?perfid=' + morningstar_id)
        self.tree = html.fromstring(self.page.content)
        self.portfolio_report_date = self.get_portfolio_report_date()
        self.investment_style = self.get_investment_style()
        self.ratios = self.get_ratios()
        self.geographic_allocation = self.get_geographic_allocation()
        self.industri_allocation = self.get_industry_allocation()
        self.portfolio_data = self.make_portfolio_object()

    def get_portfolio_report_date(self):
        date_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyle_ctl05"]/text()[1]')
        try:
            date = datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', date_element[0]).group(), '%Y-%m-%d')
        except IndexError:
            date = None
        return date

    def get_investment_style(self):

        large_cap_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyle_ctl04"]/div/div[1]/span[2]/span[1]')
        mid_cap_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyle_ctl04"]/div/div[1]/span[3]/span[1]')
        small_cap_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyle_ctl04"]/div/div[1]/span[4]/span[1]')
        equity_positions_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyle_ctl04"]/div/div[3]/span[2]/span[1]')
        fixed_income_positions_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyle_ctl04"]/div/div[3]/span[3]/span[1]')

        large_cap = self.format_float(large_cap_element[0].text_content())
        mid_cap = self.format_float(mid_cap_element[0].text_content())
        small_cap = self.format_float(small_cap_element[0].text_content())
        equity_positions = self.format_float(equity_positions_element[0].text_content())
        fixed_income_positions = self.format_float(fixed_income_positions_element[0].text_content())

        return {
            'large_cap': large_cap,
            'mid_cap': mid_cap,
            'small_cap': small_cap,
            'equity_positions': equity_positions,
            'fixed_income_positions': fixed_income_positions
        }

    def get_ratios(self):
        price_book_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyle_ctl04"]/div/div[2]/span[2]/span[1]')
        price_earnings_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyle_ctl04"]/div/div[2]/span[3]/span[1]')
        price_cashflow_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyle_ctl04"]/div/div[2]/span[4]/span[1]')


        price_book = self.format_float(price_book_element[0].text_content())
        price_earnings = self.format_float(price_earnings_element[0].text_content())
        price_cashflow = self.format_float(price_cashflow_element[0].text_content())


        return {
            'price_book': price_book,
            'price_earnings': price_earnings,
            'price_cashflow': price_cashflow
        }

    def get_geographic_allocation(self):
        # FIXME HANDLE FIXED INCOME FUNDS
        table = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiWorldMap_ContentPlaceHolder2_Chart1"]/div[2]')

        geo_allocation_dict = {}
        try:
            len(table[0][0]) > 0
        except IndexError:
            for key in self.geo_translations():
                geo_allocation_dict[self.geo_translations()[key]] = 0.0
        else:
            for i in range(1,len(table[0][0])):
                raw_key = self.strip_swedish(table[0][0][i][0].text_content().strip())
                key = self.geo_translations()[raw_key]
                value = self.format_float(table[0][0][i][1].text_content())
                geo_allocation_dict[key] = value

        return geo_allocation_dict

    def get_industry_allocation(self):
        # FIXME HANDLE FIXED INCOME FUNDS
        table = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiWorldMap_ContentPlaceHolder2_Chart1"]/div[2]')

        industry_allocation_dict = {}
        top_cyclical_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[1]/span[2]/span[1]')
        cyclical_commodities_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[1]/span[3]/span[1]')
        cyclical_consumer_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[1]/span[4]/span[1]')
        cyclical_finance_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[1]/span[5]/span[1]')
        cyclical_real_estate_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[1]/span[6]/span[1]')

        top_dynamic_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[2]/span[1]/span[1]')
        dynamic_communication_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[2]/span[2]/span[1]')
        dynamic_energy_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[2]/span[3]/span[1]')
        dynamic_industrials_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[2]/span[4]/span[1]')
        dynamic_echnology_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[2]/span[5]/span[1]')

        top_stabile_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[3]/span[1]/span[1]')
        stabile_consumer_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[3]/span[2]/span[1]')
        stabile_healthcare_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[3]/span[3]/span[1]')
        stabile_public_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiSectorAllocation_ctl04"]/div/div[3]/span[4]/span[1]')

        top_cyclical = self.format_float(top_cyclical_element[0].text_content())
        cyclical_commodities = self.format_float(cyclical_commodities_element[0].text_content())
        cyclical_consumer = self.format_float(cyclical_consumer_element[0].text_content())
        cyclical_finance = self.format_float(cyclical_finance_element[0].text_content())
        cyclical_real_estate = self.format_float(cyclical_real_estate_element[0].text_content())
        top_dynamic = self.format_float(top_dynamic_element[0].text_content())
        dynamic_communication = self.format_float(dynamic_communication_element[0].text_content())
        dynamic_energy = self.format_float(dynamic_energy_element[0].text_content())
        dynamic_industrials = self.format_float(dynamic_industrials_element[0].text_content())
        dynamic_technology = self.format_float(dynamic_echnology_element[0].text_content())
        top_stabile = self.format_float(top_stabile_element[0].text_content())
        stabile_consumer = self.format_float(stabile_consumer_element[0].text_content())
        stabile_healthcare = self.format_float(stabile_healthcare_element[0].text_content())
        stabile_public = self.format_float(stabile_public_element[0].text_content())
        return {
            'cyclical':
                {
                    'total':top_cyclical,
                    'commodities':cyclical_commodities,
                    'consumer':cyclical_consumer,
                    'finance':cyclical_finance,
                    'real_estate':cyclical_real_estate
                 },
            'dynamic':
                {
                    'total':top_dynamic,
                    'communication':dynamic_communication,
                    'energy':dynamic_energy,
                    'industrials':dynamic_industrials,
                    'technology':dynamic_technology
                },
            'stabile':
                {
                    'total': top_stabile,
                    'consumer': stabile_consumer,
                    'healthcare': stabile_healthcare,
                    'public': stabile_public
                }
        }

    def make_portfolio_object(self):
        return {
            'portfolio_report_date':self.portfolio_report_date,
            'investment_style':self.investment_style,
            'ratios':self.ratios,
            'geographic_allocation':self.geographic_allocation,
            'industri_allocation':self.industri_allocation
        }


class Fixed_Income_Portfolio(Fund_Base):

    def __init__(self, morningstar_id):
        self.page = requests.get('http://www.morningstar.se/Funds/Quicktake/Portfolio.aspx?perfid=' + morningstar_id)
        self.tree = html.fromstring(self.page.content)
        self.ratios = self.get_ratios()
        self.credit_rating = self.get_credit_ratings()
        self.durations = self.get_durations()
        self.portfolio_data = self.make_portfolio_object()

    def get_ratios(self):
        average_yield_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[1]/span[1]/span')
        average_duration_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[1]/span[2]/span')

        average_yield = self.format_float(average_yield_element[0].text_content())
        average_duration = self.format_float(average_duration_element[0].text_content())
        return {
            'average_yield':average_yield,
            'average_duration':average_duration
            }

    def get_credit_ratings(self):
        first_label_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/h6[1]')
        first_label = first_label_element[0].text_content().strip()
        if first_label == 'Snitt kreditkvalitet':
            average_rating_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[1]/span')
            AAA_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[2]/span')
            AA_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[3]/span')
            A_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[4]/span')
            BBB_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[5]/span')
            BB_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[6]/span')
            B_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[7]/span')
            junk_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[8]/span')
            not_rated_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[9]/span')
            average_rating = average_rating_element[0].text_content().strip()
        else:
            average_rating = None
            AAA_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[1]/span')
            AA_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[2]/span')
            A_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[3]/span')
            BBB_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[4]/span')
            BB_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[5]/span')
            B_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[6]/span')
            junk_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[7]/span')
            not_rated_element = self.tree.xpath(
                '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[2]/span[8]/span')

        AAA = self.format_float(AAA_element[0].text_content())
        AA = self.format_float(AA_element[0].text_content())
        A = self.format_float(A_element[0].text_content())
        BBB = self.format_float(BBB_element[0].text_content())
        BB = self.format_float(BB_element[0].text_content())
        B = self.format_float(B_element[0].text_content())
        junk = self.format_float(junk_element[0].text_content())
        not_rated = self.format_float(not_rated_element[0].text_content())

        return {
            'average_rating':average_rating,
            'AAA':AAA,
            'AA':AA,
            'A':A,
            'BBB':BBB,
            'BB':BB,
            'B':B,
            'junk':junk,
            'not_rated':not_rated
        }

    def get_durations(self):
        y1_3_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[3]/span[1]/span')
        y3_5_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[3]/span[2]/span')
        y5_7_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[3]/span[3]/span')
        y7_10_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[3]/span[4]/span')
        y10_15_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[3]/span[5]/span')
        y15_20_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[3]/span[6]/span')
        y20_30_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_fiInvestmentStyleBond_ctl04"]/div/div[3]/span[7]/span')


        y1_3 = self.format_float(y1_3_element[0].text_content())
        y3_5 = self.format_float(y3_5_element[0].text_content())
        y5_7 = self.format_float(y5_7_element[0].text_content())
        y7_10 = self.format_float(y7_10_element[0].text_content())
        y10_15 = self.format_float(y10_15_element[0].text_content())
        y15_20 = self.format_float(y15_20_element[0].text_content())
        y20_30 = self.format_float(y20_30_element[0].text_content())

        return {
            '1_3y': y1_3,
            '3_5y': y3_5,
            '5_7y': y5_7,
            '7_10y': y7_10,
            '10_15y': y10_15,
            '15_20y': y15_20,
            '20_30y': y20_30,
        }

    def make_portfolio_object(self):
        return {
            'ratios':self.ratios,
            'credit_rating':self.credit_rating,
            'durations':self.durations
        }