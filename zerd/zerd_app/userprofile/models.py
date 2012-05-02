from django.db import models
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User,unique=True)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    update_date = models.DateTimeField(default=datetime.datetime.now)
    create_user = models.ForeignKey('auth.User',unique=False,null=True, related_name='profile_user_create',blank=True)
    update_user = models.ForeignKey('auth.User',unique=False,null=True, related_name='profile_user_update',blank=True)
        
    def __unicode__(self):
        return self.user.email
