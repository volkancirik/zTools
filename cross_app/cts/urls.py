from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^cancel_item/$', 'cross_app.cts.views.cancel_item'),
    (r'^cancel_mass/$', 'cross_app.cts.views.cancel_mass'),
)
