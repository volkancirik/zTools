from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^update_returned_order/$', 'cross_app.rts.views.update_returned_order'),
    (r'^update_refunded_order/$', 'cross_app.rts.views.update_refunded_order'),
    (r'^home_warehouse/$', 'cross_app.rts.views.home_warehouse'),
    (r'^home_order_management/$', 'cross_app.rts.views.home_order_management'),
)
