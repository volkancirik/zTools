from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^upload_csv/$', 'good_acc.acceptance.views.upload_csv'),
    (r'^item_view/$', 'good_acc.acceptance.views.item_view'),
    (r'^action/$', 'good_acc.acceptance.views.action'),
)
