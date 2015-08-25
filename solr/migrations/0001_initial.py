# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=250, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7')),
                ('access_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'\xe8\xae\xbf\xe9\x97\xae\xe6\x97\xa5\xe6\x9c\x9f', editable=False)),
                ('site', models.CharField(max_length=200, null=True, verbose_name=b'\xe4\xbf\xa1\xe6\x81\xaf\xe6\xba\x90', blank=True)),
                ('category', models.CharField(max_length=200, null=True, verbose_name=b'\xe4\xbf\xa1\xe6\x81\xaf\xe7\xb1\xbb\xe5\x88\xab', blank=True)),
                ('document_id', models.CharField(max_length=500, verbose_name=b'\xe6\x96\x87\xe6\xa1\xa3\xe7\xbc\x96\xe5\x8f\xb7')),
                ('query', models.CharField(max_length=500, null=True, verbose_name=b'\xe6\xa3\x80\xe7\xb4\xa2\xe5\xbc\x8f', blank=True)),
                ('ip', models.CharField(max_length=100, null=True, verbose_name=b'IP', blank=True)),
            ],
            options={
                'ordering': ['-access_time'],
                'verbose_name': '\u6d4f\u89c8\u65e5\u5fd7',
                'verbose_name_plural': '\u6d4f\u89c8\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='HandleMsg',
            fields=[
                ('article_id', models.CharField(max_length=100, serialize=False, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0id', primary_key=True)),
                ('user_name', models.CharField(max_length=100, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7')),
                ('article_status', models.CharField(max_length=20, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe7\x8a\xb6\xe6\x80\x81')),
                ('handle_msg', models.TextField(verbose_name=b'\xe5\xa4\x84\xe7\x90\x86\xe6\x84\x8f\xe8\xa7\x81', blank=True)),
                ('msg_time', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'ordering': ['msg_time'],
                'verbose_name': '\u6587\u7ae0\u6279\u6ce8',
                'verbose_name_plural': '\u6587\u7ae0\u6279\u6ce8',
            },
        ),
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=250, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7')),
                ('access_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'\xe8\xae\xbf\xe9\x97\xae\xe6\x97\xa5\xe6\x9c\x9f', editable=False)),
                ('site', models.CharField(max_length=200, null=True, verbose_name=b'\xe4\xbf\xa1\xe6\x81\xaf\xe6\xba\x90', blank=True)),
                ('filter_query', models.CharField(max_length=500, null=True, verbose_name=b'\xe8\xbf\x87\xe6\xbb\xa4\xe6\xa3\x80\xe7\xb4\xa2\xe5\xbc\x8f', blank=True)),
                ('query', models.CharField(max_length=500, null=True, verbose_name=b'\xe6\xa3\x80\xe7\xb4\xa2\xe5\xbc\x8f', blank=True)),
                ('sort', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f', blank=True)),
                ('start', models.IntegerField(default=0, verbose_name=b'\xe8\xb5\xb7\xe5\xa7\x8b\xe5\x8f\xb7')),
                ('ip', models.CharField(max_length=100, null=True, verbose_name=b'IP', blank=True)),
            ],
            options={
                'ordering': ['-access_time'],
                'verbose_name': '\u68c0\u7d22\u65e5\u5fd7',
                'verbose_name_plural': '\u68c0\u7d22\u65e5\u5fd7',
            },
        ),
    ]
