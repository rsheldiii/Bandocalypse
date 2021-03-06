from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login

urlpatterns = patterns('polls.views',
    url(r'^$', 'home'),
    #url(r'^(?P<poll_id>\d+)/$', 'detail'),
    #url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
    url(r'^create/$', 'profile_create'),
    url(r'^profile_login/$','profile_login'),
    url(r'^profile_create/$','profile_create'),
    url(r'^accounts/login/$', login),
    url(r'^accounts/profile/$','profile_return'),
    url(r'^edit/$', 'edit'),
    url(r'^info/$', 'info'),
    url(r'^event/(?P<format>.+)?/$', 'event'),#for some reason I dont have to escape the final slash; it just adds it always
    url(r'^remove/All/$', 'remove_all'),
)
