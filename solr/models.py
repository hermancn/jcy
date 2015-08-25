# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

class SearchLog(models.Model):
    user_name = models.CharField('用户', max_length=250)
    access_time = models.DateTimeField('访问日期', default=datetime.now, editable=False)
    site = models.CharField('信息源', max_length=200, null=True, blank=True)
    filter_query = models.CharField('过滤检索式', max_length=500, null=True, blank=True)
    query = models.CharField('检索式', max_length=500, null=True, blank=True)
    sort = models.CharField('排序', max_length=200, null=True, blank=True)
    start = models.IntegerField('起始号', default = 0)
    ip = models.CharField('IP', max_length=100, null=True, blank=True)
    class Meta:
        verbose_name = '检索日志'
        verbose_name_plural = '检索日志'
        ordering = ['-access_time']


class DocumentLog(models.Model):
    user_name = models.CharField('用户', max_length=250)
    access_time = models.DateTimeField('访问日期', default=datetime.now, editable=False)
    site = models.CharField('信息源', max_length=200, null=True, blank=True)
    category = models.CharField('信息类别', max_length=200, null=True, blank=True)
    document_id = models.CharField('文档编号', max_length=500)
    query = models.CharField('检索式', max_length=500, null=True, blank=True)
    ip = models.CharField('IP', max_length=100, null=True, blank=True)
    class Meta:
        verbose_name = '浏览日志'
        verbose_name_plural = '浏览日志'
        ordering = ['-access_time']


class HandleMsg(models.Model):
    article_id = models.CharField('文章id', primary_key=True, max_length=100)
    user_name = models.CharField('用户', max_length=100)
    article_site = models.CharField('文章来源', max_length=100)
    article_status = models.CharField('文章状态', max_length=20)
    handle_msg = models.TextField('处理意见', blank=True)
    msg_time = models.DateTimeField(default=datetime.now,
                                    editable=False)

    class Meta:
        verbose_name = '文章批注'
        verbose_name_plural = '文章批注'
        ordering = ['msg_time']
