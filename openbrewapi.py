# Author: Barrett Duna

"""
Wrapper for the Open Brewery Database (https://www.openbrewerydb.org/) project API.
Provides a query API called BreweryQuery that searches for breweries in the
database by brewery name, city, state, postal code, type of brewery, by tag
and provides functionality to get a brewery by id, search the breweries with a
query and an autocomplete feature which suggests breweries based on a query. A
Brewery class is also created to store the brewery data in.
"""

import requests
import json

class Brewery:

    def __init__(self, brew_dict):
        self.brew_dict = brew_dict
        self.id = brew_dict['id']
        self.name = brew_dict['name']
        self.brewery_type = brew_dict['brewery_type']
        self.street = brew_dict['street']
        self.city = brew_dict['city']
        self.state = brew_dict['state']
        self.postal_code = brew_dict['postal_code']
        self.country = brew_dict['country']
        self.longitude = brew_dict['longitude']
        self.latitude = brew_dict['latitude']
        self.phone = brew_dict['phone']
        self.website_url = brew_dict['website_url']
        self.updated_at = brew_dict['updated_at']
        self.tag_list = brew_dict['tag_list']

    def __str__(self):
        rstr = ''
        for key, val in self.brew_dict.items():
            rstr += '{}: {}'.format(key, val) + '\n'
        return rstr


def brew_key_decorator(func):
    def wrapper(self, *args, **kwargs):
        self.current_key = func.__name__
        return func(self, *args, **kwargs)
    return wrapper


class BreweryQuery:

    RESULTS_PER_PAGE = 50
    base_api_url = 'https://api.openbrewerydb.org/breweries'
    results_per_page = '?per_page=' + str(RESULTS_PER_PAGE) + '&'
    equals = '='

    @brew_key_decorator
    def by_city(self, city_name):
        return self._query(self.current_key, city_name)

    @brew_key_decorator
    def by_name(self, brewery_name):
        return self._query(self.current_key, brewery_name)

    @brew_key_decorator
    def by_state(self, state):
        return self._query(self.current_key, state)

    @brew_key_decorator
    def by_postal(self, postal_code):
        return self._query(self.current_key, postal_code)

    @brew_key_decorator
    def by_type(self, brewery_type):
        return self._query(self.current_key, brewery_type)

    @brew_key_decorator
    def by_tag(self, tag):
        return self._query(self.current_key, tag)

    def get_brewery_by_id(self, id):
        api_url = self.base_api_url + '/' + str(id)
        try:
            source = requests.get(api_url).text
            brew_dict = json.loads(source)
            if 'message' in brew_dict:
                raise ValueError('No brewery has id {}.'.format(id))
            else:
                return Brewery(brew_dict)
        except requests.exceptions.RequestException as e:
            SystemExit(e)

    def search(self, query):
        query = self._encode_val_for_api_url(query)
        api_url = self.base_api_url + '/search?query' +self.equals + query
        try:
            source = requests.get(api_url).text
            brewery_dict_list = json.loads(source)
            return [Brewery(brewery_dict) for brewery_dict in brewery_dict_list]
        except requests.exceptions.RequestException as e:
            SystemExit(e)

    def autocomplete(self, query):
        query = self._encode_val_for_api_url(query)
        api_url = self.base_api_url + '/autocomplete?query' + self.equals \
                                    + query
        try:
            source = requests.get(api_url).text
            brewery_dict_list = json.loads(source)
            if brewery_dict_list:
                return [self.get_brewery_by_id(brewery_dict["id"])
                        for brewery_dict in brewery_dict_list]
            else:
                raise Exception("No breweries matched the autocomplete query.")
        except requests.exceptions.RequestException as e:
            SystemExit(e)

    def _encode_val_for_api_url(self, val):
        return val.lower().replace(' ', '_')

    def _assemble_api_url(self, key, val, page):
        return self.base_api_url + self.results_per_page + key + self.equals \
               + val + '&page=' + str(page)

    def _request_breweries(self, key, val, page):
        try:
            source = requests.get(self._assemble_api_url(key, val, page)).text
            brewery_dict_list = json.loads(source)
            return [Brewery(brewery_dict) for brewery_dict in brewery_dict_list]
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def _query(self, key, val):
        rv = []
        val = self._encode_val_for_api_url(val)
        page = 1
        while True:
            breweries = self._request_breweries(key, val, page)
            if breweries:
                rv += breweries
                page += 1
            else:
                break
        if rv:
            return rv
        else:
            raise Exception("No breweries found for this query.")


if __name__ == '__main__':

    brew_query = BreweryQuery()

    # sf_breweries = brew_query.by_city('San Francisco')
    # print(sf_breweries[0])

    # dog_breweries = brew_query.by_name("dog")
    # print(len(dog_breweries))

    # cali_breweries = brew_query.by_state("California")
    # print(len(cali_breweries))

    # postal_breweries = brew_query.by_postal("94104")
    # print(postal_breweries[0])

    # type_breweries = brew_query.by_type("contract")
    # print(len(type_breweries))

    # brewery_id = brew_query.get_brewery_by_id(3)
    # print(brewery_id)

    # search_results = brew_query.search("cat")
    # print(search_results[0])

    # autocomplete_results = brew_query.autocomplete("bad")
    # for result in autocomplete_results:
    #     print(result.name)
