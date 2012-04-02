from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cross_dock_order.views.home', name='home'),
    # url(r'^cross_dock_order/', include('cross_dock_order.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^orders/', 'cross_dock_order.order_check.views.order'),

#    (r'^update/(?P<order_id>[a-zA-Z0-9_.-]+)', 'cross_dock_order.order_check.views.updateOrder'),
    (r'^update/', 'cross_dock_order.order_check.views.updateOrder'),
    (r'^sort/(?P<criteria>order_id|barcode|quantity|cross_status)/?$', 'cross_dock_order.order_check.views.sort'),

)
