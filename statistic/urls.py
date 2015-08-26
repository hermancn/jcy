from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import AllStatisticView
from .views import JsondataView

urlpatterns = patterns('',
                       url(r'^$', login_required(AllStatisticView.as_view()), name='statistic_all'),
                       url(r'^data/$', login_required(JsondataView.as_view()), name='statistic_data'),

                       )
