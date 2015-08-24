# -*- coding:utf-8 -*-
from models import Keywords, Department, WebSite
from models import Monitor
# from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
# from xadmin.plugins.inline import Inline
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# from models import IDC, Host, MaintainLog, HostGroup, AccessRecord


class MonitorInline(admin.StackedInline):
    model = Monitor
    extra = 1

class UserAdmin(UserAdmin):
    inlines = [MonitorInline, ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class KeywordsAdmin(admin.ModelAdmin):
    fields = ['keyword', 'status']
    list_display = ('keyword', 'status', 'startdate')
    list_display_links = ['keyword',]
    search_fields = ['keyword']
    list_filter = ['keyword', 'status',]
    list_editable = ['status']


class DepartmentAdmin(admin.ModelAdmin):
    fields = ['dept_name', 'other_info']
    list_display = ('dept_name', 'other_info')
    list_display_links = ('dept_name',)
    search_fields = ['dept_name']
    list_filter = ['dept_name', 'other_info']
    list_editable = ['other_info']


class WebSiteAdmin(admin.ModelAdmin):
    fields = ['website_name', 'url', 'dept_name', 'regdate', 'status']
    list_display = ('website_name', 'url', 'dept_name', 'regdate',
                    'status')
    list_display_links = ['website_name']
    search_fields = ['website_name', 'url', 'dept_name']
    list_filter = ['website_name', 'url', 'dept_name', 'regdate', 'status']
    list_editable = ['status']


admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(WebSite, WebSiteAdmin)
