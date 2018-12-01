import sys
import urllib.request
import json
import time
from urllib.error import HTTPError
import Parser

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
        start = time.time()
        try:
            url = 'https://restcountries.eu/rest/v2/capital/' + city + '?fields=name;capital;currencies;population'
            with urllib.request.urlopen(url) as url1:
                if (url1.status == 200):
                    s = url1.read()
                    json_result = json.loads(s)[0]
                    self.capital = json_result['capital']
                    self.currency = json_result['currencies'][0]['code']
                    self.population = self.round_a_sum(number_format(str(json_result['population'])))
                    self.country = json_result['name']
        except HTTPError:
            try:
                url = 'http://getcitydetails.geobytes.com/GetCityDetails?fqcn=' + city
                with urllib.request.urlopen(url) as url1:
                    s = url1.read()
                    #print(time.time()-start)
                    json_result = json.loads(s)
                    self.capital = json_result['geobytescapital']
                    self.currency = json_result['geobytescurrencycode']
                    population = str(json_result['geobytespopulation'])
                    if population != '':
                        self.population = self.round_a_sum(number_format(population))
                    self.country = json_result['geobytescountry']
            except:
                print("Unexpected error occured here!!!:", sys.exc_info()[0])
        except:
            pass

        finally:
            self.dic_doc_index = {docID: ['TAG']}

def create_city_db():
    start = time.time()
    city_db = {} #dictionary of city_name as key, value: dictionary of
    url = "http://restcountries.eu/rest/v2/all?fields=name;capital;population;currencies"
    with urllib.request.urlopen(url) as res:
        data= res.read()
        json_data = json.loads(data)
        for dic in json_data:
            try:
                info_about_city = {'name': dic['name'], 'population': dic['population'], 'currency': dic['currencies'][0]['code']}
            except KeyError:
                info_about_city = {'name': dic['name'], 'population': dic['population'], 'currency': dic['currencies'][1]['code']}
            city_db[dic['capital']]= info_about_city
    end = time.time()
    x=city_db

    print (end-start)

create_city_db()
