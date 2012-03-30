from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login

urlpatterns = patterns('polls.views',
    url(r'^$', 'home'),
    #url(r'^(?P<poll_id>\d+)/$', 'detail'),
    #url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
    url(r'^artist$','artist'),
    url(r'^profile_login/$','profile_login'),
    url(r'^profile_create/$','profile_create'),
    url(r'^accounts/login/$', login),
    url(r'^accounts/profile/$','profile_return'),
    url(r'^edit/$', 'edit'),
    url(r'^info/$', 'info'),
    url(r'^event/$', 'event'),
)
