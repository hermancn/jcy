# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.utils.http import urlencode
from django.contrib.auth.models import User

from mysolr import Solr
import json

from solr.page import Pagination

from .models import DocumentLog
from .models import SearchLog
import html2text

from jcy.settings import SOLR_SERVER
from monitor.models import Monitor, WebSite, Department, Keywords
from .models import HandleMsg


class SearchView(View):
    facet_field_infos = []
    facet_pivots = None
    facet_limit = None
    hl_fl = None
    available_search_fields = None
    available_sort = None
    date_field = None

    def get(self, request, *args, **kwargs):
        facet_fields = [facet_field_info[0] for facet_field_info in self.facet_field_infos]
        query_context = request.GET.copy()  #use for pagination and facets
        if 'start' in query_context:
            del query_context['start']

        start = int(request.GET.get('start', 0))
        rows = int(request.GET.get('rows', 20))
        remove_facet_filters = request.GET.getlist('rfacet')

        q = query_context.get('q', None)
        facet_filters = query_context.getlist('fq', None)

        keywords_filter = get_keywords_filter()

        if not q:
            q = 'page:' + '(' + keywords_filter + ')'
        else:
            q = 'page:' + '(' + keywords_filter + ' OR '+ q +')'

        query = {'q' : q, 'rows': rows, 'start': start, 'fl': self.fl, 'hl':
                 'true',  'facet':  'true'}

        sites_filter = user_sites_filter(request)
        if 'fq' in query:
            if sites_filter:
                query['fq'].append(sites_filter)
        else:
            if sites_filter:
                query['fq'] = [sites_filter]


        if self.hl_fl:
            query.update({'hl.fl':self.hl_fl, 'hl.simple.pre':self.hl_pre,
                          'hl.simple.post':self.hl_post, 'hl.fragsize': 0})

        if facet_fields:
            query['facet.field'] = facet_fields
            query['facet.mincount'] = 1
        if self.facet_pivots:
            query['facet.pivot'] = self.facet_pivots
            query['facet.mincount'] = 1
        if self.facet_limit:
            query['facet.limit'] = self.facet_limit
        else:
            query['facet.limit'] = -1
        sort = request.GET.get('sort', None)
        if sort is None or sort == '':
            if q == '*:*':
                if hasattr(self, 'default_sort'):
                    query['sort'] = self.default_sort
        else:
            query['sort'] = sort

        selected_facetes = None
        if facet_filters:
            if remove_facet_filters:
                for remove_facet_filter in remove_facet_filters:
                    if remove_facet_filter in facet_filters:
                        facet_filters.remove(remove_facet_filter)
                del query_context['rfacet']
                if len(facet_filters) > 1:
                    query_context['fq'] = facet_filters
                elif len(facet_filters) == 1:
                    query_context['fq'] = facet_filters[0]
                else:
                    del query_context['fq']
            parsed_facet_filters = parse_facet_parameters(facet_filters)
            if parsed_facet_filters:
                query['fq'] = parsed_facet_filters[0]
                selected_facetes = parsed_facet_filters[1]

        context = {}

        date_from = request.GET.get('date_from', None)
        date_to = request.GET.get('date_to', None)
        date_query = parse_date_query(self.date_field, date_from, date_to)
        if date_query:
            if date_from:
                context['date_from'] = date_from
            if date_to:
                context['date_to'] = date_to

            if 'fq' in query:
                query['fq'].append(date_query)
            else:
                query['fq'] = [date_query]


        if 'qf' in request.GET:
            query['qf'] = request.GET['qf']
            context['qf'] = request.GET['qf']

        self.change_query(request, query)
        query_response = self.server.search(**query)

        if 'q' in request.GET:
            user_name = 'guest'
            if request.user.is_authenticated():
                user_name = request.user.username
            log = SearchLog(user_name=user_name, ip=
                            request.META['REMOTE_ADDR'],  filter_query=
                            ';'.join(query.get('fq', [])),  query=
                            query_context.get('q', None), start=
                            int(query.get('start', 0)), sort=query.get('sort',
                                                                       None))
            log.save()

        if self.available_search_fields:
            context['available_search_fields'] = self.available_search_fields
        if self.available_sort:
            context['available_sort'] = self.available_sort

        context['page_url'] = urlencode(query_context, True)
        context['page_url_encode'] = '&'.join([key +'=' + value.replace('"', '%22') for key,value in query_context.items()])

        if 'select_id' in query_context:
            context['select_id'] = query_context['select_id']
        if 'q' in query_context:
            context['q'] = query_context['q'].replace('"', '\"')
        if 'sort' in query_context:
            context['sort'] = query_context['sort']
        if len(facet_fields) > 0:

            if 'facet_fields' in query_response.facets:
                original_facets = query_response.facets['facet_fields']
                context['facets'] = pack_facets(original_facets, self.facet_field_infos, selected_facetes)

        if query_response.documents:
            highlight(query_response, self.id_field)
            docs = query_response.documents

            if self.date_field:
                parsed_date_field = self.date_field + '_date'
            for doc in docs:
                if self.date_field:
                    doc[parsed_date_field] = parse_date('%Y-%m-%dT%H:%M:%SZ', doc[self.date_field])
                hm = get_doc_handlemsg(doc)
                if hm:
                    doc['handle_msg'] = hm.handle_msg
                    doc['article_status'] = hm.article_status
                    doc['msg_time'] = hm.msg_time

            context['results'] = docs
            context['page'] = Pagination(total = query_response.total_results, start = start, rows = rows)

        self.populate_other_context(request, query_response, context)

        this_template = self.get_template(request)

        return render(request, this_template, context)

    def populate_other_context(self, request, query_response, context):
        pass

    def change_query(self, request, query):
        pass

    def get_template(self, request):
        return request.GET.get('template', self.template)


