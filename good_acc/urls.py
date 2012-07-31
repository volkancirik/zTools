from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from settings import DOCUMENT_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'good_acc.acceptance.views.upload_csv'),
    (r'^acceptance/', include('good_acc.acceptance.urls')),

    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': '%s' % DOCUMENT_ROOT, 'show_indexes': True}),
)
