# morningstar API

This package consists of a number of classes that enable extraction of
fund data from the Morningar.se webpage. It uses scraping of the HTML
to extract the data and thus is not the fastest. It should therefore
not be used to extraxt large amounts of data unless your OK with the
accosiated performance issues.

# How it works

## Class: Fund
'Fund' is a base class that compiles a fund data object and stores it
in a class variable called fund_data.

Data is compiled for the given fund when instantiated. To instantiate
the class one calls
```
Fund([MORNINGSTAR_ID])
```
The morningstar_id for a fund can be found on the mornings.se website
in the given funds url:
```
http://www.morningstar.se/Funds/Quicktake/Portfolio.aspx?perfid=0P0000U46Q&programid=0000000000
```
In the above example the morningstar_id is in the get_param called perfid: 0P0000U46Q

To get the data from the class object call the attribute called fund_data
ie:
```
Fund('0P00000K48').fund_data
```
will return a fund data object for a Equity/Mixed fund
### Fund data object for Equity and Mixed Funds
```
{'base_data': {'currency': 'SEK',
               'morningstar_category': 'Branschfond, ny teknik',
               'morningstar_id': '0P00000K48',
               'name': 'Swedbank Robur Ny Teknik',
               'nav': 673.68,
               'nav_date': datetime.datetime(2017, 12, 6, 0, 0)},
 'portfolio': {'geographic_allocation': {'Africa & Middle-East': 0.0,
                                         'Asia excl. Japan': 0.0,
                                         'Australia & New Zeeland': 0.0,
                                         'Eastern Europe': 5.9,
                                         'Japan': 0.0,
                                         'Latin America': 0.0,
                                         'North America': 12.0,
                                         'Sweden': 52.2,
                                         'Western Europe': 29.9},
               'industri_allocation': {'cyclical': {'commodities': 0.0,
                                                    'consumer': 14.9,
                                                    'finance': 0.0,
                                                    'real_estate': 0.0,
                                                    'total': 14.9},
                                       'dynamic': {'communication': 1.5,
                                                   'energy': 0.0,
                                                   'industrials': 2.8,
                                                   'technology': 47.9,
                                                   'total': 52.3},
                                       'stabile': {'consumer': 0.0,
                                                   'healthcare': 32.8,
                                                   'public': 0.0,
                                                   'total': 32.8}},
               'investment_style': {'equity_positions': 51.0,
                                    'fixed_income_positions': 0.0,
                                    'large_cap': 6.8,
                                    'mid_cap': 41.2,
                                    'small_cap': 52.0},
               'portfolio_report_date': datetime.datetime(2017, 11, 30, 0, 0),
               'ratios': {'price_book': 6.2,
                          'price_cashflow': 25.8,
                          'price_earnings': 35.9}},
 'returns': {'annual_returns': {2013: 30.6,
                                2014: 26.5,
                                2015: 51.6,
                                2016: 24.6,
                                2017: 29.8},
             'average_annual_return': 32.62,
             'average_quarterly_return': 8.436842105263159,
             'quarterly_returns': {'2013': {'Q1': 9.7,
                                            'Q2': 0.5,
                                            'Q3': 9.8,
                                            'Q4': 8.9},
                                   '2014': {'Q1': 6.1,
                                            'Q2': 8.6,
                                            'Q3': 0.6,
                                            'Q4': 10.4},
                                   '2015': {'Q1': 17.5,
                                            'Q2': 9.8,
                                            'Q3': 1.0,
                                            'Q4': 18.7},
                                   '2016': {'Q1': 3.6,
                                            'Q2': 1.6,
                                            'Q3': 21.6,
                                            'Q4': 4.6},
                                   '2017': {'Q1': 11.6,
                                            'Q2': 12.4,
                                            'Q3': 3.3}}},
 'risk': {'greeks': {'alpha': 0.8,
                     'beta': 0.8,
                     'category_sigma': 14.27,
                     'r_squared': 45.3,
                     'sharp_ratio': 2.14,
                     'sigma': 13.74},
          'rating': {'rating': '5',
                     'rating_date': datetime.datetime(2017, 10, 31, 0, 0)}}}
```

```
Fund('0P0000U46Q').fund_data
```
will return a fund data object for a Fixed Income fund

### Fund data object for Fixed Income Fund
```
{'base_data': {'currency': 'SEK',
               'morningstar_category': u'R\xe4nte - \xf6vriga obligationer, h\xf6grisk s\xe4krade',
               'morningstar_id': '0P0000U46Q',
               'name': 'Schroder ISF Glbl Hi Yld A SEK Acc',
               'nav': 1480.2,
               'nav_date': datetime.datetime(2017, 12, 6, 0, 0)},
 'portfolio': {'credit_rating': {'A': 0.2,
                                 'AA': 4.5,
                                 'AAA': 6.3,
                                 'B': 30.6,
                                 'BB': 35.0,
                                 'BBB': 8.1,
                                 'average_rating': 'B',
                                 'junk': 14.9,
                                 'not_rated': 0.8},
               'durations': {'10_15y': 2.1,
                             '15_20y': 1.5,
                             '1_3y': 3.8,
                             '20_30y': 4.0,
                             '3_5y': 16.1,
                             '5_7y': 27.1,
                             '7_10y': 28.4},
               'ratios': {'average_duration': 3.5, 'average_yield': 6.2}},
 'returns': {'annual_returns': {2013: 7.6,
                                2014: 2.1,
                                2015: 2.9,
                                2016: 11.5,
                                2017: 4.5},
             'average_annual_return': 5.720000000000001,
             'average_quarterly_return': 2.2736842105263158,
             'quarterly_returns': {'2013': {'Q1': 2.1,
                                            'Q2': 1.5,
                                            'Q3': 2.9,
                                            'Q4': 4.0},
                                   '2014': {'Q1': 3.0,
                                            'Q2': 2.7,
                                            'Q3': 2.0,
                                            'Q4': 1.4},
                                   '2015': {'Q1': 2.4,
                                            'Q2': 0.1,
                                            'Q3': 3.8,
                                            'Q4': 1.6},
                                   '2016': {'Q1': 1.8,
                                            'Q2': 2.9,
                                            'Q3': 4.5,
                                            'Q4': 1.8},
                                   '2017': {'Q1': 1.8, 'Q2': 1.4, 'Q3': 1.5}}},
 'risk': {'greeks': {'alpha': None,
                     'beta': None,
                     'category_sigma': None,
                     'r_squared': None,
                     'sharp_ratio': None,
                     'sigma': None},
          'rating': {'rating': None,
                     'rating_date': datetime.datetime(2017, 10, 31, 0, 0)}}}
```