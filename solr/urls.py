from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import DongtaiDocDetailView
from .views import AllDongtaiView
from .views import DongtaiSearchView
from .views import DocsView

urlpatterns = patterns('',
                       url(r'^search/$', login_required(DongtaiSearchView.as_view()), name='dongtai_search'),
                       url(r'^all/$', login_required(AllDongtaiView.as_view()), name='dongtai_all'),
                       url(r'^detail/$', login_required(DongtaiDocDetailView.as_view()), name='dongtai_detail'),
                       url(r'^dongtai/index/docs/$', login_required(DocsView.as_view()), name='docs_result'),

                       )
