class City:

    def __init__(self, country, currency,population, dic_of_doc_and_location_in_doc):
        self.country = country
        self.currency = currency
        self.population=population
        self.dictionary_of_docs_and_locations = dic_of_doc_and_location_in_doc

        #https://restcountries.eu/rest/v2/capital/tallinn?fields=name;capital;currency;population
