from morningstar import Fund_Base
from lxml import html
from datetime import datetime
import requests



class Risk(Fund_Base):

    def __init__(self, morningstar_id):
        self.page = requests.get('http://www.morningstar.se/Funds/Quicktake/RiskRating.aspx?perfid=' + morningstar_id)
        self.tree = html.fromstring(self.page.content)
        self.rating = self.get_rating()
        self.greeks = self.get_greeks()
        self.risk_data = self.make_risk_object()

    def get_rating(self):
        rating_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_ctl00_ctl04"]/div/div[1]/span[1]/span/img')
        try:
            rating = rating_element[0].get('title')
        except IndexError:
            rating = None
        rating_date_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_col1_ctl00_ctl04"]/div/div[2]/span[2]/span')
        rating_date = datetime.strptime(rating_date_element[0].text_content(), '%Y-%m-%d')
        return {'rating_date':rating_date, 'rating':rating}

    def get_greeks(self):
        alpha_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_ctl03_ModernPortfolioTheoryItem1_ctl04"]/div/div[1]/span[1]')
        beta_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_ctl03_ModernPortfolioTheoryItem1_ctl04"]/div/div[1]/span[1]')
        r_squared_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_ctl03_ModernPortfolioTheoryItem1_ctl04"]/div/div[2]/span[1]')
        sigma_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_ctl04_riskbar_ContentPlaceHolder2"]/div/div/span[1]/span')
        category_sigma_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_ctl04_riskbar_ContentPlaceHolder2"]/div/div/span[2]/span')
        sharp_ratio_element = self.tree.xpath(
            '//*[@id="ctl00_ctl01_cphContent_cphMain_quicktake1_ctl04_riskbar_ContentPlaceHolder2"]/div/div/span[3]/span')

        try:
            alpha = self.format_float(alpha_element[0].text_content())
            beta = self.format_float(beta_element[0].text_content())
            r_squared = self.format_float(r_squared_element[0].text_content())
            sigma = self.format_float(sigma_element[0].text_content())
            category_sigma = self.format_float(category_sigma_element[0].text_content())
            sharp_ratio = self.format_float(sharp_ratio_element[0].text_content())
        except IndexError:
            alpha = None
            beta = None
            r_squared = None
            sigma = None
            category_sigma = None
            sharp_ratio = None

        return {'alpha':alpha,
                'beta':beta,
                'sigma':sigma,
                'category_sigma':category_sigma,
                'r_squared':r_squared,
                'sharp_ratio':sharp_ratio
                }

    def make_risk_object(self):
        return {
            'rating':self.rating,
            'greeks':self.greeks
        }
