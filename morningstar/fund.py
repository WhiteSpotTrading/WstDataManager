from morningstar import Fund_Base
from basedata import BaseData
from returns import Returns
from risk import Risk
from portfolio import EquityPortfolio, Fixed_Income_Portfolio


class Fund(Fund_Base):

    def __init__(self, morningstar_id, base_only=False):
        self.morningstar_id = morningstar_id
        if base_only:
            self.base_data = BaseData(self.morningstar_id).fund_basics
            self.fund_data = self.make_fund_date(base_only=base_only)
        else:
            self.morningstar_id = morningstar_id
            self.base_data = BaseData(self.morningstar_id).fund_basics
            self.returns = Returns(self.morningstar_id).returns_data
            self.risk = Risk(self.morningstar_id).risk_data
            if self.fixed_income():
                self.portfolio = Fixed_Income_Portfolio(self.morningstar_id).portfolio_data
            else:
                self.portfolio = EquityPortfolio(self.morningstar_id).portfolio_data
            self.fund_data = self.make_fund_date()

    def make_fund_date(self, base_only=False):
        if base_only:
            return {
                'base_data': self.base_data
            }
        else:
            return {
                'base_data':self.base_data,
                'returns':self.returns,
                'risk':self.risk,
                'portfolio':self.portfolio
            }

    def fixed_income(self):
        if 'Rnte' in self.strip_swedish(self.base_data['morningstar_category']).split():
            return True
        else:
            return False



