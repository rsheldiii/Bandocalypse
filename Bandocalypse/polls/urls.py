from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('polls.views',
    url(r'^$', 'login_or_create'),
    url(r'^(?P<poll_id>\d+)/$', 'detail'),
    url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
    url(r'^artist$','artist'),
    url(r'^profile_return/$','profile_return'),
    url(r'^profile_login/$','profile_login'),
    url(r'^profile_create/$','profile_create'),
    url(r'^login_or_create/$', 'login_or_create'),
    url(r'^info/', 'info'),
)
