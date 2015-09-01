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

from monitor.models import Monitor, WebSite, Department

from solr.models import HandleMsg
from solr.views import get_keywords_filter


class JsondataView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        data_json = []
        if query == 'all':
            user_sites = get_user_sites(request)
            for site in user_sites:
                site.update(get_site_count(site['name']))
                data_json.append(site)

        if query == 'web':
            user_sites = get_user_sites(request)
            web_json = {'web_count':len(user_sites), 'total_count':0,
                         'today_count':0, 'month_count':0, 'year_count':0,
                         'alarm_count':0, 'problem_count':0,
                         'unhandled_count':0}

            for site in user_sites:
                site_count = get_site_count(site['name'])
                web_json['total_count'] = web_json['total_count']+site_count['total_count']
                web_json['today_count'] = web_json['today_count']+site_count['today_count']
                web_json['month_count'] = web_json['month_count']+site_count['month_count']
                web_json['year_count'] = web_json['year_count']+site_count['year_count']
                web_json['alarm_count'] = web_json['alarm_count']+site_count['alarm_count']
                web_json['problem_count'] = web_json['problem_count']+site_count['problem_count']
                web_json['unhandled_count'] = web_json['unhandled_count']+site_count['unhandled_count']

            data_json.append(web_json)

        return HttpResponse(json.dumps(data_json), content_type='application/json')


class AllStatisticView(View):
    template = 'statistic/sites_all.html'

    def get(self, request, *args, **kwargs):
        context = {}
        this_template = self.get_template(request)
        return render(request, this_template, context)

    def get_template(self, request):
        return request.GET.get('template', self.template)


class WebStatisticView(View):
    template = 'statistic/sites_web.html'

    def get(self, request, *args, **kwargs):
        context = {}
        this_template = self.get_template(request)
        return render(request, this_template, context)

    def get_template(self, request):
        return request.GET.get('template', self.template)


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
        site_data['department'] = dept.dept_name
        sites_list.append(site_data)

    print sites_list

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
    problem_count = HandleMsg.objects.filter(article_site=site_name).filter(article_status=u'已处理').count()

    count = {}
    count['total_count'] = total_count
    count['today_count'] = today_count
    #count['week_count'] = week_count
    count['month_count'] = month_count
    count['year_count'] = year_count
    count['alarm_count'] = alarm_count
    count['unhandled_count'] = alarm_count - handled_count
    count['problem_count'] = problem_count

    return count


def get_solr_count(query):
    server = Solr(SOLR_SERVER)
    query_response = server.search(**query)
    count = query_response.total_results
    return count
