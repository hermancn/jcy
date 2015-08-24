# -*-:coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


KEYWORD_STATUS = (
    (1, u'启用'),
    (0, u'停用'),
)
DEPT_INFO = (
    (1, u'省院'),
    (0, u'市院'),
)


class Keywords(models.Model):
    keyword = models.CharField(max_length=64, verbose_name=u'关键词')
    startdate = models.DateTimeField(auto_now=True, verbose_name=u'启用日期')
    status = models.SmallIntegerField(choices=KEYWORD_STATUS, verbose_name=u'状态')

    def __unicode__(self):
        return self.keyword

    class Meta:
        verbose_name = u"监控关键字"
        verbose_name_plural = verbose_name


class Department(models.Model):
    dept_name = models.CharField(max_length=64, verbose_name=u'部门名称')
    other_info = models.IntegerField(choices=DEPT_INFO,
                                     verbose_name=u'部门类型')

    def __unicode__(self):
        return self.dept_name

    class Meta:
        verbose_name = u'监控部门'
        verbose_name_plural = verbose_name


class WebSite(models.Model):
    website_name = models.CharField(max_length=64, verbose_name=u'网站名')
    url = models.URLField(verbose_name=u'网站地址')
    dept_name = models.ForeignKey(Department, verbose_name=u'所属部门')
    regdate = models.DateField()
    status = models.SmallIntegerField(choices=KEYWORD_STATUS, verbose_name=u'状态')

    def __unicode__(self):
        return self.website_name

    class Meta:
        verbose_name = u"监控网站"
        verbose_name_plural = verbose_name


class Monitor(models.Model):
    user = models.OneToOneField(User)
    dept_name = models.OneToOneField(Department)
