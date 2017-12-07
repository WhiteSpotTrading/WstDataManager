# This Python file uses the following encoding: utf-8

class Fund_Base(object):

    def iter_obj(self, obj, return_obj):
        for key in obj.keys():
            return_obj[key] = obj[key]
        return return_obj

    def get_base_date(self):
        return self.base_data

    def format_float(self, str_val):
        str_val = str_val.replace(',', '.')
        str_val = str_val.replace('%', '')
        str_val = str_val.replace('-', '0')
        return float(str_val)

    def strip_swedish(self, str):
        return str.encode('ascii', errors='ignore').decode()

    def geo_translations(self):
        return {
            'Afrika och Mellanstern': 'Africa & Middle-East',
            'Asien exkl Japan': 'Asia excl. Japan',
            'Australien och Nya Zeeland': 'Australia & New Zeeland',
            'Japan': 'Japan',
            'Latinamerika': 'Latin America',
            'Nordamerika': 'North America',
            'Sverige': 'Sweden',
            'Vsteuropa exkl Sverige': 'Western Europe',
            'steuropa': 'Eastern Europe'
        }