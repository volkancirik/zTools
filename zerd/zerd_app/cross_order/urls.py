from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^list_supplier/$', 'zerd_app.cross_order.views.list_supplier'),
    (r'^list_order/$', 'zerd_app.cross_order.views.list_order'),
    (r'^update_order_list/$', 'zerd_app.cross_order.views.update_order_list'),
    (r'^transaction_list/$', 'zerd_app.cross_order.views.transaction_list'),
    (r'^transaction_details/(?P<code>[\w-]+)/$', 'zerd_app.cross_order.views.transaction_details'),
    (r'^update_trans_order_list/$', 'zerd_app.cross_order.views.update_trans_order_list'),
    (r'^order_history/$', 'zerd_app.cross_order.views.order_history'),
    (r'^exportOrders/$', 'zerd_app.cross_order.views.exportExcelOrders'),
    (r'^exportTransactions/$', 'zerd_app.cross_order.views.exportExcelTransactions'),
)
