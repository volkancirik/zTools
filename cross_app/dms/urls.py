from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^list_documents/$', 'cross_app.dms.views.list_documents'),
    (r'^upload_document/$', 'cross_app.dms.views.upload_document'),
    (r'^document_action/$', 'cross_app.dms.views.document_action'),
)
