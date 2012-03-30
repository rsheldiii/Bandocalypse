# This also imports the include function
from django.conf.urls.defaults import *
from Bandocalypse.settings import MEDIA_ROOT
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','polls.views.home'),
    url(r'^event/$', 'polls.views.event'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': MEDIA_ROOT}),
)
