from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^list_supplier/$', 'cross_app.cross_order.views.list_supplier'),
    (r'^list_order/$', 'cross_app.cross_order.views.list_order'),
    (r'^update_order_list/$', 'cross_app.cross_order.views.update_order_list'),
    (r'^transaction_list/$', 'cross_app.cross_order.views.transaction_list'),
    (r'^transaction_details/(?P<code>[\w-]+)/$', 'cross_app.cross_order.views.transaction_details'),
    (r'^update_trans_order_list/$', 'cross_app.cross_order.views.update_trans_order_list'),
    (r'^order_history/$', 'cross_app.cross_order.views.order_history'),
    (r'^exportOrders/$', 'cross_app.cross_order.views.exportExcelOrders'),
    (r'^exportTransactions/$', 'cross_app.cross_order.views.exportExcelTransactions'),
    (r'^exportExcelForSupplier/$', 'cross_app.cross_order.views.exportExcelForSupplier'),
    (r'^update_transaction_status/$', 'cross_app.cross_order.views.update_transaction_status'),
    (r'^report_list/$', 'cross_app.cross_order.views.report_list'),
    (r'^get_excel_report/$', 'cross_app.cross_order.views.get_excel_report'),
)
