from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
from datetime import  datetime
import settings

class Document(models.Model):
    file = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='uploads')
    title = models.CharField(max_length=1000,null=True,blank=True)
    comment = models.TextField(null=True,blank=True)

    upload_date = models.DateTimeField(blank=False)
    upload_user = models.ForeignKey(User,unique=False,null=True, related_name='%(class)s_user_upload')
    update_date = models.DateTimeField(blank=False,null=True)
    update_user = models.ForeignKey(User,unique=False,null=True, related_name='%(class)s_user_update')

    downloadCount = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.title)