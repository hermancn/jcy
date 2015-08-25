# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dept_name', models.CharField(max_length=64, verbose_name='\u90e8\u95e8\u540d\u79f0')),
                ('other_info', models.IntegerField(verbose_name='\u90e8\u95e8\u7c7b\u578b', choices=[(1, '\u7701\u9662'), (0, '\u5e02\u9662')])),
            ],
            options={
                'verbose_name': '\u76d1\u63a7\u90e8\u95e8',
                'verbose_name_plural': '\u76d1\u63a7\u90e8\u95e8',
            },
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=64, verbose_name='\u5173\u952e\u8bcd')),
                ('startdate', models.DateTimeField(auto_now=True, verbose_name='\u542f\u7528\u65e5\u671f')),
                ('status', models.SmallIntegerField(verbose_name='\u72b6\u6001', choices=[(1, '\u542f\u7528'), (0, '\u505c\u7528')])),
            ],
            options={
                'verbose_name': '\u76d1\u63a7\u5173\u952e\u5b57',
                'verbose_name_plural': '\u76d1\u63a7\u5173\u952e\u5b57',
            },
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dept_name', models.ForeignKey(to='monitor.Department')),
            ],
        ),
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website_name', models.CharField(max_length=64, verbose_name='\u7f51\u7ad9\u540d')),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u5730\u5740')),
                ('regdate', models.DateField()),
                ('status', models.SmallIntegerField(verbose_name='\u72b6\u6001', choices=[(1, '\u542f\u7528'), (0, '\u505c\u7528')])),
                ('dept_name', models.ForeignKey(verbose_name='\u6240\u5c5e\u90e8\u95e8', to='monitor.Department')),
            ],
            options={
                'verbose_name': '\u76d1\u63a7\u7f51\u7ad9',
                'verbose_name_plural': '\u76d1\u63a7\u7f51\u7ad9',
            },
        ),
    ]
