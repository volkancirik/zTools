from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^search_page/$', 'cross_app.rts.views.search_page'),
    (r'^list_all/$', 'cross_app.rts.views.list_all'),
    (r'^search_returned_item/$', 'cross_app.rts.views.search_returned_item'),


)
