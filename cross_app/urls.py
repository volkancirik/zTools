from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from settings import DOCUMENT_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'cross_app.userprofile.views.user_login'),
    (r'^user/', include('cross_app.userprofile.urls')),
    (r'^cross_order/', include('cross_app.cross_order.urls')),
    (r'^dms/', include('cross_app.dms.urls')),
    (r'^sms/', include('cross_app.sms.urls')),
    (r'^rts/', include('cross_app.rts.urls')),
    (r'^cts/', include('cross_app.cts.urls')),
    (r'^rosetta/', include('rosetta.urls')),
    (r'^sms/', include('cross_app.sms.urls')),
    (r'^main/', include('main.urls')),

    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': '%s' % DOCUMENT_ROOT, 'show_indexes': True}),
)