class DocDetailView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')

        id = request.GET.get('id', None)
        if not id:
            return HttpResponse("No id param.")
        url = request.GET.get('url', id)
        hl_q = request.GET.get('q', None)
        site = request.GET.get('site', None)
        q = self.id_field + ':"' + id + '"'
        query = {'q': q, 'rows': 1}

        if hl_q and self.hl_fl:
            query.update({'hl': 'true', 'hl.fragsize': 0, 'hl.fl': self.hl_fl, 'hl.q': hl_q,
                          'hl.simple.pre': self.hl_pre, 'hl.simple.post': self.hl_post})
        query_response = self.server.search(**query)
        context = {}

        if query_response.documents:
            highlight(query_response, self.id_field)
            doc = query_response.documents[0]
            context['source_id'] = id
            context['document'] = doc
            if 'raw_data' in doc:
                h = html2text.HTML2Text()
                h.ignore_links = True
                h.ignore_images = True
                context['text'] = h.handle(doc['raw_data'])

        user_name = 'guest'
        if request.user.is_authenticated():
            user_name = request.user.username
        ip = request.META['REMOTE_ADDR']
        log = DocumentLog(user_name=user_name, site=site, document_id=url, query=hl_q, ip=ip)
        log.save()
        return render(request, self.template, context)


class DongtaiSearchView(SearchView):
    fl = ['title', 'url', 'id', 'site','text', 'raw_data', 'processed_at',]
    id_field = 'id'
    hl_pre = '<span class="hl">'
    hl_post = '</span>'
    hl_fl = 'title,text'
    server = Solr(SOLR_SERVER)
    available_sort = [('', '按相似度排序',), ('processed_at desc', '按日期排序',)]
    available_search_fields = [('text', '检索标题和全文',), ('title', '仅检索标题',)]
    default_sort = 'processed_at desc'
    template = 'solr/dongtai.html'


class AllDongtaiView(DongtaiSearchView):
    template = 'solr/dongtai_new.html'
    facet_pivots = ['site']
    facet_limit = 30

    def post(self, request, *args, **kwargs):
        article_id = request.POST.get('article_id')
        msg = request.POST.get('msg')
        article_site = request.POST.get('article_site')
        article_status = request.POST.get('article_status')

        handle_msg = HandleMsg()
        handle_msg.user_name = request.user.get_username()
        handle_msg.article_site = article_site
        handle_msg.handle_msg = msg
        handle_msg.article_id = article_id
        handle_msg.article_status = article_status
        handle_msg.save()

        return HttpResponse(json.dumps({"result": "ok"}),
                            content_type="application/json")



    def change_query(self, request, query):
        query['f.site.facet.sort'] = 'index'
        query['f.site.facet.limit'] = -1
        query['facet.sort'] = 'count'


    def populate_other_context(self, request, query_response, context):
        pivot_nodes = []
        facet_pivot_results = query_response.facets['facet_pivot']
        for facet_pivot in self.facet_pivots:
            facet_pivot_result = facet_pivot_results[facet_pivot]
            pivot_nodes.append(facet_pivot_result)
        context['pivot_nodes'] = pivot_nodes


