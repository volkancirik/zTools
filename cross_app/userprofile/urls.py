from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/$', '....userprofile.views.user_login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {"next_page":"/"}),
    (r'^register/$', '....userprofile.views.register'),
)
