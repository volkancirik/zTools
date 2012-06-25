from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^update_returned_order/$', 'cross_app.rts.views.update_returned_order'),
    (r'^list_all/$', 'cross_app.rts.views.list_all'),
    (r'^search_returned_item/$', 'cross_app.rts.views.search_returned_item'),


)
