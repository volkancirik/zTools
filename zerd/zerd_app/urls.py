from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from settings import DOCUMENT_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'zerd_app.userprofile.views.user_login'),
    (r'^user/', include('zerd_app.userprofile.urls')),
    (r'^cross_order/', include('zerd_app.cross_order.urls')),
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': '%s' % DOCUMENT_ROOT, 'show_indexes': True}),
)
