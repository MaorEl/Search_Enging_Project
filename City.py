import sys
import urllib.request
import json
import time
from urllib.error import HTTPError
import Parser

city_db = {}  # dictionary of city_name as key, value: dictionary of country,capital,currency

def create_city_db():
    global city_db
    url = "http://restcountries.eu/rest/v2/all?fields=name;capital;population;currencies"
    with urllib.request.urlopen(url) as res:
        data= res.read()
        json_data = json.loads(data)
        for dic in json_data:
            try:
                info_about_city = {'country': dic['name'], 'population': dic['population'], 'currency': dic['currencies'][0]['code'], 'capital': dic['capital']}
            except KeyError:
                info_about_city = {'country': dic['name'], 'population': dic['population'], 'currency': dic['currencies'][1]['code'],'capital': dic['capital']}
            city_db[dic['capital'].upper()]= info_about_city

class City:

    def round_a_sum(self, number):
        if '.' not in number:
            return number
        else:
            sign = ''
            if number[len(number) - 1] in ['K', 'M', 'B']:
                sign = number[len(number) - 1]
                number = number[:-1]
            splited_num = number.split('.')
            if len(splited_num[1]) <= 2:
                return number + sign
            else:
                digit_to_round = splited_num[1][2]
                if digit_to_round >= '5':
                    new_digit = str(int(splited_num[1][1]) + 1)
                else:
                    new_digit = splited_num[1][1]
                return splited_num[0] + '.' + splited_num[1][0] + new_digit + sign

    def __init__(self, city, docID):
        global city_db
        pointer_to_city_db = city_db
        if city in pointer_to_city_db:
            self.capital = city_db[city]['capital']
            self.currency = city_db[city]['currency']
            populuation_to_fix = str(city_db[city]['population'])
            self.population = self.round_a_sum(Parser.number_format(populuation_to_fix))
            self.country = city_db[city]['country']
            self.dic_doc_index = {docID: ['TAG']}
        else:
            try:
                url = 'http://getcitydetails.geobytes.com/GetCityDetails?fqcn=' + city
                with urllib.request.urlopen(url) as url1:
                    s = url1.read()
                    # print(time.time()-start)
                    json_result = json.loads(s)
                    self.capital = json_result['geobytescapital']
                    self.currency = json_result['geobytescurrencycode']
                    population = str(json_result['geobytespopulation'])
                    if population != '':
                        self.population = self.round_a_sum(Parser.number_format(population))
                    self.country = json_result['geobytescountry']
            except:
                self.capital = ''
                self.currency = ''
                self.population = ''
                self.country = ''
                print("Unexpected error occured here!!!:", sys.exc_info()[0])
                pass
            finally:
                self.dic_doc_index = {docID: ['TAG']}
#
# create_city_db()
# c = City("BUDAPEST", "1")
# print(c.capital + ',' + c.currency + ',' + c.country)