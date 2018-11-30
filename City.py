import sys
import urllib.request
import json
import time
from urllib.error import HTTPError
from Parser import number_format


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
        '''
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
        #except HTTPError:
            # try:
            #     url = 'http://getcitydetails.geobytes.com/GetCityDetails?fqcn=' + city
            #     with urllib.request.urlopen(url) as url1:
            #         s = url1.read()
            #         #print(time.time()-start)
            #         json_result = json.loads(s)
            #         self.capital = json_result['geobytescapital']
            #         self.currency = json_result['geobytescurrencycode']
            #         population = str(json_result['geobytespopulation'])
            #         if population != '':
            #             self.population = self.round_a_sum(number_format(population))
            #         self.country = json_result['geobytescountry']
            # except:
            #print("Unexpected error occured here!!!:", sys.exc_info()[0])
        except:
            pass
            
            #print("Unexpected error occured here!!!:", sys.exc_info()[0])
        finally:
        '''
        self.dic_doc_index = {docID: ['TAG']}

        # self.country = json_result[]
        # self.currency = currency
        # self.population=population
        # self.list_of_tuples_doc_index = {docID:[-1]} # tag index = -1
        # self.capital = capital

        # https://restcountries.eu/rest/v2/capital/tallinn?fields=name;capital;currency;population
        # http://getcitydetails.geobytes.com/GetCityDetails?fqcn=turku
    #
    # def add_doc_index(self, dictionary):
    #     self.dictionary_of_docs_and_locations.update()

# city = City('Berlin', '1')
