from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^home/$', 'cross_app.main.views.home'),
)
