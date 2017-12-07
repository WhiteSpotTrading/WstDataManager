from WstDataManager.morningstar.search import Search
from WstDataManager.morningstar.fund import Fund

funds_dict = Search(search_string='PriorNilsson Idea', fivestar_only=False).results

for key in funds_dict:
    print funds_dict
    morningstar_id = funds_dict[key]['morningstar_id']
    fund = Fund(morningstar_id, base_only=False)
    print fund.fund_data

funds_dict = Search(search_string='XACT OMXS30', fivestar_only=False).results

for key in funds_dict:
    print funds_dict
    morningstar_id = funds_dict[key]['morningstar_id']
    fund = Fund(morningstar_id, base_only=True)
    print fund.fund_data

