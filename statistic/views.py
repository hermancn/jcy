# -*- coding: utf-8 -*-
from datetime import timedelta
import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.models import User

from mysolr import Solr

from jcy.settings import SOLR_SERVER

from monitor.models import Monitor, WebSite, Department, Keywords

from solr.models import HandleMsg
from solr.views import get_keywords_filter


class JsondataView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        if query == 'all':
            data_json = []
            user_sites = get_user_sites(request)
            for site in user_sites:
                site.update(get_site_count(site['name']))
                data_json.append(site)

            data = {}
            data['rows'] = data_json
            data['total'] = len(data_json)

        return HttpResponse(json.dumps(data), content_type='application/json')



class AllStatisticView(View):
    template = 'statistic/sites_all.html'

    def get(self, request, *args, **kwargs):
        context = {}
        data_json = []
        user_sites = get_user_sites(request)
        for site in user_sites:
            site.update(get_site_count(site['name']))
            data_json.append(site)

        context['data_json'] = data_json

        this_template = self.get_template(request)

        #return HttpResponse(json.dumps(data_json), content_type='application/json')
        return render(request, this_template, context)


    def get_template(self, request):
        return request.GET.get('template', self.template)
    '''
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
            q = 'page' + '(' + keywords_filter + ')'
        else:
            q = 'page' + '(' + keywords_filter + ' OR '+ q +')'

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
    '''


def get_user_sites(request):
    '''
    返回的数据列表包含:
    name(网站名称), url(地址), regdate(注册日期), department(所属部门)
    '''
    sites_list = []
# 省院组用户能看到所有监控
    if len(request.user.groups.all()) > 0:
        if request.user.groups.all()[0].name == u'省院':

            for site in WebSite.objects.all():
                site_data = {}
                site_data['name'] = site.website_name
                site_data['url'] = site.url
                site_data['regdate'] = site.regdate.strftime('%Y-%m-%d')
                dept = Department.objects.get(id=site.dept_name_id)
                site_data['department'] = dept.dept_name
                sites_list.append(site_data)

            return sites_list

    name = request.user.get_username()
    t_user = User.objects.get(username=name)

    monitor = Monitor.objects.get(user=t_user)
    dept = monitor.dept_name
    websites = WebSite.objects.filter(dept_name=dept)

    for site in websites:
        site_data = {}
        site_data['name'] = site.website_name
        site_data['url'] = site.url
        site_data['regdate'] = site.regdate.strftime('%Y-%m-%d')
        site_data['department'] = dept
        sites_list.append(site_data)

    return sites_list


def get_site_count(site_name):
    now = datetime.datetime.now()
    yesterday = now + timedelta(days=-1)
    this_month = datetime.date.today() - datetime.timedelta(days=datetime.datetime.now().day - 1)
    #this_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
    this_year = now.year

    query = {'q': 'site:'+site_name}
    total_count = get_solr_count(query)

    time_query = 'processed_at:[' + datetime.datetime.strftime(yesterday, '%Y-%m-%d') + ' TO *]'
    query['fq'] = time_query
    today_count = get_solr_count(query)

    #time_query = 'processed_at:[' + datetime.strftime(this_week, '%Y-%m-%d 00:00:00') + ' TO *]'
    #query['fq'] = time_query
    #week_count = get_solr_count(query)

    time_query = 'processed_at:[' + datetime.datetime.strftime(this_month, '%Y-%m-%d') + ' TO *]'
    query['fq'] = time_query
    month_count = get_solr_count(query)

    time_query = 'processed_at:[' + str(this_year) + '-01-01 TO *]'
    query['fq'] = time_query
    year_count = get_solr_count(query)

    # 获取报警文章数
    keywords_filter = get_keywords_filter()
    query['fq'] = 'page:' + '(' + keywords_filter + ')'
    alarm_count = get_solr_count(query)

    # 获取已处理报警文章数
    handled_count = HandleMsg.objects.filter(article_site=site_name).count()

    count = {}
    count['total_count'] = total_count
    count['today_count'] = today_count
    #count['week_count'] = week_count
    count['month_count'] = month_count
    count['year_count'] = year_count
    count['alarm_count'] = alarm_count
    count['unhandled_count'] = alarm_count - handled_count

    return count


def get_solr_count(query):
    server = Solr(SOLR_SERVER)
    query_response = server.search(**query)
    count = query_response.total_results
    return count
