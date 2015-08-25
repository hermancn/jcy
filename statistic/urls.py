from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import AllStatisticView

urlpatterns = patterns('',
                       url(r'^$', login_required(AllStatisticView.as_view()), name='statistic_all'),

                       )
