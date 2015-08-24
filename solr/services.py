import re
from collections import OrderedDict
import requests

class CategoryFacetService(object):
    def __init__(self, facet_search_field):
        self.facet_search_field = facet_search_field
        self.facet_query_infos = []
        self.facet_query_infos.append(('contract', self.create_facet_query(['contract', 'order',
                                                                            'agreement', 'funding', 'award'])))
        self.facet_query_infos.append(('research', self.create_facet_query(['research', 'study'])))
        self.facet_query_infos.append(('technology', self.create_facet_query(['technology', 'technique'])))
        self.facet_query_infos.append(('program', self.create_facet_query(['program','plan',
                                                                              'project','strategy', 'policy'])))
        #self.facet_query_infos.append(('performance', self.create_facet_query(['performance', 'efficiency',
        #                                                                       'capability', 'quality','ability',
        #                                                                       'flexibility'])))
        self.facet_query_infos.append(('report', self.create_facet_query(['report','paper'])))
        self.facet_query_infos.append(('test', self.create_facet_query(['test','launch'])))
        #self.facet_query_infos.append(('damage', self.create_facet_query(['kill', 'damage'])))
        self.facet_query_infos.append(('training', self.create_facet_query(['training'])))
        #self.facet_query_infos.append(('cost', self.create_facet_query(['cost'])))
        self.facet_query_infos.append(('statement', self.create_facet_query(['tell', 'say', 'speak',
                                                                             'statement'])))
        self.facet_query_infos.append(('deloy', self.create_facet_query(['deploy','deployment'])))
        self.facet_query_infos.append(('deliver', self.create_facet_query(['deliver'])))
        self.facet_query_infos.append(('budget', self.create_facet_query(['budget'])))

        self.facet_querys = [s[1] for s in self.facet_query_infos]
        self.facet_query_map = {}
        for name, query in self.facet_query_infos:
            self.facet_query_map[query] = name
    def create_facet_query(self, keywords):
        return '%s:(%s)' %(self.facet_search_field, ' '.join(keywords))
    def parse_facet_result(self, query_response):
        result = []
        for fquery, count in query_response.facets['facet_queries'].iteritems():
            if count > 0:
                result.append((self.facet_query_map[fquery], fquery, count))
        return result

class SuggestService(object):
    '''
    'http://192.168.200.101:8983/solr/gaze_suggest/suggest?suggest=true&'\
           + 'suggest.dictionary=gazeSuggester&suggest.q=%s&wt=json&suggest.count=20'
    '''

    def __init__(self, suggest_url, suggest_name):
        s = '%s/suggest?suggest=true&suggest.dictionary=%s&wt=json' \
                          % (suggest_url, suggest_name)
        self.suggest_name = suggest_name
        self.base_url = s + '&suggest.q=%s&suggest.count=%d'
    def suggest(self, part, count = 20):
        url = self.base_url % (part, count)
        res = requests.get(url)
        category_suggestions = OrderedDict()
        for item in res.json()['suggest'][self.suggest_name][part]['suggestions']:
            suggest = {'value': item['term'], 'data': {}}
            if 'payload' in item:
                payload = item['payload']
                k = payload.rindex('_')
                if k > 0:
                    suggest['data']['category'] = payload[k + 1:]
                    suggest['data']['wiki'] = payload[0:k]
            category = 'UNKNOWN'
            if 'category' in suggest['data']:
                category = suggest['data']['category']
            if not category in category_suggestions:
                category_suggestions[category] = []
            category_suggestions[category].append(suggest)
        suggestions = []
        for category, sub_suggestions in category_suggestions.iteritems():
            suggestions.extend(sub_suggestions)

        return {'suggestions': suggestions}


def keyword_filter(word):
    regex = r'^[\w\s-]+$'
    if re.match(regex, word) and not str.isdigit(word) and len(word) > 0:
        if not word.lower() in ['ihs jane', 'full report', 'pdf document', 'publication date',
                                'accessible format', 'view and slideshow', 'legal notice', 'related media'] \
                and not word.endswith('July') and not word.endswith('format'):
            return True
    return False