'''
class NewDongtaiView(AllDongtaiView):
    def change_query(self, request, query):
        super(NewDongtaiView, self).change_query(request, query)
        now = datetime.now()
        yesterday = now + timedelta(days=-1)
        if now.weekday() == 0:
            yesterday = now + timedelta(days=-3)
        # time_query = 'crawled:[ 2015-08-01T23:10:19Z TO 2015-08-04T23:10:19Z ]'
        # TODO: change time_query
        time_query = 'crawled:['+ datetime.strftime(yesterday, '%Y-%m-%d 08:00:00') + ' TO ' + \
            datetime.strftime(now, '%Y-%m-%d 08:00:00') + ']'

        if 'fq' in query:
            query['fq'].append(time_query)
        else:
            query['fq'] = [time_query]
'''



class DocsView(AllDongtaiView):
    template = 'solr/dongtai_index_docs.html'

    def change_query(self, request, query):
        query['rows'] = 10


class DongtaiDocDetailView(DocDetailView):
    server = Solr(SOLR_SERVER)
    #id_field = 'url'
    id_field = 'id'
    hl_pre = '<span class="hl">'
    hl_post = '</span>'
    #hl_fl = 'html'
    hl_fl = None #has problem when highlighting html field
    template = 'solr/dongtai_detail.html'


def parse_facet_parameters(facet_filters):
    if facet_filters:
        facet_fields = []
        for facet_filter in facet_filters:
            while facet_filter.startswith('(') and facet_filter.endswith(')'):
                facet_filter = facet_filter[1:len(facet_filter)-1]
            if ':' in facet_filter and facet_filter.count(':') == 1:
                facet_fields.append(facet_filter.split(':', 1))
            else:
                facet_fields.append(('', facet_filter,))
        altered_facet_filters = []
        for facet_field, facet_value in facet_fields:
            if facet_field:
                facet_value = facet_value.strip(' "')
                facet_value = facet_value.replace('"', '\"')
                #facet_value = facet_value.replace(':', '\:')
                if not facet_value.startswith('"') or not facet_value.endswith('"'):
                    facet_value = '"' + facet_value + '"'
                altered_facet_filters.append(facet_field + ":" + facet_value)
            else:
                altered_facet_filters.append(facet_value)
        return altered_facet_filters, facet_fields
    return None

def highlight(query_response, id_field):
    if query_response.highlighting:
        for doc in query_response.documents:
            id = doc[id_field]
            id = str(id)
            if id in query_response.highlighting:
                for field in query_response.highlighting[id]:
                    doc[field] = query_response.highlighting[id][field][0]

def pack_facets(facets, facet_field_infos, selected_facetes = None):
    return [(field, get_facet_field_info(facet_field_infos, field)[1],
            facets[field], get_selected_facet(selected_facetes, field)) for field in facets]

def get_facet_field_info(facet_field_infos, field_name):
    for facet_field_info in facet_field_infos:
        if field_name == facet_field_info[0]:
            return facet_field_info
    return None

def get_selected_facet(selected_facetes, field_name):
    if selected_facetes is None:
        return None
    return [selected_facet[1] for selected_facet in selected_facetes if field_name == selected_facet[0]]

def find_values(arr, to_find):
    return [value for key, value in arr if key == to_find]

def parse_date_query(date_field, date_from, date_to):
    if not date_field:
        return None
    if not date_from and not date_to:
        return None
    result = date_field + ':['
    if date_from:
        result = result + date_from +'T00:00:00Z'
    else:
        result = result + '*'
    result = result + ' TO '
    if date_to:
        result = result + date_to +'T23:59:59Z'
    else:
        result = result + '*'
    result = result + ']'
    return result


def parse_date(format, date_str):
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, format)
    except:
        return None


def user_sites_filter(request):
# 省院组用户能看到所有监控
    if len(request.user.groups.all()) > 0:
        if request.user.groups.all()[0].name == '省院':
                return None
    name = request.user.get_username()
    t_user = User.objects.get(username=name)

    monitor = Monitor.objects.get(user=t_user)
    dept = monitor.dept_name
    websites = WebSite.objects.filter(dept_name=dept)

    sites_list = []
    for site in websites:
        sites_list.append(site.website_name)

    sites_filter = 'site:' + '(' + ' OR '.join(sites_list) + ')'
    return sites_filter

def get_keywords_filter():
    keywords = []
    for e in Keywords.objects.all():
        keywords.append(e.keyword)

    keywords_filter = ' OR '.join(keywords)
    return keywords_filter

def get_doc_handlemsg(doc):
    try:
        hm = HandleMsg.objects.get(article_id=doc['id'])
    except HandleMsg.DoesNotExist:
        return None
    return hm
