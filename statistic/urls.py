from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import AllStatisticView
from .views import WebStatisticView
from .views import JsondataView

urlpatterns = patterns('',
                       url(r'^base/$', login_required(AllStatisticView.as_view()), name='statistic_all'),
                       url(r'^web/$', login_required(WebStatisticView.as_view()), name='statistic_web'),
                       url(r'^data/$', login_required(JsondataView.as_view()), name='statistic_data'),

                       )
