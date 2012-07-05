from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
from datetime import  datetime
from django.utils.translation import gettext_lazy as _
import settings

class DocumentType(models.Model):
    name = models.CharField(max_length=1000,null=False)
    order = models.IntegerField(default=9999)
    def __unicode__(self):
        return self.name

#admin.site.register(DocumentType)

class DocumentStatus():
    NEW = 0
    UPLOADED_EKOL = 1
    PROCESSED = 2
    CLOSED = 3

    TYPE = (
            (NEW,_("dms_status_new")),
            (UPLOADED_EKOL ,_("dms_status_uploaded_to_ekol")),
            (PROCESSED,_("dms_status_processed")),
            (CLOSED,_("dms_status_closed")),
            )

class Document(models.Model):
    file = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='uploads')
    title = models.CharField(max_length=1000,null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    type = models.ForeignKey(DocumentType,null=True,blank=True)

    upload_date = models.DateTimeField(blank=False)
    upload_user = models.ForeignKey(User,unique=False,null=True, related_name='%(class)s_user_upload')
    update_date = models.DateTimeField(blank=False,null=True)
    update_user = models.ForeignKey(User,unique=False,null=True, related_name='%(class)s_user_update')

    status = models.IntegerField(default=DocumentStatus.NEW,choices=DocumentStatus.TYPE)
    ekol_doc_number = models.CharField(max_length=1000,null=True,blank=True)

    downloadCount = models.IntegerField(default=0)


    def __unicode__(self):
        return str(self.title)