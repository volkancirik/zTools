from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/$', 'zerd_app.userprofile.views.user_login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {"next_page":"/"}),
    (r'^register/$', 'zerd_app.userprofile.views.register'),
)
