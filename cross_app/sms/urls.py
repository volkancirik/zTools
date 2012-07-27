from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^list_catalog_simple/$', 'cross_app.sms.views.list_catalog_simple'),
    (r'^update_basket/$', 'cross_app.sms.views.update_basket'),
    (r'^view_basket/$', 'cross_app.sms.views.view_basket'),
    (r'^delete_shipment_item/$', 'cross_app.sms.views.delete_shipment_item'),
    (r'^create_new_shipment/$', 'cross_app.sms.views.create_shipment'),
    (r'^list_shipment/$', 'cross_app.sms.views.list_shipment'),
    (r'^view_shipment/$', 'cross_app.sms.views.view_shipment'),
    (r'^confirm_shipment/$', 'cross_app.sms.views.confirm_shipment'),
    (r'^cancel_shipment/$', 'cross_app.sms.views.cancel_shipment'),
    (r'^receive_shipment/$', 'cross_app.sms.views.receive_shipment'),
    (r'^export_shipment_csv/$', 'cross_app.sms.views.export_shipment_csv'),
    (r'^comment_on_shipment/$', 'cross_app.sms.views.comment_on_shipment'),
)