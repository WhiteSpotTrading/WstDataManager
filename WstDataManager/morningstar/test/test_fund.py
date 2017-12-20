from WstDataManager.morningstar.fund import Fund
import pprint

"""
funds_list = ['0P0000P3Y4','0P0000U46Q',
              '0P00000K48','0P0000WVXD',
              '0P00000LCG','0P00014CYL',
              '0P00014CYL','0P0000NC0M',
              '0P00000F01','0P0000S55A',
              '0P0001038E','0P0000U46Q',
              '0P0000RWIQ','0P0000XPGN']
"""
funds_list = ['0P00000K48']
for fund in funds_list:
    a = Fund(fund, base_only=True)
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(a.fund_data)
