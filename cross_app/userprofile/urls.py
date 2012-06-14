from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/$', 'cross_app.userprofile.views.user_login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {"next_page":"/"}),
    (r'^register/$', 'cross_app.userprofile.views.register'),
    (r'^change_language/$', 'cross_app.userprofile.views.change_language'),
)
