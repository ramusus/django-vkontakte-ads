# -*- coding: utf-8 -*-
from ajax_select import LookupChannel
from vkontakte_api.utils import api_call

class VkontakteAdsLookupChannel(LookupChannel):

    section = None

    def get_query(self, q, request):
        # TODO: make model Suggestion and use it
        response = api_call('ads.getSuggestions', methods_access_tag='ads', **{'section': self.section, 'q': q})
#        print response
        return response

    def get_pk(self, obj):
        return obj['id']

    def get_result(self, obj):
        """ The text result of autocompleting the entered query """
        return unicode(obj['name'])

    def format_match(self, obj):
        """ (HTML) formatted item for displaying item in the dropdown """
        return unicode(obj['name'])

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return unicode(obj['name'])

    def get_objects(self, ids):
        if ids:
            response = api_call('ads.getSuggestions', methods_access_tag='ads', **{'section': self.section})
            return [item['name'] for item in response if item['id'] in ids]
        else:
            return []

class ReligionsLookup(VkontakteAdsLookupChannel):
    section = 'religions'
class CountriesLookup(VkontakteAdsLookupChannel):
    # TODO: strange response
    section = 'countries'
class PositionsLookup(VkontakteAdsLookupChannel):
    section = 'positions'
class GroupTypesLookup(VkontakteAdsLookupChannel):
    section = 'group_types'
class BrowsersLookup(VkontakteAdsLookupChannel):
    section = 'browsers'

class CitiesLookup(VkontakteAdsLookupChannel):
    section = 'cities'
class DistrictsLookup(VkontakteAdsLookupChannel):
    section = 'districts'
class StreetsLookup(VkontakteAdsLookupChannel):
    section = 'streets'

    def get_objects(self, ids):
        response = api_call('ads.getSuggestions', methods_access_tag='ads', **{'section': self.section, 'cities': '1'})
        return [item['name'] for item in response if item['id'] in ids]

class SchoolsLookup(VkontakteAdsLookupChannel):
    section = 'schools'

    def get_result(self, obj):
        return unicode('%s (%s)' % (obj['name'], obj['desc']))

    def format_match(self, obj):
        return unicode('%s (%s)' % (obj['name'], obj['desc']))

    def format_item_display(self, obj):
        return unicode('%s (%s)' % (obj['name'], obj['desc']))

class RegionsLookup(VkontakteAdsLookupChannel):
    section = 'regions'

class InterestsLookup(VkontakteAdsLookupChannel):
    section = 'interests'

    def get_objects(self, ids):
        return ids

    def get_pk(self, obj):
        return unicode(obj)

    def get_result(self, obj):
        return unicode(obj)

    def format_match(self, obj):
        return unicode(obj)

    def format_item_display(self, obj):
        return unicode(obj)
