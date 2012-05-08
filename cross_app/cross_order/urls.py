from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^list_supplier/$', '....cross_order.views.list_supplier'),
    (r'^list_order/$', '....cross_order.views.list_order'),
    (r'^update_order_list/$', '....cross_order.views.update_order_list'),
    (r'^transaction_list/$', '....cross_order.views.transaction_list'),
    (r'^transaction_details/(?P<code>[\w-]+)/$', '....cross_order.views.transaction_details'),
    (r'^update_trans_order_list/$', '....cross_order.views.update_trans_order_list'),
    (r'^order_history/$', '....cross_order.views.order_history'),
    (r'^exportOrders/$', '....cross_order.views.exportExcelOrders'),
    (r'^exportTransactions/$', '....cross_order.views.exportExcelTransactions'),
    (r'^exportExcelForSupplier/$', '....cross_order.views.exportExcelForSupplier'),
)
